# PYTHON_ARGCOMPLETE_OK

import sys
from typing import List
from lpp_collector.config import (
    TEST_BASE_DIR,
    IS_DOCKER_ENV,
)
import argcomplete, argparse
import glob
from pathlib import Path
import pytest
from .docker import fix_permission, run_test_container, run_debug_build, update
import os
import pty

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
        help="Specify testcase to run",
        default="all",
        nargs="?",
    )
else:
    full_parser.add_argument(
        "testcases",
        help="Specify testcase to run",
        choices=["all"],
        default="all",
        nargs="?",
    )

full_parser.add_argument("pytest_args", nargs=argparse.REMAINDER)

argcomplete.autocomplete(full_parser)


def run_pytest(args):
    testsuite: str = args.testsuite
    testcases = [
        testcase for testcase in all_testcases if testcase.parent.name == testsuite
    ]

    if len(testcases) == 0:
        print(f"No testcases found in {testsuite}")
        return

    specified_testcases: List[str] = [args.testcases]

    if "all" not in specified_testcases:
        testcases = [
            testcase for testcase in testcases if testcase.name in specified_testcases
        ]

    # Sort testcases by name
    testcase_paths = sorted([str(testcase.absolute()) for testcase in testcases])

    # print(f"Running pytest with {testcase_paths}")

    pwd = os.getcwd()
    os.environ["LPP_TARGET_PATH"] = pwd
    os.chdir(TEST_BASE_DIR)
    pty.spawn(
        [
            "pytest",
            *args.pytest_args,
            *testcase_paths,
        ]
    )
    os.chdir(pwd)


def main():
    args = full_parser.parse_args()
    # print(args)
    if args.run_pytest or IS_DOCKER_ENV:
        run_pytest(args)
    else:
        if "LPP_DOCKER_BASE" in os.environ:
            run_debug_build(os.environ["LPP_DOCKER_BASE"])
        else:
            update()
        run_test_container(["lpptest", *sys.argv[1:]])

    if IS_DOCKER_ENV:
        # Fix permissions
        fix_permission()


def main_PYTHON_ARGCOMPLETE_OK():
    main()
