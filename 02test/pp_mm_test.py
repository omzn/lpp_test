"""課題2用メタモーフィックテスト"""
# 課題2では，1回実行した出力を再度入力として実行させても
# 全く同一の出力が得られるべき
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
        with open(out_file, mode='w', encoding=ascii) as fp:
            for l in out:
                fp.write(l+'\n')
        return 0
    except ParseError as exc:
        if re.search(r'sample0', mpl_file):
            for line in serr.splitlines():
                out.append(line)
            with open(out_file, mode='w', encoding=ascii) as fp:
                for l in out:
                    fp.write(l+'\n')
            return 1
        raise ParseError(serr) from exc
    except Exception as err:
        with open(out_file, mode='w', encoding=ascii) as fp:
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
@pytest.mark.parametrize(("mpl_file"), test_valid_data)
def test_idempotency(mpl_file):
    """メタモーフィックテストによって，冪等性を確認"""
    # 自分自身が生成したソースコードを読み込ませると同じファイルを生成するはず．
    if not Path(TEST_RESULT_DIR).exists():
        os.mkdir(TEST_RESULT_DIR)
    out_file = Path(TEST_RESULT_DIR).joinpath(Path(mpl_file).stem + ".out")
    # 1回目の実行
    res = common_task(mpl_file, out_file)
    if res == 0:
        out2_file = Path(TEST_RESULT_DIR).joinpath(Path(mpl_file).stem + ".out2")
       # 2回目の実行
        res1 = common_task(out_file, out2_file)
        if res1 == 0:
            with open(out2_file,encoding=ascii) as ofp2, open(out_file,encoding=ascii) as ofp1:
                assert ofp2.read() == ofp1.read()
        else:
            # 実行結果がエラーになるのであれば，それはダメ
            assert False
    else:
        # エラーになるわけがないテストデータのみを与えるので，ここは無条件にダメ
        assert False
