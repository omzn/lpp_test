"""課題2用テスト"""
import os
import glob
import subprocess
import sys
import re
from pathlib import Path
import pytest

TARGET = "pp"
TARGETPATH = "/workspaces"

class ParseError(Exception):
    """構文エラーハンドラ"""

def command(cmd):
    """コマンドの実行"""
    try:
        result = subprocess.run(cmd, shell=True, check=False,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                universal_newlines=True)
#        for line in result.stdout.splitlines():
#            yield line
        return [result.stdout,result.stderr]
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
            raise ParseError(serr)
        for line in sout.splitlines():
            out.append(line)
        with open(out_file, mode='w', encoding='ascii') as fp:
            for l in out:
                fp.write(l+'\n')
        return 0
    except ParseError as exc:
        if re.search(r'sample0', mpl_file):
            for line in serr.splitlines():
                out.append(line)
            with open(out_file, mode='w', encoding='ascii') as fp:
                for l in out:
                    fp.write(l+'\n')
            return 1
        raise ParseError(serr) from exc
    except Exception as err:
        with open(out_file, mode='w', encoding='ascii') as fp:
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
    """準備したテストケースを全て実行する．"""
    # 期待された出力が得られるかを確認．ただし，厳密すぎるため，テストに通らないからといってダメというわけではない．
    if not Path(TEST_RESULT_DIR).exists():
        os.mkdir(TEST_RESULT_DIR)
    out_file = Path(TEST_RESULT_DIR).joinpath(Path(mpl_file).stem + ".out")
    res = common_task(mpl_file, out_file)
    # 正常終了した場合
    if res == 0:
        expect_file = Path(TEST_EXPECT_DIR).joinpath(Path(mpl_file).stem + ".stdout")
        with open(out_file,encoding='ascii') as ofp, open(expect_file,encoding='ascii') as efp:
            assert ofp.read() == efp.read()
    # 異常終了した場合
    else:
        # エラーの行番号が正しいかを確認
        expect_file = Path(TEST_EXPECT_DIR).joinpath(Path(mpl_file).stem + ".stderr")
        with open(out_file,encoding='ascii') as ofp, open(expect_file,encoding='ascii') as efp:
            o =  re.search(r'(\d+)',ofp.read()).group()
            e =  re.search(r'(\d+)',efp.read()).group()
            assert o == e

def test_no_param():
    """引数を付けずに実行するテスト"""
    exe = Path(TARGETPATH) / Path(TARGET)
    exec_res = command(f"{exe}")
    exec_res.pop(0)
    serr = exec_res.pop(0)
    assert serr

def test_not_valid_file():
    """存在しないファイルを引数にした場合のテスト"""
    exe = Path(TARGETPATH) / Path(TARGET)
    exec_res = command(f"{exe} hogehoge")
    exec_res.pop(0)
    serr = exec_res.pop(0)
    assert serr
