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
import sys


def run_test_container(args: List[str]):
    data_dir = str(Path(LPP_DATA_DIR).absolute())
    os.makedirs(data_dir, exist_ok=True)
    target_path = str(Path(TARGETPATH).absolute())

    # print(f"Data directory: {data_dir}")
    # print(f"Target path: {target_path}")

    fix_perm_args = []

    if not sys.platform.startswith("win"):
        fix_perm_args = [
            "--env",
            f"TARGET_UID={os.getuid()}",
            "--env",
            f"TARGET_GID={os.getgid()}",
        ]

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
        *fix_perm_args,
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
    subprocess.call(["chown", "-R", f"{target_uid}:{target_gid}", LPP_DATA_DIR])


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


def update(force: bool = False):
    if not check_update() and not force:
        return

    print("Updating LPP test environment...")
    previous_image_id = subprocess.check_output(
        ["docker", "inspect", "--format", "{{.Id}}", DOCKER_IMAGE]
    ).decode("utf-8")
    subprocess.call(["docker", "pull", DOCKER_IMAGE])
    current_image_id = subprocess.check_output(
        ["docker", "inspect", "--format", "{{.Id}}", DOCKER_IMAGE]
    ).decode("utf-8")

    if previous_image_id != current_image_id and previous_image_id != "":
        print("Removing old image...")
        subprocess.call(["docker", "rmi", previous_image_id])

    print("Update complete.")
