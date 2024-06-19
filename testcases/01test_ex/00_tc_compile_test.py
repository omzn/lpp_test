"""課題1拡張用テスト"""
import os
import sys
import re
from pathlib import Path
import glob
import subprocess
#import pytest

TARGET = "tc"
TARGETPATH = "/workspaces"

class ScanError(Exception):
    """字句解析エラーハンドラ"""

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
#        tc = Path(__file__).parent.parent.joinpath("tc")
        exe = Path(TARGETPATH) / Path(TARGET)
        exec_res = command(f"{exe} {mpl_file}")
        out = []
        sout = exec_res.pop(0)
        serr = exec_res.pop(0)
        if serr:
            raise ScanError(serr)
        for line in sout.splitlines():
            if re.search(r'\s*"\s*\S*\s*"\s*\d+\s*',line) or re.search(r'\s*"\s*\S*\s*"\s*"\s*\S*\s*"\s*\d+\s*',line):
                formatted = re.sub(r'\s+', r'', line)
                out.append(formatted)
        out.sort()
        with open(out_file, mode='w',encoding='utf-8') as fp:
            for l in out:
                fp.write(l+'\n')
        return 0
    except ScanError as exc:
        if re.search(r'sample0', mpl_file):
            for line in serr.splitlines():
                out.append(line)
            with open(out_file, mode='w',encoding='utf-8') as fp:
                for l in out:
                    fp.write(l+'\n')
            return 1
        raise ScanError(serr) from exc
    except Exception as err:
        with open(out_file, mode='w',encoding='utf-8') as fp:
            print(err, file=fp)
        raise err

# ===================================
# pytest code
# ===================================

TEST_RESULT_DIR = "test_results"
TEST_EXPECT_DIR = "test_expects"

test_data = sorted(glob.glob("../input01/*.mpl", recursive=True))

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
