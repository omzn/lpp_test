"""課題4用コンパイル・実行テスト"""
import os
import re
import json
from pathlib import Path
import glob
import subprocess
import itertools
import pytest


TARGET = "mpplc"
TARGETPATH = "/workspaces"

class CompileError(Exception):
    """コンパイルエラーハンドラ"""

class Casl2AssembleError(Exception):
    """アセンブルエラーハンドラ"""

class Comet2ExecutionError(Exception):
    """エミュレータ実行エラーハンドラ"""

def command(cmd):
    """コマンドの実行"""
    try:
        result = subprocess.run(cmd, shell=True, check=False,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                universal_newlines=True)
        return [result.stdout,result.stderr]
    except subprocess.CalledProcessError as exc:
#        print(f"外部プログラムの実行に失敗しました [{cmd}]", file=sys.stderr)
        raise Comet2ExecutionError("Failed to execute COMET II") from exc

def interactive_command(cmd):
    """対話コマンド実行"""
    try:
        result = subprocess.run(cmd, shell=True, check=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                universal_newlines=True)
        for line in result.stdout.splitlines():
            yield line
    except subprocess.CalledProcessError as exc:
#        print(f'外部プログラムの実行に失敗しました [{cmd}]', file=sys.stderr)
        raise Comet2ExecutionError("Failed to interactively execute COMET II") from exc

def compile_task(mpl_file, out_file):
    """コンパイルタスク"""
    try:
        #mpplc = Path(__file__).parent.parent.joinpath("mpplc")
        exe = Path(TARGETPATH) / Path(TARGET)
        exec_res = command(f"{exe} {mpl_file}")
        cslfile = Path(mpl_file).stem + ".csl"
        if not Path(cslfile).exists():
            cslfile2 = Path(mpl_file).with_suffix(".csl")
            if not Path(cslfile2).exists():
                raise FileNotFoundError(f"Not found: {cslfile} or {cslfile2}")
            cslfile = cslfile2
        out = []
        exec_res.pop(0)
        serr = exec_res.pop(0)
        if serr:
            raise CompileError(serr)
        casl2file = Path(__file__).parent / Path(CASL2_FILE_DIR) / Path(cslfile).name
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
        raise exc
    except Exception as err:
        with open(out_file, mode='w',encoding='utf-8') as fp:
            print(err, file=fp)
        raise err

def execution_task(casl2_file, out_file):
    """c2c2実行タスク"""
    try:
#        c2c2 = Path(__file__).parent.parent.joinpath("c2c2.js")
        c2c2 = Path("/casljs") / Path("c2c2.js")
        assembler_text = interactive_command(f"node {c2c2} -n -c -a {casl2_file}")
        if "DEFINED SYMBOLS" not in assembler_text:
            raise Casl2AssembleError("Compile error")
        with open("input.json",encoding='utf-8') as fp:
            inp = json.load(fp)
        inputparams = ''
        if Path(casl2_file).name in inp.keys():
            inputparams = ' '.join(list(inp[Path(casl2_file).name]))
        terminal_text = interactive_command(f"node {c2c2} -n -q -r {casl2_file} {inputparams}")
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
CASL2_FILE_DIR  = "casl2"

test_data = sorted(glob.glob("/lpp_test/input*/*.mpl", recursive=True))

@pytest.mark.timeout(15)
@pytest.mark.parametrize(("mpl_file"), test_data)
def test_mpplc_run(mpl_file):
    """mpplcを実行する"""
    if not Path(TEST_RESULT_DIR).exists():
        os.mkdir(TEST_RESULT_DIR)
    if not Path(CASL2_FILE_DIR).exists():
        os.mkdir(CASL2_FILE_DIR)
    out_file = Path(TEST_RESULT_DIR).joinpath(Path(mpl_file).name + ".out")
    res = compile_task(mpl_file, out_file)
    if res == 0:
        casl2file = Path(__file__).parent/Path(CASL2_FILE_DIR)/Path(Path(mpl_file).stem + ".csl")
        assert os.path.getsize(casl2file) > 0, "CASL2ファイルが空です"
        out_file = Path(TEST_RESULT_DIR)/Path(Path(casl2file).name + ".out")
        execution_task(casl2file, out_file)
        expect_file = Path(TEST_EXPECT_DIR)/Path(Path(casl2file).name + ".out")
        with open(out_file,encoding='utf-8') as ofp, open(expect_file,encoding='utf-8') as efp:
            out_cont = ofp.read().splitlines()
            est_cont = efp.read().splitlines()
            for out_line, est_line in itertools.zip_longest(out_cont, est_cont, fillvalue=""):
                assert out_line == est_line, "正常な出力と異なります"
    else:
        expect_file = Path(TEST_EXPECT_DIR)/Path(Path(mpl_file).name + ".stderr")
        with open(out_file,encoding='utf-8') as ofp, open(expect_file,encoding='utf-8') as efp:
            try:
                o =  int(re.search(r'(\d+)',ofp.read()).group())
                e =  int(re.search(r'(\d+)',efp.read()).group())
                assert o - 1 <= e <= o + 1, "エラーが出ている行番号が異なります"
            except IndexError:
                assert False, "エラーメッセージ中に行番号がありません"
