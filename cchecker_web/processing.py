#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
from compliance_checker.runner import CheckSuite
from rq.connections import get_current_connection
import six
import base64
import logging
import requests
import json
import io
import os
import sys
import subprocess
from contextlib import contextmanager

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# Py 3.4+ has contextlib.redirect_stdout to redirect stdout to a different
# stream, but use this decorated function in order to redirect output in
# previous versions
@contextmanager
def stdout_redirector(stream):
    old_stdout = sys.stdout
    sys.stdout = stream
    try:
        yield
    finally:
        sys.stdout = old_stdout


def compliance_check(job_id, dataset, checker, path=None):
    '''
    Performs the Check Suite for the specified checker and sets the result in a
    redis result for the job_id

    :param str job_id: ID for the rq job
    :param dataset: Dataset handle
    :param str checker: Check Suite ID for a checker
    :param str path: Full path to dataset directory (OPeNDAP only)
    '''
    try:
        redis = get_current_connection()
        cs = CheckSuite()
        if dataset.startswith('http'):
            dataset = check_redirect(dataset)
        ds = cs.load_dataset(dataset)
        score_groups = cs.run(ds, [], checker)

        rpair = score_groups[checker]
        groups, errors = rpair

        aggregates = cs.build_structure(checker, groups, dataset)
        aggregates = cs.serialize(aggregates)
        aggregates['all_priorities'] = sorted(aggregates['all_priorities'], key=lambda x: x['weight'], reverse=True)
        # We use b64 to keep the filenames safe but it's helpful to the user to see
        # the filename they uploaded
        if not aggregates['source_name'].startswith('http'):
            decoded = base64.b64decode(aggregates['source_name'].split('/')[-1])
            if isinstance(decoded, str):
                aggregates['source_name'] = decoded
            else:
                aggregates['source_name'] = decoded.decode('utf-8')
        aggregates['testname'] = cs._get_check_versioned_name(checker)
        aggregates['cc_url'] = cs._get_check_url(aggregates['testname'])
        aggregates['ncdump'] = ncdump(dataset)
        buf = json.dumps(aggregates)

        # Write the report to a text file for download
        if path is None:
            # Must be a local file, get the path from the dataset
            path = os.path.dirname(dataset)
        fname = 'compliance_{}.txt'.format(job_id)
        output_filename = os.path.join(path, fname)
        with io.open(output_filename, 'w', encoding='utf-8') as f:
            with stdout_redirector(f):
                stdout_output(cs, score_groups, aggregates['source_name'])

        redis.set('processing:job:%s' % job_id, buf, 3600)

        return True

    except Exception as e:
        logger.exception("Failed to process job")
        if getattr(e, 'message', None):
            message = e.message
        else:
            message = str(e)
        error_message = {
            "error": type(e).__name__,
            "message": message
        }
        redis.set('processing:job:%s' % job_id, json.dumps(error_message), 3600)
        return False

def stdout_output(cs, score_groups, source_name):
    '''
    Calls output routine to display results in terminal, including scoring.
    Goes to verbose function if called by user.

    :param CheckSuite cs: Compliance Checker Suite
    :param list score_groups: list of results
    :param str source_name: filename
    '''
    limit = 1 # Strictness
    # Generate the report as normal
    for checker, rpair in six.iteritems(score_groups):
        groups, errors = rpair
        score_list, points, out_of = cs.standard_output(source_name, limit,
                                                        checker,
                                                        groups)
        cs.standard_output_generation(groups, limit, points, out_of, check=checker)
    return groups


def check_redirect(dataset, checked_urls=None):
    '''
    Check for a HTTP Redirect for a URL to a OPeNDAP Dataset

    :param str dataset: URL to the dataset
    :param list checked_urls: List of already checked URLs
    '''
    checked_urls = checked_urls or []
    if dataset in checked_urls:
        raise IOError("Invalid URL")
    checked_urls.append(dataset)
    response = requests.get(dataset + '.das', allow_redirects=False)
    if response.status_code == 301:
        new_location = response.headers['Location']
        new_location = new_location.replace('.das', '')
        return check_redirect(new_location, checked_urls)
    return dataset


def ncdump(dataset):
    '''
    Returns the CDL of the dataset
    '''

    try:
        output = subprocess.check_output(['ncdump', '-h', dataset])
        if not isinstance(output, str):
            output = output.decode('utf-8')
        lines = output.split('\n')
        # replace the filename for safety
        dataset_id = 'uploaded-file'
        lines[0] = 'netcdf %s {' % dataset_id
        filtered_lines = '\n'.join(lines)
    except Exception:
        return "Error generating ncdump"
    return filtered_lines
