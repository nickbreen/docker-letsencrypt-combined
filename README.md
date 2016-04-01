
# Usage

Run an instance. E.g.

```
le:
  build: nickbreen/letsencrypt-combined
  volumes:
    - /certs # mount this from the haproxy
    - /var/www # mount this from the web server
  environment:
    CRON_D_LE: |
      @monthly root le renew | logger
```

The service remains running for `cron`.

Then `exec` into the container and run `le` to invoke letsencrypt.

```
docker exec le le -c /etc/opt/letsencrypt/combined.cli --email webmaster@example.com --domains www.example.com,example.com
```

Configuration files are provided with useful defaults in `$XDG_CONFIG_HOME/letsencrypt`, consult each files for more info.

Notes:

- "combined" installation requires the volume at `/certs`, which cam
  be specified with `--letsencrypt-combined:combined-path`. Typically
  this is a volume mounted from `dockercloud/haproxy`.
- "webroot" authentication requires the web server's docroot volume
  mounted at `/var/www`, which can be specified with `--webroot-path`.
- as of writing `dockercloud/haproxy:1.2.1` (and earlier) requires
  **re-deployment** to pickup the new certificates, `/reload.sh` does not.
