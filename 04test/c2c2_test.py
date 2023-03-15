import os
import glob
import json
import subprocess
import pytest
import sys
from pathlib import Path

class Casl2AssembleError(Exception):
    pass

def command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, check=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                universal_newlines=True)
        for line in result.stdout.splitlines():
            yield line
    except subprocess.CalledProcessError:
        print('外部プログラムの実行に失敗しました [' + cmd + ']', file=sys.stderr)
        sys.exit(1)

def common_task(casl2_file, out_file):
    try:
        c2c2 = Path(__file__).parent.parent.joinpath("c2c2.js")
        assembler_text = command("node {} -n -c -a {}".format(c2c2,casl2_file))
        if not "DEFINED SYMBOLS" in assembler_text:
            raise Casl2AssembleError
        with open("input.json") as fp:
            input = json.load(fp)
        inputparams = ''
        if Path(casl2_file).name in input.keys():
            inputparams = ' '.join([i for i in input[Path(casl2_file).name]])
        terminal_text = command("node {} -n -q -r {} {}".format(c2c2,casl2_file,inputparams))
        with open(out_file, mode='w') as fp:
            for line in terminal_text:
                fp.write(line + '\n')
    except Casl2AssembleError:
        with open(out_file, mode='w') as fp:
            fp.write("============ASSEMBLE ERROR==============\n")
            for line in assembler_text:
                fp.write(line + '\n')
        raise Casl2AssembleError
    except Exception as err:
        with open(out_file, mode='w') as fp:
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
    if not Path(TEST_RESULT_DIR).exists():
        os.mkdir(TEST_RESULT_DIR)
    out_file = Path(TEST_RESULT_DIR).joinpath(Path(casl2_file).name + ".out")
    common_task(casl2_file, out_file)
    expect_file = Path(TEST_EXPECT_DIR).joinpath(Path(casl2_file).name + ".out")
    with open(out_file) as ofp, open(expect_file) as efp:
        assert ofp.read() == efp.read()
