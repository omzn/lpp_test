# Dockerfile for KIT-LPP

* gcc:11.4.0

# How to build

* https://dev.classmethod.jp/articles/docker-multi-architecture-image-build/
* https://selkit.esa.io/posts/917

```
$ docker buildx create --use --name aquatan
$ docker buildx use aquatan
$ docker buildx inspect --bootstrap
$ docker buildx build --platform linux/amd64,linux/arm64 -t omzn/kit-lpp:v2 --push .  
```

docker login se.is.kit.ac.jp
docker tag omzn/kit-lpp:v2 se.is.kit.ac.jp/o_mizuno/kit-lpp:v2
docker push se.is.kit.ac.jp/o_mizuno/kit-lpp:v2
