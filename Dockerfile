FROM nickbreen/letsencrypt:v1.0.0

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -qqy jq && apt-get clean

ENV COMB_VER=1.0.0 COMB_DIR=/opt/letsencrypt-combined-installer

RUN URL=$(curl -LsSf https://api.github.com/repos/nickbreen/letsencrypt-combined-installer/releases/tags/v$COMB_VER | jq -r .tarball_url) && \
    curl -sSfL $URL | (mkdir -p $COMB_DIR && tar zx -C $COMB_DIR --strip-components 1)

RUN . $LE_DIR/venv/bin/activate && cd $COMB_DIR && python setup.py install

ENV XDG_CONFIG_HOME=/etc/opt

COPY *.ini $XDG_CONFIG_HOME/letsencrypt/

# Test
RUN TMP=$(mktemp -d) && cd $TMP && \
    le --help letsencrypt-combined:combined && \
    (openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 90 -nodes -subj '/CN=example.com/O=Test/C=NZ' && \
    le -vvv --config $XDG_CONFIG_HOME/letsencrypt/install.ini install \
        --cert-path cert.pem \
        --key-path key.pem \
        --domains example.com \
        --letsencrypt-combined:combined-path . && \
    test -s example.com.pem ) && \
    cd && rm -rf $TMP

# Add a default cron job that does monthly renews (and logs them)
ENV CRON_D_LE="@monthly root le renew | logger\n"
