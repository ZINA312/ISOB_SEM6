from rename_identifiers import rename_identifiers
from add_junk_code import add_junk_code
from encrypt_strings import encrypt_strings

def obfuscate(code):
    code = rename_identifiers(code)
    code = add_junk_code(code)
    code = encrypt_strings(code)
    return code

input_code_1 = '''
def calculate_sum(a, b):
    result = a + b
    print("Result:", result)
    return result

calculate_sum(5, 3)
'''
input_code_2 = '''
def custom_function(x, y):
    total = x * y
    max_value = max(x, y)
    print("Max value is:", max_value)
    return total

print(custom_function(3, 5))
'''
input_code_3 = '''
global_var = 100

def outer_function(a):
    def inner_function(b):
        return a + b + global_var
    return inner_function(10)

print(outer_function(5))
'''

obfuscated_code = obfuscate(input_code_1)
print(obfuscated_code)