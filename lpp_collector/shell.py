from lpp_collector.config import (
    IS_DOCKER_ENV,
)
from .docker import run_test_container


def main():
    if IS_DOCKER_ENV:
        print("Running in Docker environment")
        return

    run_test_container(["bash"])
