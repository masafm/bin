# This is common class
import sys

class common:
    def decode(s, encodings=('utf8', 'cp932')):
        for encoding in encodings:
            try:
                return s.decode(encoding)
            except UnicodeDecodeError:
                pass
            return ''

    def add_quote():
        text=""
        for line in common.decode(sys.stdin.buffer.read()).splitlines():
            if line.startswith('>'):
                text += f">{line}\n"
            else:
                text += f"> {line}\n"
        return text
