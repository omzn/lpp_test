# lpp_test
KIT言語処理プログラミング課題におけるテスト環境

Dockerイメージの中に展開して利用することを想定

## ディレクトリ配置

* /workspaces : 編集中のCのソースが置いてある場所
* /lpp_test   : このリポジトリ
* /lpp_test/input0[123] : サンプルmplファイルが置いてある場所
  * `sample0*.mpl` は，実行時にエラーが出力されることが期待されている
* /lpp_test/0[1234]test : 各課題に対するテスト
* /lpp_test/0[1234]test/test_expects : 各課題に対するテストの期待される出力(オラクル)
  * 以下のテストでは，エラーが出力される想定のものは，エラーの出た行番号が同じであればPASSとなる．

### 課題1の場合

```bash
# プログラムのビルド
gcc *.c -o tc
# テストの実行
cd /lpp_test/01test; pytest -vv
```

* 空白を取り除いた出力を辞書順にソートしたものを比較する．

### 課題1拡張の場合

```bash
# プログラムのビルド
gcc *.c -o tc
# テストの実行
cd /lpp_test/01test_ex; pytest -vv
```
* 空白を取り除いた出力を辞書順にソートしたものを比較する．

### 課題2の場合

```bash
# プログラムのビルド
gcc *.c -o pp
# テストの実行
cd /lpp_test/02test; pytest -vv
```
* 出力をお手本と比較する．
 * 課題2のテストは厳密すぎるので，もっと緩和できてもよい．
* 別の考え方として，一旦ppを通したものを再度ppに通し，冪等性を見ることもできる．

### 課題3の場合

```bash
# プログラムのビルド
gcc *.c -o cr
# テストの実行
cd /lpp_test/03test; pytest -vv
```
* 仕様の順に出力した表から空白文字をすべて削除したものを比較する

### 課題4の場合

```bash
# プログラムのビルド
gcc *.c -o mpplc
# テストの実行
cd /lpp_test/04test && pytest -vv mpplc_test.py
cd /lpp_test/04test && pytest -vv c2c2_test.py

```
* mpplcですべてのサンプルをコンパイルできるかを見る．(mpplc_test.py)
* c2c2でコンパイルしたアセンブリプログラムが実行できるかを見る．(c2c2_test.py)
