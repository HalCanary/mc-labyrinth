#!/usr/bin/python
# Copyright 2015 Hal Canary
# Use of this program is governed by the file LICENSE.md.
import subprocess
import sys
import time
for line in sys.stdin:
    subprocess.call([
        'screen', '-S', 'minecraft', '-X', 'stuff', '%s\r' % line.strip()])
    time.sleep(0.01)
