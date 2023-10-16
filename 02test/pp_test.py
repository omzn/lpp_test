import os
import glob
import json
import subprocess
import pytest
import sys
import re
from pathlib import Path

target = "pp"
targetpath = "/workspace"

class ParseError(Exception):
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
        exec = Path(targetpath).joinpath(target)
        exec_res = command("{} {}".format(exec,mpl_file))
        out = []
        sout = exec_res.pop(0)
        serr = exec_res.pop(0)
        if serr:
            raise ParseError(serr)
        for line in sout.splitlines():
            out.append(line)
        with open(out_file, mode='w') as fp:
            for l in out:
                fp.write(l+'\n')
        return 0
    except ParseError:
        if re.search(r'sample0', mpl_file):
            for line in serr.splitlines():
                out.append(line)
            with open(out_file, mode='w') as fp:
                for l in out:
                    fp.write(l+'\n')
            return 1
        else:
            raise ParseError(serr)
    except Exception as err:
        with open(out_file, mode='w') as fp:
            print(err, file=fp)
        raise err

# ===================================
# pytest code
# ===================================

TEST_RESULT_DIR = "test_results"
TEST_EXPECT_DIR = "test_expects"

# 全てのテストデータ
test_data = sorted(glob.glob("../input0[12]/*.mpl", recursive=True))
# エラーが出ないことが期待されるデータのみ
test_valid_data = sorted(glob.glob("../input0[12]/sample[!0]*.mpl", recursive=True))

@pytest.mark.timeout(10)
@pytest.mark.parametrize(("mpl_file"), test_data)
def test_run(mpl_file):
    # 期待された出力が得られるかを確認．ただし，厳密すぎるため，テストに通らないからといってダメというわけではない．
    if not Path(TEST_RESULT_DIR).exists():
        os.mkdir(TEST_RESULT_DIR)
    out_file = Path(TEST_RESULT_DIR).joinpath(Path(mpl_file).stem + ".out")
    res = common_task(mpl_file, out_file)
    if res == 0:
        expect_file = Path(TEST_EXPECT_DIR).joinpath(Path(mpl_file).stem + ".stdout")
        with open(out_file) as ofp, open(expect_file) as efp:
            assert ofp.read() == efp.read()
    else:
        # エラーの行番号が正しいかを確認
        expect_file = Path(TEST_EXPECT_DIR).joinpath(Path(mpl_file).stem + ".stderr")
        with open(out_file) as ofp, open(expect_file) as efp:
            o =  re.search(r'(\d+)',ofp.read()).group()
            e =  re.search(r'(\d+)',efp.read()).group()
            assert o == e

def test_no_param():
    exec = Path(targetpath).joinpath(target)
    exec_res = command("{}".format(exec))
    sout = exec_res.pop(0)
    serr = exec_res.pop(0)
    assert serr 

def test_not_valid_file():
    exec = Path(targetpath).joinpath(target)
    exec_res = command("{} hogehoge".format(exec))
    sout = exec_res.pop(0)
    serr = exec_res.pop(0)
    assert serr 


