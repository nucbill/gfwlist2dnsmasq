GFWList2Privoxy
==============================================================


Usage
--------------------------------------------------------------

Generate config file for dnsmasq from gfwlist, forked from snachx's gfwlist2privoxy_ and modified

::

    pip install gfwlist2privoxy

    usage: main.py [-h] [-i GFWLIST] -f FILE -d DNS [-p PORT] [--user-rule USER_RULE]

    detail arguments:
      -h, --help                    show this help message and exit

      -i GFWLIST, --input GFWLIST   local path or remote url of gfwlist, ignore to use default address

      -f ACTION, --file ACTION      path to the output action file

      -d DNS, --dns DNS             the upstream dns server to use to resolve related
                                    domains
      -p PORT, --port PORT          the port for the upstream dns server

      --user-rule USER_RULE         user rule file, which will be appended to gfwlist

Example Action File
----------------------------------------------------------
An example of generated action file is here_.

.. _gfwlist2privoxy: https://github.com/snachx/gfwlist2privoxy
.. _here: 
