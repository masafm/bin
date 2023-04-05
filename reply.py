#!/usr/bin/env python3
import subprocess
import os
import datetime
import sys
from _common import common as c

d = datetime.datetime.now()
path=f"{os.environ['HOME']}/Documents/Drafts/{d.strftime('%Y%m%d-%H%M%S')}.md"

with open(path, 'w') as f:
    count = c.reply_template(f, c.add_quote)
print(path)

