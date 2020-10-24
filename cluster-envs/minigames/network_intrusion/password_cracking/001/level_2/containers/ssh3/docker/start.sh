#!/bin/bash

nohup /usr/sbin/inspircd --runasroot --debug --nopid & > irc.log
rethinkdb --bind all --bind-http all --bind-cluster all &
/usr/sbin/sshd -D &
tail -f /dev/null
