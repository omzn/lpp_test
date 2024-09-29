import os

from lpp_collector.config import TEST_BASE_DIR


def main():
    os.symlink(TEST_BASE_DIR, "/lpp_test")
