"""課題4用コンパイルテスト"""
import os
import sys
import re
from pathlib import Path
import glob
import subprocess
import pytest

TARGET = "mpplc"
TARGETPATH = "/workspaces"

class CompileError(Exception):
    """コンパイルエラーハンドラ"""

def command(cmd):
    """コマンドの実行"""
    try:
        result = subprocess.run(cmd, shell=True, check=False,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                universal_newlines=True)
        return [result.stdout,result.stderr]
    except subprocess.CalledProcessError:
        print(f"外部プログラムの実行に失敗しました [{cmd}]", file=sys.stderr)
        sys.exit(1)

def common_task(mpl_file, out_file):
    """共通して実行するタスク"""
    try:
        #mpplc = Path(__file__).parent.parent.joinpath("mpplc")
        exe = Path(TARGETPATH) / Path(TARGET)
        exec_res = command(f"{exe} {mpl_file}")
        cslfile = Path(mpl_file).stem + ".csl"
        out = []
        exec_res.pop(0)
        serr = exec_res.pop(0)
        if serr:
            raise CompileError(serr)
        casl2file = Path(__file__).parent / Path(CASL2_FILE_DIR) / Path(cslfile)
        os.rename(cslfile, casl2file)
        return 0
    except CompileError as exc:
        if re.search(r'sample0', mpl_file):
            out = []
            for line in serr.splitlines():
                out.append(line)
            with open(out_file, mode='w',encoding='utf-8') as fp:
                for l in out:
                    fp.write(l+'\n')
            os.remove(cslfile)
            return 1
        raise CompileError(serr) from exc
    except Exception as err:
        with open(out_file, mode='w',encoding='utf-8') as fp:
            print(err, file=fp)
        raise err

# ===================================
# pytest code
# ===================================

TEST_RESULT_DIR = "test_results"
TEST_EXPECT_DIR = "test_expects"
CASL2_FILE_DIR  = "casl2"

test_data = sorted(glob.glob("../input*/*.mpl", recursive=True))

@pytest.mark.timeout(10)
@pytest.mark.parametrize(("mpl_file"), test_data)
def test_mpplc_run(mpl_file):
    """mpplcを実行する"""
    if not Path(TEST_RESULT_DIR).exists():
        os.mkdir(TEST_RESULT_DIR)
    if not Path(CASL2_FILE_DIR).exists():
        os.mkdir(CASL2_FILE_DIR)
    out_file = Path(TEST_RESULT_DIR).joinpath(Path(mpl_file).name + ".out")
    res = common_task(mpl_file, out_file)
    if res == 0:
        casl2file = Path(__file__).parent / Path(CASL2_FILE_DIR) / Path(Path(mpl_file).stem + ".csl")
        assert os.path.getsize(casl2file) > 0, "No CASL code generated."
    else:
        expect_file = Path(TEST_EXPECT_DIR).joinpath(Path(mpl_file).name + ".stderr")
        with open(out_file,encoding='utf-8') as ofp, open(expect_file,encoding='utf-8') as efp:
            try:
                o =  int(re.search(r'(\d+)',ofp.read()).group())
                e =  int(re.search(r'(\d+)',efp.read()).group())
                assert o - 1 <= e <= o + 1, "Line number of error message is different."
            except IndexError:
                assert False, "Line number does not appear in error message."
