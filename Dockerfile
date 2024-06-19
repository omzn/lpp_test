# hadolint global ignore=DL3006,DL3008,DL3013
FROM node:20-bookworm-slim AS build_env

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    imagemagick \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Preparation for casljs
WORKDIR /casljs
COPY casljs/package.json casljs/package-lock.json ./
RUN npm ci
COPY casljs/ ./

# Preparation for motd
WORKDIR /motd
COPY docker/mk_motd.sh docker/aqua.png ./
RUN bash mk_motd.sh aqua.png

# 演習室は Ubuntu 22.04 なので
FROM ubuntu:22.04 AS user_env
# install essential packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    ca-certificates curl gnupg gdb \
    python3-pip python3-pytest \
    python3-pytest-timeout tmux \
    vim less cmake g++ \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# install latest (20.x) node.js
RUN curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/nodesource.gpg \
    && echo "deb [signed-by=/etc/apt/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" > /etc/apt/sources.list.d/nodesource.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /usr/lib/node_modules/npm/ /usr/bin/npm

WORKDIR /lpp_test

# Copy shell related files
COPY --from=build_env /etc/motd /etc/motd
COPY ./docker/pytest /usr/local/bin/pytest
COPY ./docker/bashrc /root/.bashrc
COPY ./docker/issue /etc/issue
COPY ./docker/lpptest /usr/local/bin/lpptest

COPY --from=build_env /casljs /casljs

# Copy testcases
COPY ./testcases/ ./

RUN echo '[ ! -z "$TERM" -a -r /etc/motd ] && cat /etc/motd && cat /etc/issue ' >> /etc/bash.bashrc
