#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pkgutil
import urlparse
import logging
import urllib2
import time
import re
from argparse import ArgumentParser

__all__ = ['main']


gfwlist_url = 'https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt'


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-i', '--input', dest='input',
                        help='local path or remote url of gfwlist, ignore to use default address', metavar='GFWLIST')
    parser.add_argument('-f', '--file', dest='output', required=True,
                        help='path to the output config file', metavar='FILE')
    parser.add_argument('-d', '--dns', dest='dns', required=True,
                        help='the upstream dns server to use to resolve related domains', metavar='DNS')
    parser.add_argument('-p', '--port', dest='port',
                        help='the port for the upstream dns server', metavar='PORT')
    parser.add_argument('--user-rule', dest='user_rule',
                        help='user rule file, which will be appended to gfwlist')
    return parser.parse_args()


def decode_gfwlist(content):
    # decode base64 if have to
    try:
        return content.decode('base64')
    except StandardError:
        return content


def get_hostname(something):
    try:
        # quite enough for GFW
        if not something.startswith('http:'):
            something = 'http://' + something
        r = urlparse.urlparse(something)
        return r.hostname
    except Exception as e:
        logging.error(e)
        return None


def add_domain_to_set(s, something):
    hostname = get_hostname(something)
    if hostname is not None:
        if hostname.startswith('.'):
            hostname = hostname.lstrip('.')
        if hostname.endswith('/'):
            hostname = hostname.rstrip('/')
        if hostname:
            s.add(hostname)


def parse_gfwlist(content, user_rule=None):
    builtin_rules = pkgutil.get_data('gfwlist2dnsmasq', 'resources/builtin.txt').splitlines(False)
    gfwlist = content.splitlines(False)
    if user_rule:
        gfwlist.extend(user_rule.splitlines(False))
    domains = set(builtin_rules)
    for line in gfwlist:
        if line.find('.*') >= 0:
            continue
        elif line.find('*') >= 0:
            line = line.replace('*', '/')
        if line.startswith('!'):
            continue
        elif line.startswith('['):
            continue
        elif line.startswith('@'):
            # ignore white list
            continue
        elif line.startswith('||'):
            add_domain_to_set(domains, line.lstrip('||'))
        elif line.startswith('|'):
            add_domain_to_set(domains, line.lstrip('|'))
        elif line.startswith('.'):
            add_domain_to_set(domains, line.lstrip('.'))
        else:
            add_domain_to_set(domains, line)
    return domains


def reduce_domains(domains):
    # reduce 'www.google.com' to 'google.com'
    # remove invalid domains
    tld_content = pkgutil.get_data('gfwlist2dnsmasq', 'resources/tld.txt')
    tlds = set(tld_content.splitlines(False))
    new_domains = set()
    for domain in domains:
        domain_parts = domain.split('.')
        last_root_domain = None
        for i in xrange(0, len(domain_parts)):
            root_domain = '.'.join(domain_parts[len(domain_parts) - i - 1:])
            if i == 0:
                if not tlds.__contains__(root_domain):
                    # root_domain is not a valid tld
                    break
            last_root_domain = root_domain
            if tlds.__contains__(root_domain):
                continue
            else:
                break
        if last_root_domain is not None:
            new_domains.add(last_root_domain)
    return new_domains


def generate_dnsmasq_conf(domains, dns, port):
    # render the config file
    proxy_content = pkgutil.get_data('gfwlist2dnsmasq', 'resources/gfwlist.conf')
    domains_string = ''
    for domain in domains:
        domains_string += 'server=/.' + domain + '/' + dns + '#' + port + '\n'
    proxy_content = proxy_content.replace('__DOMAINS__', domains_string)
    gen_time = time.localtime()
    format_time = time.strftime("%Y-%m-%d %X %z", gen_time)
    proxy_content = proxy_content.replace('__TIME__', format_time)
    return proxy_content

def is_url(input):
    # URL validator copied from django
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
        r'localhost|' # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' # ...or ipv6
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return regex.match(input)

def main():
    args = parse_args()
    user_rule = None
    if args.input:
        if is_url(args.input):
            print 'Downloading gfwlist from %s' % args.input
            content = urllib2.urlopen(args.input, timeout=10).read()
        else:
            with open(args.input, 'rb') as f:
                content = f.read()
    else:
        print 'Downloading gfwlist from %s' % gfwlist_url
        content = urllib2.urlopen(gfwlist_url, timeout=10).read()
    if args.user_rule:
        with open(args.user_rule, 'rb') as f:
            user_rule = f.read()
    if args.port:
        dns_port = args.port
    else:
        dns_port = '53'
    content = decode_gfwlist(content)
    domains = parse_gfwlist(content, user_rule)
    #domains = reduce_domains(domains)
    #do not need to reduce domains for dnsmasq
    pac_content = generate_dnsmasq_conf(domains, args.dns, dns_port)
    with open(args.output, 'wb') as f:
        f.write(pac_content)


if __name__ == '__main__':
    main()
