#!/bin/bash

/etc/init.d/xinetd restart
/cockroach-v20.1.8.linux-amd64/cockroach start-single-node --insecure --listen-addr=0.0.0.0:26257 --http-addr=0.0.0.0:8080 --background &
tail -f /dev/null
