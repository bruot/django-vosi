#!/usr/bin/env python
import argparse
import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner

def main():
    parser = argparse.ArgumentParser(description='Run the tests for django-vosi.')
    parser.add_argument('test_label', nargs='*', help='Module paths to test; can be modulename, modulename.TestCase or modulename.TestCase.test_method')

    parser.add_argument('-k', '--keepdb', action='store_true', help='Preserves the test DB between runs.')

    args = parser.parse_args()

    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_settings'
    django.setup()
    TestRunner = get_runner(settings)
    #test_runner = TestRunner()
    failures = TestRunner(verbosity=1, keepdb=args.keepdb).run_tests(args.test_label)
    sys.exit(bool(failures))


if __name__ == "__main__":
    main()