import numpy as np


class Variable:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.value = None
        self.degree = -1
        self.domain = {0, 1}


def MCdV(variables):
    one_constrained_variables = list()
    two_constrained_variables = list()
    one = False
    for var in variables.flatten():
        if var.value is None:
            if len(var.domain) == 1:
                one = True
                one_constrained_variables.append(var)
            elif not one:
                two_constrained_variables.append(var)

    if one:
        return one_constrained_variables
    return two_constrained_variables


def MCgV(most_constrained_variables):
    pass


def forward_checking(var, variables):
    pass


def MAC(var, variables):
    pass


def main():
    variables = input_parser()


def input_parser():
    row, col = input().split()

    data = []
    for i in range(int(row)):
        dummy = input().split()
        for j in range(int(col)):
            var = Variable(i, j)
            data.append(var)
            if dummy[j] != "-":
                var.value = int(dummy[j])

    return np.array(data, dtype='object')


if __name__ == '__main__':
    main()
