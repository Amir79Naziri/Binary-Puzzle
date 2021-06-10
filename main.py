from itertools import product
import random

import numpy as np


class Variable:

    def __init__(self, gtype, place, initial_value):
        self.gtype = gtype
        self.place = place
        self.initial_value = initial_value
        self.value = None
        if None not in initial_value:
            self.value = initial_value
        self.domain = []
        self.unary_constrained()

    def unary_constrained(self):
        total_domain = list(product([0, 1], repeat=len(self.initial_value)))
        for value in total_domain:
            for i in range(len(value)):
                if self.initial_value[i] is not None and value[i] != self.initial_value[i]:
                    break
            else:
                if self.value is not None:
                    continue
                one_count = 0
                zero_count = 0
                for v in value:
                    if v == 1:
                        one_count += 1
                    elif v == 0:
                        zero_count += 1

                if one_count != zero_count:
                    continue

                for i in range(len(value) - 2):
                    window = [value[i], value[i + 1], value[i + 2]]
                    total = map(sum, window)
                    if total == 3 or total == 0:
                        continue

                self.domain.append(value)


def MCdV(variables):
    minimum_domain_size = np.inf
    most_constrained_variables = []

    for var in variables:
        if var.value is None:
            if len(var.domain) < minimum_domain_size:
                minimum_domain_size = len(var.domain)

    for var in variables:
        if var.value is None:
            if len(var.domain) == minimum_domain_size:
                most_constrained_variables.append(var)

    return MCgV(most_constrained_variables)


def MCgV(most_constrained_variables):
    unassigned_rows = 0
    unassigned_cols = 0

    most_constrained_row_variables = []
    most_constrained_col_variables = []

    for var in most_constrained_variables:
        if var.value is None:
            if var.gtype == 'row':
                unassigned_rows += 1
                most_constrained_row_variables.append(var)
            elif var.gtype == 'col':
                unassigned_cols += 1
                most_constrained_col_variables.append(var)

    if unassigned_cols > unassigned_rows:
        return random.choice(most_constrained_col_variables)
    elif unassigned_cols < unassigned_rows:
        return random.choice(most_constrained_row_variables)
    else:
        return random.choice((random.choice(most_constrained_row_variables),
                              random.choice(most_constrained_col_variables)))


def forward_checking(var, variables):
    for v in variables:
        dummy = []
        if var.gtype == v.gtype and v.value is None:
            if var.value in v.domain:
                dummy.append(var.value)

        else:
            for d in v.domain:
                if d[var.place] != var.value[v.place] and v.value is None:
                    dummy.append(d)

        v.domain = [x for x in v.domain if x not in dummy]

        if len(v.domain) == 0:
            return False

    return True


def MAC(var, variables):  # todo : fix consistency
    queue = []
    for v in variables:
        if v != var and v.value is None:
            queue.append((v, var))

    while len(queue) > 0:
        arc = queue.pop(0)
        pre_domain_length = len(arc[0].domain)

        dummy = []

        if arc[1].value is None:
            if len(arc[1].domain) == 1:
                if arc[1].gtype == arc[0].gtype and arc[0].value is None:
                    if arc[1].domain[0] in arc[0].domain:
                        dummy.append(arc[1].domain[0])
                else:
                    for d in arc[0].domain:
                        if d[arc[1].place] != arc[1].domain[0][arc[0].place] and arc[0].value is None:
                            dummy.append(d)

        else:
            if arc[1].gtype == arc[0].gtype and arc[0].value is None:
                if arc[1].value in arc[0].domain:
                    dummy.append(arc[1].value)
            else:
                for d in arc[0].domain:
                    if d[arc[1].place] != arc[1].value[arc[0].place] and arc[0].value is None:
                        dummy.append(d)

        arc[0].domain = [x for x in arc[0].domain if x not in dummy]

        if len(arc[0].domain) == pre_domain_length:
            continue
        if len(arc[0].domain) == 0:
            return False

        for v in variables:
            if v != arc[0] and v != arc[1] and v.value is None:
                queue.append((v, arc[0]))

    return True


def CSP_backtracking(variables, assigned):
    if len(assigned) == len(variables):
        return assigned

    var = MCdV(variables)

    for value in var.domain:
        var.value = value
        assigned.append(var)
        variables_copy = variables.copy()
        # result = forward_checking(var, variables_copy)
        result = MAC(var, variables_copy)
        if not result:
            return False

        res = CSP_backtracking(variables_copy, assigned)
        if res:
            return True

        assigned.remove(var)
        var.value = None

    return False


def main():
    rows, cols = input_parser()
    variables = []
    for i in range(len(rows)):
        variables.append(Variable('row', i, tuple(rows[i])))
    for i in range(len(cols)):
        variables.append(Variable('col', i, tuple(cols[i])))

    assigned = []
    result = CSP_backtracking(variables, assigned)
    if result:
        for var in assigned:
            print(var.gtype, var.place, var.value)

    else:
        print('could not find answer')


def input_parser():
    row, col = input().split()

    data = []
    for i in range(int(row)):
        dummy = input().split()
        data.append(dummy)

    rows = []
    cols = []
    data = np.array(data, dtype='object')
    for i in range(data.shape[0]):
        rows.append(list(data[i]))
    for j in range(data.shape[1]):
        cols.append(list(data[:, j]))

    for i in range(len(rows)):
        for j in range(len(rows[i])):
            if rows[i][j] != '-':
                rows[i][j] = int(rows[i][j])
            else:
                rows[i][j] = None

            if cols[i][j] != '-':
                cols[i][j] = int(cols[i][j])
            else:
                cols[i][j] = None

    return rows, cols


if __name__ == '__main__':
    main()
