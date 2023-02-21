#!/usr/bin/env python3
# Reply customer with quotation

# %%%{CotEditorXInput=Selection}%%%
# %%%{CotEditorXOutput=None}%%%

import subprocess
import re
import os
import datetime
import sys
from _common import common as c

d = datetime.datetime.now()
path=f"{os.environ['HOME']}/Documents/drafts/{d.strftime('%Y%m%d-%H%M%S')}.txt"
text=c.decode(sys.stdin.buffer.read())

with open(path, 'w') as f:
    f.write(text)

cmd = ["open", path]
p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out, err = p.communicate()
