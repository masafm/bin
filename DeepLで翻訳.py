#!/usr/bin/env python3
# Translate texts by DeepL API

# %%%{CotEditorXInput=AllText}%%%
# %%%{CotEditorXOutput=ReplaceAllText}%%%

import sys
import subprocess
import re
import os
import json
import argparse

def decode(s, encodings=('utf8', 'cp932')):
    for encoding in encodings:
        try:
            return s.decode(encoding)
        except UnicodeDecodeError:
            pass
    return ''

parser = argparse.ArgumentParser(prog=sys.argv[0], usage='Provides texts from standard input', add_help=True)
parser.add_argument('-k', '--key', help='DeepL API key')
parser.add_argument('-l', '--lang', help='Target language. JA, EN, etc')
args = parser.parse_args()

if not args.key:
    with open(os.environ['HOME']+'/.deepl') as file:
        args.key = file.readline()
if not args.lang:
    args.lang = 'EN'

input = sys.stdin.buffer.read()
try:
    text='\n'.join(decode(input).splitlines())
except BrokenPipeError:
    devnull = os.open(os.devnull, os.O_WRONLY)
    os.dup2(devnull, sys.stdout.fileno())
    sys.exit(1)
print(text+"\n-----")
cmd = ["curl",
       "-X", "POST",
       "https://api-free.deepl.com/v2/translate",
       "-H", f"Authorization: DeepL-Auth-Key {args.key}",
       "-d", "@-",
       "-d", f"target_lang={args.lang}"]
p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out, err = p.communicate(input="text="+text)
print(json.loads(out)['translations'][0]['text'])
