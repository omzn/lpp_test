# Configuration

import os
import lpp_collector

LPP_BASE_URL = (
    os.environ["LPP_BASE_URL"]
    if "LPP_BASE_URL" in os.environ
    else "https://se.is.kit.ac.jp/lpp_api/"
)

LPP_CONSENT_TEXT = """
(この画面は上下キーでスクロールできます)
この画面は、言語処理プログラミングにおいて、ソフトウェア工学研究室が行う研究のための同意書です。
以下の内容をよく読み、同意する場合は「同意する」を選択してください。

同意した場合、今後、課題で作成するソフトウェアをpytestによりテストする際、以下の項目を自動的に収集します。

- テストの実行結果
- ソフトウェアのソースコードとテストスイート
- 実行した環境の情報
- テストを行った日時

なお、これらの情報は、研究目的以外には使用せず、成績評価には一切影響しません。

また、同意する場合、次の画面でフォームへのURLが表示されます。
このフォームへの回答をもって、同意が完了します。

研究の同意を取り消す場合、同意するときと同様のコマンドを実行してください。
"""

LPP_AFTER_CONSENT_TEXT = """
ソフトウェア工学研究室 「言語処理プログラミング」における開発手法の分析に関する研究 への同意ありがとうございます。
以下のURLにアクセスして、フォームに回答してください。
{form_url}
"""

LPP_REVOKE_CONSENT_TEXT = """
ソフトウェア工学研究室 「言語処理プログラミング」における開発手法の分析に関する研究 への同意を取り消しますか？

同意を取り消した場合、今後、情報の収集は行われません。
"""

LPP_SOURCE_FILES = ["*.c", "*.h", "CMakelists.txt", "Makefile"]

TEST_BASE_DIR = os.path.join(os.path.dirname(lpp_collector.__file__), "testcases")

# Docker environment
IS_DOCKER_ENV = os.path.exists("/.dockerenv")
DOCKER_IMAGE = (
    os.environ["DOCKER_IMAGE"]
    if "DOCKER_IMAGE" in os.environ
    else "ghcr.io/f0reacharr/lpp_test:latest"
)


def derive_data_dir():
    if "LPP_DATA_DIR" in os.environ:
        return os.environ["LPP_DATA_DIR"]

    if IS_DOCKER_ENV:
        return "/lpp/data"
    else:
        return os.path.expanduser("~/.config/lpp")


LPP_DATA_DIR = derive_data_dir()

LPP_UPDATE_MARKER = os.path.join(LPP_DATA_DIR, ".update_marker")
LPP_UPDATE_INTERVAL = 60 * 60 * 24  # 1 day


def derive_target_path():
    if "LPP_TARGET_PATH" in os.environ:
        return os.environ["LPP_TARGET_PATH"]

    if IS_DOCKER_ENV:
        return "/workspaces"
    else:
        return os.getcwd()


TARGETPATH = derive_target_path()
