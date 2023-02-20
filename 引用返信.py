#!/usr/bin/env python3
# Reply customer with quotation

# %%%{CotEditorXInput=Selection}%%%
# %%%{CotEditorXOutput=None}%%%

import subprocess
import re
import os
import datetime
from common import common as c

d = datetime.datetime.now()
path=f"{os.environ['HOME']}/Documents/drafts/{d.strftime('%Y%m%d-%H%M%S')}.txt"
text=c.add_quote()

with open(path, 'w') as f:
    f.write(f"""ご担当者様

お世話になっております｡ Datadog 柏木です｡

{text}

以上､よろしくお願いいたします｡
""")

cmd = ["/Applications/CotEditor.app/Contents/SharedSupport/bin/cot", "-l", str(text.count('\n')+5), path]
p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out, err = p.communicate()
