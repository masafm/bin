#!/usr/bin/env python3
# Delete timestamps in the begining of each line

# %%%{CotEditorXInput=AllText}%%%
# %%%{CotEditorXOutput=ReplaceAllText}%%%

import sys
import re
from _common import common as c

while line := sys.stdin.buffer.readline():
    tmp = re.sub('^\[.+?\] ?', '', c.decode(line))
    sys.stdout.write(re.sub('\r\n$', '\n', tmp))
