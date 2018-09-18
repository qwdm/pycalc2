#!/usr/bin/env python3.6

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
        if self.associativity == 'right':
            self.operands.reverse()

        self.operands = [x if type(x) in (int, float) else x.eval() for x in self.operands]

        result = self.operands.pop()
        for x in self.operands:
            result = self.func(result, x)

        return result

    def __str__(self):
        return f'<{self.symbol}> {self.operands}'

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


OP_CLASSES = {
        '+': Add,
        '*': Mul,
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
        if op_symbol == prev_op.symbol:
            prev_op.operands.append(x)
            continue

        new_op = OP_CLASSES[op_symbol]()

        # 1 + 2 * 3
        if new_op.rank >= prev_op.rank:
            new_op.operands.append(x)
            new_op.parent = prev_op
            prev_op.operands.append(new_op)

        # 2 * 3 + 4
        else:
            prev_op.operands.append(x)

            while True:
                parent = prev_op.parent
                if parent.rank <= new_op.rank:
                    break
            
            parent.operands.append(new_op)

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
#    tokens = [1, '+', 2, '*', 3]
#    print(create_op_tree(tokens))
#
#    tokens = [4, '*', 2, '+', 3]
#    print(create_op_tree(tokens))
    while True:
        s = input('> ')

        if s in 'qQ':
            break

        tokens = tokenize(s)
        optree = create_op_tree(tokens)
        print(optree.eval())




    


