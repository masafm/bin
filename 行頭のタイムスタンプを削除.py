#!/usr/bin/env python3
# Delete timestamps in the begining of each line

# %%%{CotEditorXInput=AllText}%%%
# %%%{CotEditorXOutput=ReplaceAllText}%%%

import sys
import subprocess
import re
import os
from _common import common as c

input = c.decode(sys.stdin.buffer.read())
for line in input.splitlines():
    tmp = re.sub('^\[.+?\] ?', '', line)
    print(re.sub('\r\n$', '\n', tmp))
