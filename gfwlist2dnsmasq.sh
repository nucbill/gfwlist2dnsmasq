#!/bin/bash
dir=`dirname $0`
PYTHONPATH=. python $dir/gfwlist2dnsmasq/main.py $*
