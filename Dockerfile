FROM nickbreen/letsencrypt:v1.2.1

ENV COMB_VER=1.2.0-rc5 COMB_DIR=/opt/letsencrypt-combined-installer

RUN pip install python-dockercloud docker-cloud

RUN URL=$(curl -LsSf https://api.github.com/repos/nickbreen/letsencrypt-combined-installer/releases/tags/v$COMB_VER | jq -r .tarball_url) && \
    curl -sSfL $URL | (mkdir -p $COMB_DIR && tar zx -C $COMB_DIR --strip-components 1)

ENV XDG_CONFIG_HOME=/etc/opt

RUN . $LE_DIR/venv/bin/activate && pip install -e $COMB_DIR

COPY *.ini $XDG_CONFIG_HOME/letsencrypt/

# Test
RUN TMP=$(mktemp -d) && cd $TMP && \
    le --help letsencrypt-combined:combined && \
    le --help letsencrypt-combined:dockercloud && \
    (openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 90 -nodes -subj '/CN=test.example.com/OU=Test/O=Example/C=US' && \
    le -vvv --config $XDG_CONFIG_HOME/letsencrypt/install.ini install \
        --cert-path cert.pem \
        --key-path key.pem \
        --domains test.example.com \
        --letsencrypt-combined:combined-path . && \
    test -s test.example.com.pem ) && \
    cd && rm -rf $TMP

# Add a default cron job that does monthly renews (and logs them)
ENV CRON_D_LE="@monthly root /usr/local/bin/le renew 2>&1 | logger --tag le-renew\n"
