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

    def add_quote(input,output):
        count=0
        while line := input.buffer.readline():
            line = common.decode(line)
            if line.startswith('>'):
                output.write(f">{line}")
            else:
                output.write(f"> {line}")
            count += 1
        return count
