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
        try:
            for line in common.decode(sys.stdin.buffer.read()).splitlines():
                if line.startswith('>'):
                    text += f">{line}\n"
                else:
                    text += f"> {line}\n"
        except BrokenPipeError:
            devnull = os.open(os.devnull, os.O_WRONLY)
            os.dup2(devnull, sys.stdout.fileno())
            sys.exit(1)
        
        return text
