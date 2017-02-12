#!/bin/bash

pushd .. && \
PYTHONPATH=. python gfwlist2dnsmasq/main.py  -i test/gfwlist.txt -f test/gfwlist.conf -p 1053 -d 192.168.1.1 --user-rule test/user_rule.txt && \
popd && cat gfwlist.conf && [ -n "`grep -e .googleapis.com gfwlist.conf`" ]  && [ -n "`grep -e .twitter.com gfwlist.conf`" ] && \
[ -n "`grep -e .userdefined.com gfwlist.conf`" ] && echo 'Test passed'
