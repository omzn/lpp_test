"""課題3用テスト"""

import os
import sys
import re
from pathlib import Path
import glob
import subprocess
import itertools
import pytest

from lpp_collector.config import TARGETPATH, TEST_BASE_DIR

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
            out.pop(0)  # 1行目を捨てる
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

TEST_RESULT_DIR = "test_results"
TEST_EXPECT_DIR = Path(__file__).parent / Path("test_expects")

test_data = sorted(glob.glob(f"{TEST_BASE_DIR}/input0[123]/*.mpl", recursive=True))

paramed_test_data = [
    pytest.param(mpl_file, id=Path(mpl_file).stem) for mpl_file in test_data
]


@pytest.mark.timeout(10)
@pytest.mark.parametrize(("mpl_file"), paramed_test_data)
def test_cr_run(mpl_file):
    """準備したテストケースを全て実行する．"""
    if not Path(TEST_RESULT_DIR).exists():
        os.mkdir(TEST_RESULT_DIR)
    out_file = Path(TEST_RESULT_DIR).joinpath(Path(mpl_file).stem + ".out")
    res = common_task(mpl_file, out_file)
    if res == 0:
        expect_file = Path(TEST_EXPECT_DIR).joinpath(Path(mpl_file).stem + ".stdout")
        with open(out_file, encoding="utf-8") as ofp, open(
            expect_file, encoding="utf-8"
        ) as efp:
            out_cont = ofp.read().splitlines()
            est_cont = efp.read().splitlines()
            for out_line, est_line in itertools.zip_longest(
                out_cont, est_cont, fillvalue=""
            ):
                assert out_line == est_line, "Line does not match."

    else:
        expect_file = Path(TEST_EXPECT_DIR).joinpath(Path(mpl_file).stem + ".stderr")
        with open(out_file, encoding="utf-8") as ofp, open(
            expect_file, encoding="utf-8"
        ) as efp:
            try:
                o = int(re.search(r"(\d+)", ofp.read()).group())
                e = int(re.search(r"(\d+)", efp.read()).group())
                assert o - 1 <= e <= o + 1, "Line number of error message is different."
            except IndexError:
                assert False, "Line number does not appear in error message."
