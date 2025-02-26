import base64
import re

def encrypt_strings(code):
    strings = re.findall(r'"(.*?)"', code)
    for s in strings:
        encoded = base64.b64encode(s.encode()).decode()
        code = code.replace(f'"{s}"', f'base64.b64decode("{encoded}").decode()')
    return code