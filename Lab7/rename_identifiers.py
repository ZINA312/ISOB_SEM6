import re
import random
import string
import keyword
import builtins  

def rename_identifiers(code):
    builtins_set = set(dir(builtins))  
    keywords_set = set(keyword.kwlist)
    reserved_names = builtins_set | keywords_set 

    code_without_strings = re.sub(r'(\".*?\"|\'.*?\')', '', code, flags=re.DOTALL)
    code_without_comments = re.sub(r'#.*', '', code_without_strings)
    
    identifiers = re.findall(r'\b(?!def\b|class\b)([a-zA-Z_][a-zA-Z0-9_]*)\b(?=\s*[=\(])', code_without_comments)
    
    unique_ids = {name for name in identifiers if name not in reserved_names}
    
    replacements = {}
    for name in unique_ids:
        new_name = ''.join(random.choices(string.ascii_letters, k=random.randint(4, 8)))
        replacements[name] = new_name
    
    for old, new in replacements.items():
        code = re.sub(r'\b' + re.escape(old) + r'\b', new, code)
    
    return code