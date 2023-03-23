FROM gcc:latest
RUN apt update
RUN curl -sL https://deb.nodesource.com/setup_lts.x | bash - 
RUN apt install -y nodejs
RUN apt install -y gdb python3-pytest python3-pytest-timeout tmux vim less
RUN echo '#!/bin/sh\npython3 -m pytest $1 $2 $3 $4 $5 $6 $7 $8 $9' > /usr/local/bin/pytest && chmod +x /usr/local/bin/pytest
RUN cd / && git clone https://github.com/omzn/casljs && cd /casljs && npm ci
RUN cd / && git clone https://github.com/omzn/lpp_test 
RUN cd /lpp_test/docker && ./mk_motd.sh aqua.png
RUN echo '[ ! -z "$TERM" -a -r /etc/motd ] && cat /etc/motd && cat /etc/issue ' >> /etc/bash.bashrc
COPY bashrc /root/.bashrc
COPY issue /etc/issue