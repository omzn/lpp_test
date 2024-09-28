import os
from pathlib import Path
import pty
from lpp_collector.config import DOCKER_IMAGE, LPP_DATA_DIR, TARGETPATH


def run_test_container(args):
    data_dir = str(Path(LPP_DATA_DIR).absolute())
    os.makedirs(data_dir, exist_ok=True)
    target_path = str(Path(TARGETPATH).absolute())

    print(f"Data directory: {data_dir}")
    print(f"Target path: {target_path}")

    run_args = [
        "run",
        "-it",
        "--rm",
        "-v",
        f"{target_path}:/workspaces",
        "-v",
        f"{data_dir}:/lpp/data",
        # おまけ
        "-v",
        f"{data_dir}/bash_history:/root/.bash_history",
        "-w",
        "/workspaces",
        DOCKER_IMAGE,
        "lpptest",
        *args,
    ]

    # Run Docker container
    pty.spawn(["docker", *run_args])


def run_debug_build(base_dir: str):
    build_args = [
        "buildx",
        "build",
        "--platform",
        "linux/amd64",
        "-t",
        DOCKER_IMAGE,
        base_dir,
    ]

    pty.spawn(["docker", *build_args])
