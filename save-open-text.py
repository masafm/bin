#!/usr/bin/env python3
import subprocess
import os
import datetime
import sys
from _common import common as c

d = datetime.datetime.now()
path=f"{os.environ['HOME']}/Documents/drafts/{d.strftime('%Y%m%d-%H%M%S')}.txt"
text=c.decode(sys.stdin.buffer.read())

with open(path, 'w') as f:
    f.write(text)
print(path)
