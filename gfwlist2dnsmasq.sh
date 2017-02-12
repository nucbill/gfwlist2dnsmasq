#!/bin/bash
dir=`dirname $0`
PYTHONPATH=$dir python $dir/gfwlist2dnsmasq/main.py $*
