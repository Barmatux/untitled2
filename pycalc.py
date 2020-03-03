from symbol_classes import base_symbol
from const_and_paterns import token_pattern, symbol_table, operator_table
from numbers import Number
import math
import argparse
from error_classes import Error


global token, gen


def expression(rbp=0):
    global token, gen
    t = token
    token = next(gen)
    left = t.nud()
    while rbp < token.lbp:
        t = token
        token = next(gen)
        if isinstance(left, Number) or left is None:
            left = t.led(left)
        elif isinstance(left.value, float):
            left = t.led(float(left.value))
        else:
            left = t.led(int(left.value))
    if isinstance(left, Number):
        return left
    else:
        return left.value


def infix(id, bp):
    def count_left(oper, left):
        a = expression(bp)
        if isinstance(a, Number) and (left, Number):
            return operator_table[id](left, a)
        elif isinstance(a, int):
            a = int(a.value)
        else:
            a = float(a.value)
        return operator_table[id](left, a)
    make_symbol(id, bp).led = count_left


def prefix(id, bp):
    def count(exp):
        if exp.value == 'e' or exp.value == 'pi':
            return getattr(math, exp.value)
        if exp.id == 'func':
            try:
                x = getattr(math, exp.value)
            except Exception:
                print('Unknown function {}'.format(exp.value))
                exit(-1)
            else:
                return x(expression(bp))
        a = expression(bp)
        if not isinstance(a, Number):
            a = float(a.value)
        if id == '+':
            return a
        elif id == '-':
            return -a
    make_symbol(id).nud = count


def make_symbol(id, bp=0):
    try:
        s = symbol_table[id]
    except KeyError:
        class s(base_symbol):
            pass
        s.id = id
        s.lbp = bp
        symbol_table[id] = s
    else:
        s.lbp = max(bp, s.lbp)
    return s


def nud(oper):
    expr = expression()
    advance(")")
    return expr
make_symbol("(").nud = nud


def advance(id=None):
    global token
    if id and token.id != id:
        try:
            raise Error()
        except Error as e:
            print(': bracket unbalanced')
            exit(-1)
    token = next(gen)


def tokenize(inpt: str):
    """Tokenize our input string and make token one  of the given type"""
    for flt, integ,  func, operator in token_pattern.findall(inpt):
        if flt or integ:
            make_symbol= symbol_table['lit']
            s = make_symbol()
            if flt:
                s.value = float(flt)
            else:
                s.value = int(integ)
            yield s
        elif func:
            s = symbol_table['func']()
            s.value = func
            yield s
        else:
            op = symbol_table.get(operator)
            if not op:
                try:
                    raise Error()
                except Error:
                    print('Syntaxis error')
                    exit(-1)
            yield op()
    symbol = symbol_table['end']()
    yield symbol


def parse(inpt: str):
    global gen, token
    gen = tokenize(inpt)
    token = next(gen)
    return expression()


# def read_console():
    # parser = argparse.ArgumentParser()
    # parser.add_argument('EXPRESSION', nargs='+', help="expression string to evaluate")
    # name = 'EXPRESSION'
    # args = parser.parse_args()
    # inpt_lst_str = vars(args).get(name)
    # fr = ' '.join(inpt_lst_str)
    # return fr


def main():
    print(parse('cos(-2)'))


infix("+", 10)
infix("-", 10)
infix("*", 20)
infix("/", 20)
infix("//", 20)
infix("%", 20)
infix("^", 30)
prefix("+", 100)
prefix("-", 100)
prefix('func', 200)

make_symbol("lit").nud = lambda exp: exp
make_symbol("end")
make_symbol('(', 150)
make_symbol(')')
infix("<", 5); infix("<=", 5)
infix(">", 5); infix(">=", 5)
infix("!=", 5); infix("==", 5)



if __name__ == "__main__":
    main()
