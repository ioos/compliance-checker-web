#!/usr/bin/env python

import logging
import json
from compliance_checker.runner import ComplianceCheckerCheckSuite

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def compliance_check(job_id, filepath, checker):
    cs = ComplianceCheckerCheckSuite()
    ds = cs.load_dataset(filepath)
    score_groups = cs.run(ds, checker)

    rpair = score_groups[checker]
    groups, errors = rpair

    aggregates = cs.build_structure(checker, groups, filepath)
    aggregates = cs.serialize(aggregates)
    buf = json.dumps(aggregates)

    return buf

