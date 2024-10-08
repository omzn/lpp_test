"""課題3用テスト"""

import os
import sys
import re
from pathlib import Path
import glob
import subprocess

from lpp_collector.config import TARGETPATH, TEST_BASE_DIR

# import pytest

TARGET = "cr"


class SemanticError(Exception):
    """意味解析エラーハンドラ"""


def command(cmd):
    """コマンドの実行"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        return [result.stdout, result.stderr]
    except subprocess.CalledProcessError:
        print(f"外部プログラムの実行に失敗しました [{cmd}]", file=sys.stderr)
        sys.exit(1)


def common_task(mpl_file, out_file):
    """共通して実行するタスク"""
    try:
        exe = Path(TARGETPATH) / Path(TARGET)
        exec_res = command(f"{exe} {mpl_file}")
        out = []
        sout = exec_res.pop(0)
        serr = exec_res.pop(0)
        if serr:
            raise SemanticError(serr)
        for line in sout.splitlines():
            out.append(re.sub(r"\s", r"", line))
        if out:
            out.pop(0)
            out.sort()
            with open(out_file, mode="w", encoding="utf-8") as fp:
                for l in out:
                    fp.write(l + "\n")
            return 0
        raise SemanticError(serr)
    except SemanticError as exc:
        if re.search(r"sample0", mpl_file):
            for line in serr.splitlines():
                out.append(line)
            with open(out_file, mode="w", encoding="utf-8") as fp:
                for l in out:
                    fp.write(l + "\n")
            return 1
        raise SemanticError(serr) from exc
    except Exception as err:
        with open(out_file, mode="w", encoding="utf-8") as fp:
            print(err, file=fp)
        raise err


# ===================================
# pytest code
# ===================================

TEST_RESULT_DIR = f"{TARGETPATH}/test_results"
TEST_EXPECT_DIR = "test_expects"

test_data = sorted(glob.glob(f"{TEST_BASE_DIR}/input*/*.mpl", recursive=True))


def test_compile():
    """指定ディレクトリでコンパイルができるかをテスト"""
    cwd = os.getcwd()
    os.chdir(TARGETPATH)
    if os.path.isfile("Makefile"):
        exec_res = command("make")
    else:
        exec_res = command(f"gcc -w -o {TARGET} *.c")
    os.chdir(cwd)
    exec_res.pop(0)
    serr = exec_res.pop(0)
    assert not serr, "Compilation failed."


def test_no_param():
    """引数を付けずに実行するテスト"""
    exe = Path(TARGETPATH) / Path(TARGET)
    exec_res = command(f"{exe}")
    exec_res.pop(0)
    serr = exec_res.pop(0)
    assert serr, "No error message when no parameter is given."


def test_not_valid_file():
    """存在しないファイルを引数にした場合のテスト"""
    exe = Path(TARGETPATH) / Path(TARGET)
    exec_res = command(f"{exe} hogehoge")
    exec_res.pop(0)
    serr = exec_res.pop(0)
    assert serr, "No error message when non existent file is given."
