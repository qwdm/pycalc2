import sys
import random
import pycalc2



def random_expr():

    numops = random.randint(0, 7)

    tokens = [random.randint(1, 3)]

    for _ in range(numops):
        tokens.append(random.choice(list(pycalc2.OP_CLASSES.keys())))
        tokens.append(random.randint(1,3))

    tokens = [str(t) for t in tokens]
    expr = ' '.join(tokens)

    return expr


def test_calc_random():

    for _ in range(100):
        expr = random_expr()
        print(expr)

        tokens = pycalc2.tokenize(expr)
        optree = pycalc2.create_op_tree(tokens)

        try:
            value = optree.eval()
            assert eval(expr.replace('^', '**')) == value
#            print(f'{expr} = {value}', file=sys.stderr)
        except OverflowError:
            pass

def test_calc():
    cases = [
        '1',

        '1 + 2',
        '2 * 3',
        '10 / 2',
        '4 ^ 120',
        '34 - 7',

        '1 + 2 + 3',
        '1 + 2 * 3',
        '1 + 5 - 10',
        '34 * 15 ^ 2',
        '113 ^ 5 - 3 * 2 ^ 4 ^ 2',
        '2 ^ 2 ^ 3 + 1',
        '3 ^ 4 ^ 5 * 2 + 1 - 100 * 11 ^ 4',
        '12 + 36 / 3 / 9 ^ 4 - 100'
    ]

    for expr in cases:
        expr = random_expr()

        tokens = pycalc2.tokenize(expr)
        optree = pycalc2.create_op_tree(tokens)
        value = optree.eval()

        assert eval(expr.replace('^', '**')) == value
