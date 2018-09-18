#!/usr/bin/env python3.6

class AssociativityMismatchError(Exception):
    pass

class OpNode:

    # overrided 
    rank = 1
    associativity = 'left'
    
    @staticmethod
    def func(x, y):
        return x + y

    # common

    def __init__(self, parent=None):
        self.operands = []
        self.parent = parent

    def eval(self):

        self.operands = [x if type(x) in (int, float) else x.eval() for x in self.operands]

        result = self.operands[0]
        for x in self.operands[1:]:
            result = self.func(result, x)

        return result

    def __str__(self):
        ops = ' '.join([str(op) for op in self.operands])
        return f'({self.symbol} {ops})'

    __repr__ = __str__


class Add(OpNode):
    symbol = '+'
    rank = 1
    associativity = 'left'

    @staticmethod
    def func(x, y):
        return x + y


class Mul(OpNode):
    symbol = '*'
    rank = 2 
    associativity = 'left'

    @staticmethod
    def func(x, y):
        return x * y


class Sub(OpNode):
    symbol = '-'
    rank = 1
    associativity = 'left'

    @staticmethod
    def func(x, y):
        return x - y


class Div(OpNode):
    symbol = '/'
    rank = 2
    associativity = 'left'

    @staticmethod
    def func(x, y):
        return x / y


class Pow(OpNode):
    symbol = '^'
    rank = 3 
    associativity = 'right'

    @staticmethod
    def func(x, y):
        return x ** y


OP_CLASSES = {
        '+': Add,
        '*': Mul,
        '-': Sub,
        '/': Div,
        '^': Pow,
}


def create_op_tree(tokens):

    last_x = tokens[-1]
    pairs = zip(tokens[::2], tokens[1::2])  # [(1, '+'), (3, '-')...]

    pairs = list(pairs)

    # guard
    prev_op = OP_CLASSES['+']()
    prev_op.operands = [0]

    top = prev_op

    for x, op_symbol in pairs:

        new_op = OP_CLASSES[op_symbol]()

        # 1 + 2 * 3
        if new_op.rank > prev_op.rank:
            new_op.operands.append(x)
            new_op.parent = prev_op
            prev_op.operands.append(new_op)

        # 1 + 2 - 3
        elif new_op.rank == prev_op.rank:
            if new_op.associativity != prev_op.associativity:
                raise AssociativityMismatchError

            if new_op.associativity == 'left':
                prev_op.operands.append(x)

                # exchange parent
                top_level = prev_op.parent
                prev_op.parent = new_op
                new_op.parent = top_level
                if top_level is not None:
                    top_level.operands.pop()
                    top_level.operands.append(new_op)

                if top is prev_op:
                    top = new_op

                new_op.operands.append(prev_op)

            else: # right associativity
                prev_op.operands.append(new_op)
                new_op.operands.append(x)
                new_op.parent = prev_op

        # 2 * 3 + 5
        else: # new_op.rank < prev_op.rank
            
            init_prev_op = prev_op
            init_prev_op.operands.append(x)

            while new_op.rank < prev_op.rank:
                prev_op = prev_op.parent

            if new_op.rank > prev_op.rank:
                op = prev_op.operands.pop()
                new_op.operands.append(op)
                new_op.parent = prev_op
                prev_op.operands.append(new_op)

            # 1 + 2 - 3
            elif new_op.rank == prev_op.rank:
                if new_op.associativity != prev_op.associativity:
                    raise AssociativityMismatchError

                # exchange parent
                top_level = prev_op.parent
                prev_op.parent = new_op
                new_op.parent = top_level
                if top_level is not None:
                    top_level.operands.pop()
                    top_level.operands.append(new_op)

                if top is prev_op:
                    top = new_op

                new_op.operands.append(prev_op)

        prev_op = new_op

    prev_op.operands.append(last_x)

    return top


def tokenize(s):

    for symbol in OP_CLASSES:
        s = s.replace(symbol, f' {symbol} ')

    tokens = s.split()
    
    for i, t in enumerate(tokens):
        for numtype in (int, float):
            try:
                x = numtype(t)
            except ValueError:
                continue
            else:
                tokens[i] = x
                break

    return tokens


if __name__ == '__main__':
    while True:
        s = input('> ')

        if s in 'qQ':
            break

        tokens = tokenize(s)
        optree = create_op_tree(tokens)
        print(optree)
        print(optree.eval())
