#!/usr/bin/env python
# -*- coding: utf-8 -*-

from compliance_checker.runner import CheckSuite
from rq.connections import get_current_connection

import base64
import logging
import requests
import json
import subprocess

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def compliance_check(job_id, dataset, checker):
    '''
    Performs the Check Suite for the specified checker and sets the result in a
    redis result for the job_id

    :param str job_id: ID for the rq job
    :param dataset: Dataset handle
    :param str checker: Check Suite ID for a checker
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
        aggregates['ncdump'] = ncdump(dataset)
        buf = json.dumps(aggregates)

        redis.set('processing:job:%s' % job_id, buf, 3600)
        return True
    except Exception as e:
        logger.exception("Failed to process job")
        error_message = {
            "error": type(e).__name__,
            "message": e.message
        }
        redis.set('processing:job:%s' % job_id, json.dumps(error_message), 3600)
        return False


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

