import re

def has_digit(str):
    return bool(re.search(r'\d', str))