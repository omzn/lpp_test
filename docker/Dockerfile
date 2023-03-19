FROM gcc:latest
RUN apt update
RUN curl -sL https://deb.nodesource.com/setup_lts.x | bash - 
RUN apt install -y nodejs
RUN apt install -y python3-pytest python3-pytest-timeout tmux
RUN cd / && git clone https://github.com/omzn/casljs && cd /casljs && npm ci
RUN cd / && git clone https://github.com/omzn/lpp_test 
RUN cd /lpp_test/docker && ./mk_motd.sh aqua.png && cp motd /etc/motd
RUN echo '[ ! -z "$TERM" -a -r /etc/motd ] && cat /etc/motd && cat /etc/issue ' >> /etc/bash.bashrc
COPY bashrc /root/.bashrc
COPY issue /etc/issue