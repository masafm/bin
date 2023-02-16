#!/usr/bin/env python3
# Translate texts by DeepL API

# %%%{CotEditorXInput=AllText}%%%
# %%%{CotEditorXOutput=ReplaceAllText}%%%

import sys
import subprocess
import re
import os
import json

def decode(s, encodings=('utf8', 'cp932')):
    for encoding in encodings:
        try:
            return s.decode(encoding)
        except UnicodeDecodeError:
            pass
    return ''

input = sys.stdin.buffer.read()
try:
    if len(sys.argv) < 2:
        print("API key required")
        exit(1)
    key=sys.argv[1]
    lang="EN"
    if len(sys.argv) >= 3:
        lang = sys.argv[2]
    text='\n'.join(decode(input).splitlines())
    print(text+"\n-----")
    cmd = ["curl", "-X", "POST", "https://api-free.deepl.com/v2/translate", "-H", f"Authorization: DeepL-Auth-Key {key}", "-d", "@-", "-d", f"target_lang={lang}"]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, err = p.communicate(input="text="+text)
    print(json.loads(output)['translations'][0]['text'])
except BrokenPipeError:
    devnull = os.open(os.devnull, os.O_WRONLY)
    os.dup2(devnull, sys.stdout.fileno())
    sys.exit(1)
