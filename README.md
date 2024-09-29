# lpp/test

KIT言語処理プログラミング課題におけるテスト環境
[`pipx`](https://pipx.pypa.io/stable/installation/)によりインストールされた`lpptest`コマンドを用いてテストを行う．
`lpptest`コマンドは自動的にDockerを用いたテスト用環境を用意し，テストを行うことができる．

## インストール方法

[`pipx`](https://pipx.pypa.io/stable/installation/)に従う．
その後、以下のコマンドを実行する．

```bash
pipx install git+https://github.com/f0reachARR/lpp_test --force
```

これにより，`lpptest`コマンドがインストールされる．
インストール後は，ソースコードのあるディレクトリで`lpptest`コマンドを実行することでテストを行うことができる．

## テストの実行

### 課題1の場合

```bash
# テストの実行
lpptest 01test
```

* 00_tc_compile_test.py - コンパイルできるか，引数の有無での動作，無効なファイル名を与えた動作
* 01_tc_run_test.py - 空白を取り除いた出力を辞書順にソートしたものを比較する．

### 課題1拡張の場合

```bash
# テストの実行
lpptest 01test_ex
```

* 00_tc_compile_test.py - コンパイルできるか，引数の有無での動作，無効なファイル名を与えた動作
* 01_tc_run_test.py - 空白を取り除いた出力を辞書順にソートしたものを比較する．

### 課題2の場合

```bash
# テストの実行
lpptest 02test
```

* 00_pp_compile_test.py - コンパイルできるか，引数の有無での動作，無効なファイル名を与えた動作
* 01_pp_run_test.py - 与えられた仕様通りに出力できているかを見る．
* 02_pp_mm_test.py - 一度出力した内容を再度ppに通して，エラーが出ないかを見る．

### 課題3の場合

```bash
# テストの実行
lpptest 03test
```

* 00_cr_compile_test.py - コンパイルできるか，引数の有無での動作，無効なファイル名を与えた動作
* 01_cr_run_test.py - 仕様の順に出力した表から空白文字をすべて削除したものを比較する

### 課題4の場合

```bash
# テストの実行
lpptest 04test
```

* 00_mpplc_compile_test.py - コンパイルできるか，引数の有無での動作，無効なファイル名を与えた動作
* 01_mpplc_c2c2_run_test.py - コンパイルしたアセンブリプログラムがc2c2で実行できるかを見る．

## Docker内部のディレクトリ配置

各テストはDocker内部に置かれるため、普段意識する必要はない．
なお、このレポジトリにおいては`lpp_collector/testcases`に配置されている．

* /lpp/test   : テストケースが置かれているフォルダ
* /lpp/test/input0[123] : サンプルmplファイルが置いてある場所
  * `sample0*.mpl` は，実行時にエラーが出力されることが期待されている
* /lpp/test/0[1234]test : 各課題に対するテスト
* /lpp/test/0[1234]test/test_expects : 各課題に対するテストの期待される出力(オラクル)
  * 以下のテストでは，エラーが出力される想定のものは，エラーの出た行番号が同じであればPASSとなる．
* /lpp/test/coverage : C0カバレッジを上げていくためのテストケース(上記テストでは使わない)
