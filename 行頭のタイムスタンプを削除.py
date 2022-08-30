#!/usr/bin/env python3
# Delete timestamps in the begining of each line

# %%%{CotEditorXInput=AllText}%%%
# %%%{CotEditorXOutput=ReplaceAllText}%%%

import sys
import subprocess
import re
import os

def decode(s, encodings=('utf8', 'cp932')):
    for encoding in encodings:
        try:
            return s.decode(encoding)
        except UnicodeDecodeError:
            pass
    return ''

input = sys.stdin.buffer.read()
try:
    for line in decode(input).splitlines():
        tmp = re.sub('^\[.+?\] ?', '', line)
        print(re.sub('\r\n$', '\n', tmp))
except BrokenPipeError:
    devnull = os.open(os.devnull, os.O_WRONLY)
    os.dup2(devnull, sys.stdout.fileno())
    sys.exit(1)
