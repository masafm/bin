#!/usr/bin/env python3
# Reply customer with quotation

# %%%{CotEditorXInput=Selection}%%%
# %%%{CotEditorXOutput=None}%%%

import sys
import subprocess
import re
import os
import datetime

def decode(s, encodings=('utf8', 'cp932')):
    for encoding in encodings:
        try:
            return s.decode(encoding)
        except UnicodeDecodeError:
            pass
    return ''

d = datetime.datetime.now()
input = sys.stdin.buffer.read()
text=""
count=0
try:
    for line in decode(input).splitlines():
        newline = re.sub('\r\n$', '\n', line)
        count += 1
        if newline.startswith('>'):
            text += f">{newline}\n"
        else:
            text += f"> {newline}\n"
except BrokenPipeError:
    devnull = os.open(os.devnull, os.O_WRONLY)
    os.dup2(devnull, sys.stdout.fileno())
    sys.exit(1)

path=f"{os.environ['HOME']}/Documents/drafts/{d.strftime('%Y%m%d-%H%M%S')}.txt"
with open(path, 'w') as f:
    f.write(f"""ご担当者様

お世話になっております｡ Datadog 柏木です｡

{text}

以上､よろしくお願いいたします｡
""")

cmd = ["/Applications/CotEditor.app/Contents/SharedSupport/bin/cot", "-l", str(count+5), path]
p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out, err = p.communicate()
