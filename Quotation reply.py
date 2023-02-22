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
    count = c.reply_template(f, c.add_quote)
cmd = ["/Applications/CotEditor.app/Contents/SharedSupport/bin/cot", "-l", str(count-2), path]
p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out, err = p.communicate()
