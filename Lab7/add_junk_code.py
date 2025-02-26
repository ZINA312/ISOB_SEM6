import random

def add_junk_code(code):
    junk_statements = [
        'x = 0\nfor _ in range(10): x += 1\n',
        'print("This is junk!")\n',
        'y = [i**2 for i in range(5)]\n'
    ]
    lines = code.split('\n')
    
    for _ in range(3):
        pos = random.randint(0, len(lines))
        lines.insert(pos, random.choice(junk_statements))
    return '\n'.join(lines)