#!/usr/bin/env python3
# Reply customer with quotation

# %%%{CotEditorXInput=Selection}%%%
# %%%{CotEditorXOutput=None}%%%

import subprocess
import os
import datetime
import sys
from _common import common as c

d = datetime.datetime.now()
path=f"{os.environ['HOME']}/Documents/drafts/{d.strftime('%Y%m%d-%H%M%S')}.txt"

with open(path, 'w') as f:
    print("ご担当者様", file=f)
    print("", file=f)
    print("お世話になっております｡ Datadog 柏木です｡", file=f)
    print("", file=f)
    count = c.add_quote(sys.stdin,f)
    print("", file=f)
    print("以上､よろしくお願いいたします｡", file=f)

cmd = ["/Applications/CotEditor.app/Contents/SharedSupport/bin/cot", "-l", str(count+5), path]
p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out, err = p.communicate()
