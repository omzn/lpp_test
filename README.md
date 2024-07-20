# lpp/test
KIT言語処理プログラミング課題におけるテスト環境

Dockerイメージの中に展開して利用することを想定

## ディレクトリ配置

* /workspaces : 編集中のCのソースが置いてある場所
* /lpp/test   : このリポジトリ
* /lpp/test/input0[123] : サンプルmplファイルが置いてある場所
  * `sample0*.mpl` は，実行時にエラーが出力されることが期待されている
* /lpp/test/0[1234]test : 各課題に対するテスト
* /lpp/test/0[1234]test/test_expects : 各課題に対するテストの期待される出力(オラクル)
  * 以下のテストでは，エラーが出力される想定のものは，エラーの出た行番号が同じであればPASSとなる．
* /lpp/test/coverage : C0カバレッジを上げていくためのテストケース(上記テストでは使わない)

### 課題1の場合

```bash
# テストの実行
cd /lpp/test/01test; pytest -vv
```
* 00_tc_compile_test.py - コンパイルできるか，引数の有無での動作，無効なファイル名を与えた動作
* 01_tc_run_test.py - 空白を取り除いた出力を辞書順にソートしたものを比較する．

### 課題1拡張の場合

```bash
# テストの実行
cd /lpp/test/01test_ex; pytest -vv
```
* 00_tc_compile_test.py - コンパイルできるか，引数の有無での動作，無効なファイル名を与えた動作
* 01_tc_run_test.py - 空白を取り除いた出力を辞書順にソートしたものを比較する．

### 課題2の場合

```bash
# テストの実行
cd /lpp/test/02test; pytest -vv
```
* 00_pp_compile_test.py - コンパイルできるか，引数の有無での動作，無効なファイル名を与えた動作
* 01_pp_run_test.py - 与えられた仕様通りに出力できているかを見る．
* 02_pp_mm_test.py - 一度出力した内容を再度ppに通して，エラーが出ないかを見る．

### 課題3の場合

```bash
# テストの実行
cd /lpp/test/03test; pytest -vv
```
* 00_cr_compile_test.py - コンパイルできるか，引数の有無での動作，無効なファイル名を与えた動作
* 01_cr_run_test.py - 仕様の順に出力した表から空白文字をすべて削除したものを比較する

### 課題4の場合

```bash
# テストの実行
cd /lpp/test/04test && pytest -vv mpplc_test.py
cd /lpp/test/04test && pytest -vv c2c2_test.py

```
* 00_mpplc_compile_test.py - コンパイルできるか，引数の有無での動作，無効なファイル名を与えた動作
* 01_mpplc_c2c2_run_test.py - コンパイルしたアセンブリプログラムがc2c2で実行できるかを見る．
