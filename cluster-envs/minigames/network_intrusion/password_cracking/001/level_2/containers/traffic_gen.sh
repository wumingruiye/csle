#!/bin/bash

while :
do
	wget 172.18.2.2
	sleep 1
	psql -h 172.18.2.21 -p 5432
	sleep 1
	curl 172.18.2.3
	sleep 1
	curl 172.18.2.79:8080
	sleep 10
done