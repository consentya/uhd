#
# Copyright 2019 Ettus Research, a National Instruments Brand
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
"""
USRP MPM Python Unit testing framework
"""

import unittest
import sys
from sys_utils_tests import TestNet

TESTS = {
    '__all__': {TestNet},
    'n3xx': set(),
}

def get_test_suite(device_name=''):
    """
    Gets a test suite (collection of test cases) which is relevant for
    the specified device.
    """
    # A collection of test suites, generated by test loaders, which will
    # be later combined
    test_suite_list = []
    test_loader = unittest.TestLoader()

    # Combine generic and device specific tests
    test_cases = TESTS.get('__all__') | TESTS.get(device_name, set())
    for case in test_cases:
        new_suite = test_loader.loadTestsFromTestCase(case)
        for test in new_suite:
            # Set up test case class for a specific device.
            # Each test uses a different test case instance.
            if (hasattr(test, 'set_device_name')) and (device_name != ''):
                test.set_device_name(device_name)
        test_suite_list.append(new_suite)

    # Individual test suites are combined into a master test suite
    test_suite = unittest.TestSuite(test_suite_list)
    return test_suite

def run_tests(device_name=''):
    """
    Executes the unit tests specified by the test suite.
    This should be called from CMake.
    """
    test_result = unittest.TestResult()
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_result = test_runner.run(get_test_suite(device_name))
    return test_result

def main():
    if len(sys.argv) >= 2:
        mpm_device_name = sys.argv[1]
    else:
        mpm_device_name = ''

    if not run_tests(mpm_device_name).wasSuccessful():
        sys.exit(-1)

if __name__ == "__main__":
    main()
