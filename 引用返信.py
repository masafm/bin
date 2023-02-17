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
cmd = ["/Applications/CotEditor.app/Contents/SharedSupport/bin/cot"]
p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
text = ""
try:
    for line in decode(input).splitlines():
        newline = re.sub('\r\n$', '\n', line)
        if newline.startswith('>'):
            text += f">{newline}\n"
        else:
            text += f"> {newline}\n"
except BrokenPipeError:
    devnull = os.open(os.devnull, os.O_WRONLY)
    os.dup2(devnull, sys.stdout.fileno())
    sys.exit(1)

out, err = p.communicate(input=f"""ご担当者様

お世話になっております｡ Datadog 柏木です｡

{text}

以上､よろしくお願いいたします｡
""")
