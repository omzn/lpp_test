"""課題4用C2C2実行テスト"""
import os
import glob
import json
import subprocess
import sys
from pathlib import Path
import pytest

class Casl2AssembleError(Exception):
    """アセンブルエラーハンドラ"""

def command(cmd):
    """コマンド実行"""
    try:
        result = subprocess.run(cmd, shell=True, check=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                universal_newlines=True)
        for line in result.stdout.splitlines():
            yield line
    except subprocess.CalledProcessError:
        print(f'外部プログラムの実行に失敗しました [{cmd}]', file=sys.stderr)
        sys.exit(1)

def common_task(casl2_file, out_file):
    """共通実行タスク"""
    try:
#        c2c2 = Path(__file__).parent.parent.joinpath("c2c2.js")
        c2c2 = Path("/casljs") / Path("c2c2.js")
        assembler_text = command(f"node {c2c2} -n -c -a {casl2_file}")
        if "DEFINED SYMBOLS" not in assembler_text:
            raise Casl2AssembleError("Failed to compile")
        with open("input.json",encoding='utf-8') as fp:
            inp = json.load(fp)
        inputparams = ''
        if Path(casl2_file).name in inp.keys():
            inputparams = ' '.join(list(inp[Path(casl2_file).name]))
        terminal_text = command(f"node {c2c2} -n -q -r {casl2_file} {inputparams}")
        with open(out_file, mode='w',encoding='utf-8') as fp:
            for line in terminal_text:
                fp.write(line + '\n')
    except Casl2AssembleError as exc:
        with open(out_file, mode='w',encoding='utf-8') as fp:
            fp.write("============ASSEMBLE ERROR==============\n")
            for line in assembler_text:
                fp.write(line + '\n')
        raise Casl2AssembleError("Assemble Error") from exc
    except Exception as err:
        with open(out_file, mode='w',encoding='utf-8') as fp:
            print(err, file=fp)
        raise err

# ===================================
# pytest code
# ===================================

TEST_RESULT_DIR = "test_results"
TEST_EXPECT_DIR = "test_expects"

test_data = sorted(glob.glob("casl2/sample[!0]*.csl", recursive=True))

@pytest.mark.timeout(10)
@pytest.mark.parametrize(("casl2_file"), test_data)
def test_c2c2_run(casl2_file):
    """c2c2実行"""
    if not Path(TEST_RESULT_DIR).exists():
        os.mkdir(TEST_RESULT_DIR)
    out_file = Path(TEST_RESULT_DIR).joinpath(Path(casl2_file).name + ".out")
    common_task(casl2_file, out_file)
    expect_file = Path(TEST_EXPECT_DIR).joinpath(Path(casl2_file).name + ".out")
    with open(out_file,encoding='utf-8') as ofp, open(expect_file,encoding='utf-8') as efp:
        out_cont = ofp.read().splitlines()
        est_cont = efp.read().splitlines()
        for i, out_line in enumerate(out_cont):
            assert out_line == est_cont[i], "Line does not match."