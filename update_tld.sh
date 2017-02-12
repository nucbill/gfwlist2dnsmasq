#!/bin/bash
grep -iv "^//" public_suffix_list.dat |grep -iv "^$"> gfwlist2dnsmasq/resources/tld.txt
