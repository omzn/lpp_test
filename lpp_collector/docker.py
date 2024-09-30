import os
from pathlib import Path
import subprocess
import time
from typing import List
from lpp_collector.config import (
    DOCKER_IMAGE,
    LPP_DATA_DIR,
    LPP_UPDATE_INTERVAL,
    LPP_UPDATE_MARKER,
    TARGETPATH,
)


def run_test_container(args: List[str]):
    data_dir = str(Path(LPP_DATA_DIR).absolute())
    os.makedirs(data_dir, exist_ok=True)
    target_path = str(Path(TARGETPATH).absolute())

    # print(f"Data directory: {data_dir}")
    # print(f"Target path: {target_path}")

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
        "--env",
        f"TARGET_UID={os.getuid()}",
        "--env",
        f"TARGET_GID={os.getgid()}",
        DOCKER_IMAGE,
        *args,
    ]

    # Run Docker container
    subprocess.call(["docker", *run_args])


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

    subprocess.call(["docker", *build_args])


def fix_permission():
    if "TARGET_UID" not in os.environ or "TARGET_GID" not in os.environ:
        return
    target_uid = os.environ.get("TARGET_UID")
    target_gid = os.environ.get("TARGET_GID")
    subprocess.call(["chown", "-R", f"{target_uid}:{target_gid}", TARGETPATH])


def write_update_marker():
    with open(LPP_UPDATE_MARKER, "w") as f:
        f.write(str(time.time()))


def check_update():
    if not os.path.exists(LPP_UPDATE_MARKER):
        write_update_marker()
        return True

    last_update = os.path.getmtime(LPP_UPDATE_MARKER)
    write_update_marker()

    return (time.time() - last_update) > LPP_UPDATE_INTERVAL


def update():
    if not check_update():
        return

    print("Updating LPP test environment...")
    subprocess.call(["docker", "pull", DOCKER_IMAGE])
    print("Update complete.")
