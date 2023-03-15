import os
import glob
import json
import subprocess
import pytest
import sys
import re
from pathlib import Path

def command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, check=False,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                universal_newlines=True)
        for line in result.stdout.splitlines():
            yield line
    except subprocess.CalledProcessError:
        print('外部プログラムの実行に失敗しました [' + cmd + ']', file=sys.stderr)
        sys.exit(1)

def common_task(mpl_file, out_file):
    try:
        tc = Path(__file__).parent.parent.joinpath("tc")
        compiler_text = command("{} {}".format(tc,mpl_file))
        out = []
        for line in compiler_text:
            out.append(line)
        out.sort()
        with open(out_file, mode='w') as fp:
            for l in out:
                fp.write(re.sub(r'\s*"\s*(\S*)\s*"\s*(\d+)\s*',r'"\1"\t\2\n',l))
    except Exception as err:
        with open(out_file, mode='w') as fp:
            print(err, file=fp)
        raise err

# ===================================
# pytest code
# ===================================

TEST_RESULT_DIR = "test_results"
TEST_EXPECT_DIR = "test_expects"

test_data = sorted(glob.glob("../input*/*.mpl", recursive=True))

@pytest.mark.timeout(10)
@pytest.mark.parametrize(("mpl_file"), test_data)
def test_mppl_run(mpl_file):
    if not Path(TEST_RESULT_DIR).exists():
        os.mkdir(TEST_RESULT_DIR)
    out_file = Path(TEST_RESULT_DIR).joinpath(Path(mpl_file).stem + ".out")
    common_task(mpl_file, out_file)
    expect_file = Path(TEST_EXPECT_DIR).joinpath(Path(mpl_file).stem + ".txt")
    with open(out_file) as ofp, open(expect_file) as efp:
        assert ofp.read() == efp.read()
