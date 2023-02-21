#!/usr/bin/env python3
# Paste clipboard text with quote marks

# %%%{CotEditorXInput=Selection}%%%
# %%%{CotEditorXOutput=InsertAfterSelection}%%%

import sys
from _common import common as c

c.add_quote(sys.stdin, sys.stdout)
