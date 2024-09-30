# hadolint global ignore=DL3006,DL3008,DL3013
FROM node:20-bookworm-slim AS build_env

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    imagemagick wget ca-certificates \
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

# Starship
WORKDIR /starship
RUN wget https://github.com/starship/starship/releases/download/v1.19.0/starship-x86_64-unknown-linux-gnu.tar.gz \
    && tar xvf starship-x86_64-unknown-linux-gnu.tar.gz

################################################################################
FROM python:3.10-slim AS collector
WORKDIR /app
ARG LPP_PYTHON_BASE=.

RUN pip install poetry==1.7 \
    && poetry config virtualenvs.create false

COPY ${LPP_PYTHON_BASE}/pyproject.toml ${LPP_PYTHON_BASE}/poetry.lock* ./
RUN poetry install

COPY ${LPP_PYTHON_BASE}/ ./

RUN poetry build -f wheel

################################################################################
# 演習室は Ubuntu 22.04 なので
FROM ubuntu:22.04 AS user_env

# install essential packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    ca-certificates curl gnupg \
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

# install essential packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    ca-certificates curl gnupg gdb \
    python3-pip tmux \
    vim less cmake g++ bash-completion whiptail \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /lpp/test

# Copy shell related files
COPY --from=build_env /etc/motd /etc/motd
COPY --from=build_env /starship/starship /usr/local/bin/starship
COPY ./docker/pytest /usr/local/bin/pytest
COPY ./docker/bashrc /root/.bashrc
COPY ./docker/issue /etc/issue
# COPY ./docker/lpptest /usr/local/bin/lpptest
COPY ./docker/starship.toml /root/.config/starship.toml
# COPY ./docker/lpptest_completion /etc/bash_completion.d/lpptest_completion

RUN touch /.dockerenv

COPY --from=build_env /casljs /casljs

RUN echo '[ ! -z "$TERM" -a -r /etc/motd ] && cat /etc/motd && cat /etc/issue ' >> /etc/bash.bashrc

COPY --from=collector /app/dist/*.whl /tmp/

RUN pip install /tmp/*.whl \
    && rm -rf /tmp/*.whl \
    && python3 -c 'from lpp_collector.mklink import main; main()'

VOLUME [ "/workspaces" ]
WORKDIR /workspaces