# 課題3 クロスリファレンス テスト

## 出力仕様

* 以下の形式のクロスリファレンス表を「標準出力(stdout)」に書き出す．
* エラーが発生した場合は，表を出力しない．また「標準エラー出力(stderr)」にエラーの内容を出力する．
```
Name|Type|Define|Reference
aaa|integer|2|3
bbb|procedure|4|10,11
ccc:bbb|boolean|5|7,8
```
* 1行目は必ずヘッダ行とする．
* カラムは`|`で区切る．
* 局所変数と仮引数は`変数名:手絵続き名`の形式で名前を書く．
* 配列の型名は`array[数字] of 基本型`と記載する．
* 参照行(reference)が複数ある場合は`,`で区切る．
* 各項目内を見やすくするために適宜空白を加えても構わない．

### 例
```
Name                | Type                     | Define | References          
UnusedArrayForTest  | array[  200] of char     | 10     | 
a:abs               | integer                  | 26     | 28,28,28
a:gcm               | integer                  | 30     | 33,35
a:gcmlcm            | integer                  | 14     | 16,19,19,20,23
```

## テスト実行

```
pytest -v
```
