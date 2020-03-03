import re
from operator import *


symbol_table = {}

token_pattern = re.compile("(?:(\d*\.\d*)|(\d+)|(\w+)|(\>\=|\=\=|\<\=|\!\=|\/\/|.))")

operator_table = {'+': add, '-': sub, '*': mul, '/': truediv, '%': mod, '//': floordiv, '^': pow, '<': lt, '<=': le,
                  '==': eq, '>': gt, '>=': ge, '!=': ne, 'abs': abs, 'round': round
                  }