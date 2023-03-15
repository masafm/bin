#!/usr/bin/env python3
import sys
import subprocess
import os
import json
import argparse
from _common import common as c

parser = argparse.ArgumentParser(prog=sys.argv[0], usage='Provides texts from standard input', add_help=True)
parser.add_argument('-k', '--key', help='DeepL API key')
parser.add_argument('-l', '--lang', help='Target language. JA, EN, etc')
args = parser.parse_args()

if not args.key:
    with open(os.environ['HOME']+'/.deepl') as file:
        args.key = file.readline()
if not args.lang:
    args.lang = 'EN'

text=c.decode(sys.stdin.buffer.read())
print(text+"-----")
cmd = ["curl",
       "-X", "POST",
       "-H", f"Authorization: DeepL-Auth-Key {args.key}",
       "-d", f"target_lang={args.lang}",
       "-d", "@-",
       "https://api-free.deepl.com/v2/translate",
       ]
p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out, err = p.communicate(input="text="+text)
print(json.loads(out)['translations'][0]['text'])
