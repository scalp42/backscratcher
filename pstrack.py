#!/usr/bin/python
"""
show lineage of the current process

pstrack

Copyright (C) 1995 - <the end of time>  Tom Barron
  tom.barron@comcast.net
  177 Crossroads Blvd
  Oak Ridge, TN  37830

This software is licensed under the CC-GNU GPL. For the full text of
the license, see http://creativecommons.org/licenses/GPL/2.0/

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

import glob
import os
import pdb
import re
import subprocess
import sys
import toolframe
import unittest

from optparse import *

# ---------------------------------------------------------------------------
def main(args):
    p = OptionParser()
#     p.add_option('-b', '--background',
#                  action='store_true', default=False, dest='background',
#                  help='put the session in the background')
    p.add_option('-d', '--debug',
                 action='store_true', default=False, dest='debug',
                 help='start the debugger')
#     p.add_option('-t', '--tunnel',
#                  action='store', dest='tunnel',
#                  help='port to use for tunnel')
#     p.add_option('-v', '--verbose',
#                  action='store_true', default=False, dest='verbose',
#                  help='report more of what is going on')
    (o, a) = p.parse_args(args)

    if (o.debug): pdb.set_trace()

    pt = get_process_list()

    pid = str(os.getpid())
    while pid in pt.keys():
        print("%s %s" % (pid, pt[pid]['cmd']))
        pid = pt[pid]['ppid']
        
# ---------------------------------------------------------------------------
def get_process_list():
    mypid = os.getpid()
    pdir = "/proc/%d" % mypid
    if os.path.exists(pdir):
        # We have a /proc directory -- get the tree from there
        pass
    else:
        # We don't have a /proc dir -- have to call ps
        p = subprocess.Popen("ps -ef".split(),
                             stdin=None,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        (out, err) = p.communicate()
        ptxt = out.split('\n')
        rgx = r'\s*(\d+)\s+(\d+)\s+(\d+)\s+(\d+)' \
              + '\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)'
        pd = {}
        for pline in out.split('\n'):
            d = {}
            q = re.search(rgx, pline)
            if q:
                d['pid'] = q.groups()[1]
                d['ppid'] = q.groups()[2]
                d['cmd'] = q.groups()[7]
                pd[d['pid']] = d
                
        return pd

# ---------------------------------------------------------------------------
def usage():
    print("usage: pstrack")
    sys.exit(1)
    
# ---------------------------------------------------------------------------
toolframe.ez_launch(main)
