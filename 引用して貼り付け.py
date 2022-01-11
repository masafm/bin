#!/usr/bin/env python3
# Paste clipboard text with quote marks

# %%%{CotEditorXInput=None}%%%
# %%%{CotEditorXOutput=InsertAfterSelection}%%%

import sys
import subprocess

cmd = ["pbpaste"]
p = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
for line in p.stdout.strip().splitlines():
    print(f"> {line}")


