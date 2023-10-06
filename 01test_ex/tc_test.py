import os
import glob
import json
import subprocess
import pytest
import sys
import re
from pathlib import Path

target = "tc"
targetPath = "/workspaces"

class ScanError(Exception):
    pass

def command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, check=False,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                universal_newlines=True)
#        for line in result.stdout.splitlines():
#            yield line
        return [result.stdout,result.stderr]
    except subprocess.CalledProcessError:
        print('外部プログラムの実行に失敗しました [' + cmd + ']', file=sys.stderr)
        sys.exit(1)

def common_task(mpl_file, out_file):
    try:
#        tc = Path(__file__).parent.parent.joinpath("tc")
        exec = Path(targetPath).joinpath(target)
        exec_res = command(f"{exec} {mpl_file}")
        out = []
        sout = exec_res.pop(0)
        serr = exec_res.pop(0)
        if len(serr) > 0:
            print(f'err message [{serr}]', file=sys.stderr)
            raise ScanError
        for line in sout.splitlines():
            formatted = re.sub(r'\s+', r'\t', line)
            formatted = re.sub(r'^\t', r'', formatted)
            out.append(formatted + '\n')
        out.sort()
        with open(out_file, mode='w') as fp:
            for l in out:
                fp.write(l)
        return 0
    except ScanError:
        if re.search(r'sample0', mpl_file):
            for line in serr.splitlines():
                out.append(line)
            with open(out_file, mode='w') as fp:
                for l in out:
                    fp.write(l+'\n')
            return 1
        else:
            raise ScanError        
    except Exception as err:
        with open(out_file, mode='w') as fp:
            print(err, file=fp)
        raise err

# ===================================
# pytest code
# ===================================

TEST_RESULT_DIR = "test_results"
TEST_EXPECT_DIR = "test_expects"

test_data = sorted(glob.glob("../input01/*.mpl", recursive=True))

@pytest.mark.timeout(10)
@pytest.mark.parametrize(("mpl_file"), test_data)
def test_run(mpl_file):
    if not Path(TEST_RESULT_DIR).exists():
        os.mkdir(TEST_RESULT_DIR)
    out_file = Path(TEST_RESULT_DIR).joinpath(Path(mpl_file).stem + ".out")
    res = common_task(mpl_file, out_file)
    if res == 0:
        expect_file = Path(TEST_EXPECT_DIR).joinpath(Path(mpl_file).stem + ".stdout")
        with open(out_file) as ofp, open(expect_file) as efp:
            assert ofp.read() == efp.read()
    else:
        with open(out_file) as ofp:
            assert not ofp.read() == ''

def test_no_param():
    exec = Path(targetPath).joinpath(target)
    exec_res = command("{}".format(exec))
    sout = exec_res.pop(0)
    serr = exec_res.pop(0)
    assert serr

def test_not_valid_file():
    exec = Path(targetPath).joinpath(target)
    exec_res = command("{} hogehoge".format(exec))
    sout = exec_res.pop(0)
    serr = exec_res.pop(0)
    assert serr
