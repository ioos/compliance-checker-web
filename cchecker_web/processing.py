#!/usr/bin/env python

import logging
import json
from compliance_checker.runner import CheckSuite
from rq.connections import get_current_connection

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def compliance_check(job_id, filepath, checker):
    cs = CheckSuite()
    ds = cs.load_dataset(filepath)
    redis = get_current_connection()
    score_groups = cs.run(ds, checker)

    rpair = score_groups[checker]
    groups, errors = rpair

    aggregates = cs.build_structure(checker, groups, filepath)
    aggregates = cs.serialize(aggregates)
    buf = json.dumps(aggregates)

    redis.set('processing:job:%s' % job_id, buf, 3600)
    return True
