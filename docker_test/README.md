# Dockerfile for KIT-LPP

* gcc:11.4.0

# How to build

* https://dev.classmethod.jp/articles/docker-multi-architecture-image-build/
* https://selkit.esa.io/posts/917

```
$ docker buildx build --platform linux/amd64,linux/arm64 -t omzn/kit-lpp:test --push .  
```

採点用にpytest実行専用のイメージを作りました．
`omzn/lpp-kit:test` になります．

課題1のディレクトリに移動して，
```
docker run --rm -it -v $PWD:/workspaces -w /workspaces omzn/kit-lpp:test 01test
```
とすると，勝手にビルドしてから課題1のテストが実行されます．
引数でテストのディレクトリとpytestへの引数を記述できます．
```
docker run --rm -it -v $PWD:/workspaces -w /workspaces omzn/kit-lpp:test 02test -vv
```
とか，
```
docker run --rm -it -v $PWD:/workspaces -w /workspaces omzn/kit-lpp:test 02test -vv -k sample11pp.mpl
```
のように指定できますので，aliasなどに登録しておくと便利です．
```alias lpptest='docker run --rm -it -v $PWD:/workspaces -w /workspaces omzn/kit-lpp:test'```
これで，
```
lpptest 01test
lpptest 02test -vv -k sample11pp.mpl
```
のように記述できます．