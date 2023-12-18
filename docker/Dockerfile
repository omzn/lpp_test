# based on gcc 11.4.0 (same as that in exercise room in 2023)
FROM gcc:11.4.0
# install essential packages
RUN apt update
RUN apt-get install -y ca-certificates curl gnupg gdb python3-pip python3-pytest python3-pytest-timeout tmux vim less cmake
# install latest (20.x) node.js
RUN curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/nodesource.gpg
RUN echo "deb [signed-by=/etc/apt/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" > /etc/apt/sources.list.d/nodesource.list
RUN apt update && apt install -y nodejs
# obsolute style script for node.js
#RUN curl -sL https://deb.nodesource.com/setup_lts.x | bash - 
# deploy casl/comet
RUN cd / && git clone https://github.com/omzn/casljs && cd /casljs && npm ci
# deploy lpp_test
RUN cd / && git clone https://github.com/omzn/lpp_test 
# utilities
RUN cd /lpp_test/docker && ./mk_motd.sh aqua.png
RUN echo '[ ! -z "$TERM" -a -r /etc/motd ] && cat /etc/motd && cat /etc/issue ' >> /etc/bash.bashrc
#RUN echo '#!/bin/sh\npython3 -m pytest $1 $2 $3 $4 $5 $6 $7 $8 $9' > /usr/local/bin/pytest && chmod +x /usr/local/bin/pytest
COPY pytest /usr/local/bin/pytest
COPY bashrc /root/.bashrc
COPY issue /etc/issue
COPY lpptest /usr/local/bin/lpptest 
