import os
import glob
import json
import subprocess
import pytest
import sys
import re
from pathlib import Path

class MpplCompileError(Exception):
    pass

def command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, check=False,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                universal_newlines=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError:
        print('外部プログラムの実行に失敗しました [' + cmd + ']', file=sys.stderr)
        sys.exit(1)

def common_task(mpl_file, out_file):
    try:
        mpplc = Path(__file__).parent.parent.joinpath("mpplc")
        cslfile = Path(mpl_file).stem + ".csl"
        compiler_text = command("{} {}".format(mpplc,mpl_file))
        if compiler_text:
            raise MpplCompileError
        casl2file = Path(__file__).parent.joinpath(CASL2_FILE_DIR).joinpath(cslfile)
        os.rename(cslfile, casl2file)
        return 1
    except MpplCompileError:
        with open(out_file, mode='w') as fp:
            fp.write("============COMPILE ERROR==============\n")
            fp.write(compiler_text)
        if re.match(r'sample0', cslfile):
            os.remove(cslfile)
            return 1
        else:
            raise MpplCompileError
    except Exception as err:
        with open(out_file, mode='w') as fp:
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
def test_mppl_run(mpl_file):
    if not Path(TEST_RESULT_DIR).exists():
        os.mkdir(TEST_RESULT_DIR)
    if not Path(CASL2_FILE_DIR).exists():
        os.mkdir(CASL2_FILE_DIR)
    out_file = Path(TEST_RESULT_DIR).joinpath(Path(mpl_file).name + ".out")
    res = common_task(mpl_file, out_file)
    assert res == 1
