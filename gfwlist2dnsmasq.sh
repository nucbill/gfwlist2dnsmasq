#!/bin/bash
PYTHONPATH=. python `dirname $0`/gfwlist2dnsmasq/main.py $*
