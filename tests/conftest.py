import pytest
import os
import sys
import prophesy.config
import logging

sys.path.append(os.path.join(os.path.dirname(__file__), 'helpers'))

logging.basicConfig(filename="prophesy_test.log", format='%(levelname)s:%(message)s', level=logging.DEBUG)
prophesy.config.load_configuration()
""" Enable incremental testing """


def pytest_runtest_makereport(item, call):
    if "incremental" in item.keywords:
        if call.excinfo is not None:
            parent = item.parent
            parent._previousfailed = item


def pytest_runtest_setup(item):
    if "incremental" in item.keywords:
        previousfailed = getattr(item.parent, "_previousfailed", None)
        if previousfailed is not None:
            pytest.xfail("previous test failed (%s)" % previousfailed.name)
