"""課題4用コンパイルテスト"""
import os
import sys
import re
from pathlib import Path
import glob
import subprocess
import shutil
#import pytest

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
        cslfile = Path(Path(mpl_file).stem + ".csl")
        if not cslfile.exists():
            cslfile = Path(mpl_file).parent / Path(Path(mpl_file).stem + ".csl")
            if not cslfile.exists():
                raise CompileError(".csl file not found.")
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
    assert not serr, "mpplcのコンパイルに失敗しました"

def test_no_param():
    """引数を付けずに実行するテスト"""
    exe = Path(TARGETPATH) / Path(TARGET)
    exec_res = command(f"{exe}")
    exec_res.pop(0)
    serr = exec_res.pop(0)
    assert serr, "パラーメータを与えない時にエラーがでません"

def test_not_valid_file():
    """存在しないファイルを引数にした場合のテスト"""
    exe = Path(TARGETPATH) / Path(TARGET)
    exec_res = command(f"{exe} hogehoge")
    exec_res.pop(0)
    serr = exec_res.pop(0)
    assert serr, "存在しないファイル名を与えた時にエラーがでません"

def test_absolute_path_file():
    """絶対パスでファイルを指定した場合のテスト"""
    shutil.copy('../input01/sample12.mpl','/tmp/sample12.mpl')
    exe = Path(TARGETPATH) / Path(TARGET)
    command(f"{exe} /tmp/sample12.mpl")
    if os.path.isfile("./sample12.csl"):
        assert True
    elif os.path.isfile("/tmp/sample12.csl"):
        assert True
    else:
        assert False, "絶対パスでのファイル名指定ができていません"

def test_relative_path_file():
    """相対パスでファイルを指定した場合のテスト"""
    exe = Path(TARGETPATH) / Path(TARGET)
    command(f"{exe} ../input01/sample12.mpl")
    if os.path.isfile("./sample12.csl"):
        assert True
    elif os.path.isfile("../input01/sample12.csl"):
        assert True
    else:
        assert False, "相対パスでのファイル名指定ができていません"
