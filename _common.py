# This is common class
import sys

class common:
    cot="/Applications/CotEditor.app/Contents/SharedSupport/bin/cot"

    def decode(s, encodings=('utf8', 'cp932')):
        for encoding in encodings:
            try:
                return s.decode(encoding)
            except UnicodeDecodeError:
                pass
            return ''

    def add_quote(output):
        count=0
        while line := sys.stdin.buffer.readline():
            line = common.decode(line)
            if line.startswith('>'):
                output.write(f">{line}")
            else:
                output.write(f"> {line}")
            count += 1
        return count

    def reply_template(output,func=None):
        output.write("""ご担当者様

お世話になっております｡ Datadog 柏木です｡

""")
        count = func(output) if func else 0
        output.write("""

以上､よろしくお願いいたします｡""")
        return count+7
