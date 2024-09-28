# PYTHON_ARGCOMPLETE_OK

from typing import List
from lpp_collector.config import TEST_BASE_DIR
import argcomplete, argparse
import glob
from pathlib import Path
import pytest


all_testcases = [
    Path(testcase)
    for testcase in glob.glob(f"{TEST_BASE_DIR}/**/*_test.py", recursive=True)
]
all_testsuite_list = sorted(set([testcase.parent.name for testcase in all_testcases]))


base_parser = argparse.ArgumentParser(add_help=False)
base_parser.add_argument(
    "--run-pytest",
    action="store_true",
    help="Enforce running pytest even though not in Docker environment",
)
base_parser.add_argument(
    "testsuite", choices=all_testsuite_list, help="Specify testsuite"
)

full_parser = argparse.ArgumentParser(parents=[base_parser])
specified_testsuite = base_parser.parse_known_args()[0].testsuite

if specified_testsuite in all_testsuite_list:
    all_testcases = [
        testcase
        for testcase in all_testcases
        if testcase.parent.name == specified_testsuite
    ]
    full_parser.add_argument(
        "testcases",
        choices=[testcase.name for testcase in all_testcases] + ["all"],
        help="Specify testcases to run",
        nargs="*",
        default="all",
    )
else:
    full_parser.add_argument(
        "testcases",
        help="Specify testcases to run",
        choices=["all"],
        nargs="*",
        default="all",
    )

argcomplete.autocomplete(full_parser)


def run_pytest(args):
    testsuite: str = args.testsuite
    testcases = [
        testcase for testcase in all_testcases if testcase.parent.name == testsuite
    ]
    specified_testcases: List[str] = args.testcases

    if "all" not in specified_testcases:
        testcases = [
            testcase for testcase in testcases if testcase.name in specified_testcases
        ]

    # Sort testcases by name
    testcase_paths = sorted([str(testcase) for testcase in testcases])

    pytest.main(["-v", *testcase_paths])


def main():
    args = full_parser.parse_args()
    if args.run_pytest:
        run_pytest(args)
