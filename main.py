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


def MCgV(most_constrained_variables, unassigned_count):
    most_constraining_variable = None
    max_unassigned = -1
    for var in most_constrained_variables:
        unassigned = 0
        x = var.x
        y = var.y
        unassigned += unassigned_count[0][x] - 1
        unassigned += unassigned_count[1][y] - 1
        if unassigned > max_unassigned:
            max_unassigned = unassigned
            most_constraining_variable = var
    return most_constraining_variable


def forward_checking(var, variables, unassigned_count):

    x = var.x
    y = var.y

    # equality of zero and ones count

    zero_count_col = 0
    zero_count_row = 0
    one_count_col = 0
    one_count_row = 0

    for v in variables[x]:
        if v.value == 1:
            one_count_row += 1
        elif v.value == 0:
            zero_count_row += 1

    if zero_count_row >= variables.shape[0] // 2:
        for v in variables[x]:
            if v.value is None:
                v.domain.remove(0)

    elif one_count_row >= variables.shape[0] // 2:
        for v in variables[x]:
            if v.value is None:
                v.domain.remove(1)

    for v in variables[:, y]:
        if v.value == 1:
            one_count_col += 1
        elif v.value == 0:
            zero_count_col += 1

    if zero_count_col >= variables.shape[1] // 2:
        for v in variables[:, y]:
            if v.value is None:
                v.domain.remove(0)

    elif one_count_col >= variables.shape[1] // 2:
        for v in variables[:, y]:
            if v.value is None:
                v.domain.remove(1)

    # < 000 and < 111 in each col and row

    if x + 1 < variables.shape[0] and variables[x + 1][y].value == var.value:
        if x + 2 < variables.shape[0]:
            variables[x + 2][y].domain.remove(var.value)
        if x - 1 >= 0:
            variables[x - 1][y].domain.remove(var.value)

    if x - 1 >= 0 and variables[x - 1][y].value == var.value:
        if x + 1 < variables.shape[0]:
            variables[x + 1][y].domain.remove(var.value)
        if x - 2 >= 0:
            variables[x - 2][y].domain.remove(var.value)

    if x + 2 < variables.shape[0] and variables[x + 2][y].value == var.value:
        variables[x + 1][y].domain.remove(var.value)

    if x - 2 >= 0 and variables[x - 2][y].value == var.value:
        variables[x - 1][y].domain.remove(var.value)

    if y + 1 < variables.shape[1] and variables[x][y + 1].value == var.value:
        if y + 2 < variables.shape[1]:
            variables[x][y + 2].domain.remove(var.value)
        if y - 1 >= 0:
            variables[x][y - 1].domain.remove(var.value)

    if y - 1 >= 0 and variables[x][y - 1].value == var.value:
        if y + 1 < variables.shape[1]:
            variables[x][y + 1].domain.remove(var.value)
        if x - 2 >= 0:
            variables[x][y - 2].domain.remove(var.value)

    if y + 2 < variables.shape[1] and variables[x][y + 2].value == var.value:
        variables[x][y + 1].domain.remove(var.value)

    if y - 2 >= 0 and variables[x][y - 2].value == var.value:
        variables[x][y - 1].domain.remove(var.value)

    # different cols and rows

    if unassigned_count[0][x] == 0:
        for i in range(variables.shape[0]):
            if unassigned_count[0][i] == 1:
                equal = True
                unassigned_variable = None
                assigned_variable_value = None

                for j in range(variables.shape[1]):
                    if variables[i][j].value is None:
                        unassigned_variable = variables[i][j]
                        assigned_variable_value = variables[x][j].value
                    elif variables[x][j].value != variables[i][j].value:
                        equal = False
                        break

                if equal:
                    unassigned_variable.domain.remove(assigned_variable_value)

    if unassigned_count[1][y] == 0:
        for i in range(variables.shape[1]):
            if unassigned_count[1][i] == 1:
                equal = True
                unassigned_variable = None
                assigned_variable_value = None

                for j in range(variables.shape[0]):
                    if variables[j][i].value is None:
                        unassigned_variable = variables[j][i]
                        assigned_variable_value = variables[j][y].value
                    elif variables[j][y].value != variables[j][i].value:
                        equal = False
                        break

                if equal:
                    unassigned_variable.domain.remove(assigned_variable_value)


def MAC(var, variables):
    queue = []
    x = var.x
    y = var.y


def main():
    variables, unassigned_count = input_parser()


def input_parser():
    row, col = input().split()

    data = []
    unassigned_count = np.zeros((2, int(col)), dtype='int')
    for i in range(int(row)):
        inner_data = []
        dummy = input().split()
        for j in range(int(col)):
            var = Variable(i, j)
            inner_data.append(var)
            if dummy[j] != "-":
                var.value = int(dummy[j])
            else:
                unassigned_count[1][j] += 1
                unassigned_count[0][i] += 1
        data.append(inner_data)

    return np.array(data, dtype='object'), unassigned_count


if __name__ == '__main__':
    main()
