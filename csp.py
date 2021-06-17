"""

this module represents a CSP backtracking algorithm which can solve binary puzzle,
binary puzzle consists of an n * n table where n is an even number and
the player must place the numbers zero or one in the empty cells so that:
\n
    1- each row and each column must have an equal number of zeros and ones\n
    2- the numbers in each row and column must produce a unique string\n
    3- there should be no more than 2 duplicates in each row and column\n

for example, consider the table in four of the following:

    1   0   0   1\n
    0   1   1   0\n
    1   1   0   0\n
    0   0   1   1

    1- the number of rows in each row and column is equal to the number of one in that row and column\n
    2- the string columns 1010, 0110, 0101 and 1001 are unique, and the row strings are
    similarly unique\n
    3- in no row or column are more than two one or two zeros together

developed by\n
    Amin Habibollah\n
    Amirreza Naziri

"""

from itertools import product
import random
import numpy as np
import view
from copy import deepcopy
from time import perf_counter_ns


class Variable:
    """

    this class represents CSP variables , which is a row or column in this project formulation:
    each variable has an n size array which contains sequence of 0, 1 in each square,
    each variable has gtype field which specifies whether the variable is a row or a column,
    each variable has place field which specifies the row or column number of the variable

    """

    def __init__(self, gtype, place, initial_value):
        """

        constructor of Variable

        :param gtype: specifies whether the variable is a row or a column
        :param place: specifies the row or column number of the variable
        :param initial_value: Specifies the initial value of the variable with a n sized tuple
                                    for example (0, 0, 1, 0, None, 0) for 0 0 1 0 - 0

        """
        self.gtype = gtype
        self.place = place
        self.initial_value = initial_value
        self.value = None
        if None not in initial_value:
            self.value = initial_value
        self.domain = []
        self.unary_constrained()

    def unary_constrained(self):
        """

        this method creates the domain according to one-way constraints

        :return None

        """
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

                ok = True
                for i in range(len(value) - 2):
                    total = value[i] + value[i + 1] + value[i + 2]
                    if total > 2 or total == 0:
                        ok = False
                        break
                if not ok:
                    continue

                self.domain.append(value)


def MCdV(variables):
    """

    this function finds a list of most constrained variables and choose most
    constraining variable from this list

    :param variables: list of variables
    :return: a variable which is most constrained and also most constraining
                between most constrained variables

    """
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
    """

    this function finds most constraining variable

    :param most_constrained_variables: list of most constrained variables
    :return: most constraining variable

    """
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
    """

    this function represents forward checking algorithm

    :param var: newly assigned variable
    :param variables: list of all variables
    :return: false if the variable domain is depleted by running the algorithm,
                  otherwise true

    """
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


def MAC(var, variables):
    """

    this function represents MAC algorithm

    :param var: newly assigned variable
    :param variables: list of all variables
    :return: false if the variable domain is depleted by running the algorithm,
                  otherwise true

    """
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


def CSP_backtracking(variables, assigned, cons_algorithm=forward_checking):
    """

    this function represents CSP backtracking algorithm

    :param variables: list of all variables
    :param assigned: list of assigned variables
    :param cons_algorithm: constraint propagation algorithm which can be MAC or forward_checking
    :return: false if constraint propagation algorithm return false, true if every thing was okay

    """
    if len(assigned) == len(variables):
        return True

    var = MCdV(variables)

    for value in var.domain:
        var.value = value
        assigned.append(var)
        variables_copy = deepcopy(variables)
        result = cons_algorithm(var, variables_copy)
        if result:
            res = CSP_backtracking(variables_copy, assigned, cons_algorithm)
            if res:
                return True

        assigned.remove(var)
        var.value = None

    return False


def main():
    """

    main function

    :return: None

    """
    cons_propagation_type = int(input("Which constraint propagation algorithm would you prefer?\n 1) MAC\n 2) Forward "
                                      "Checking\n"))
    rows, cols, puzzle = input_parser()
    variables = []
    for i in range(len(rows)):
        variables.append(Variable('row', i, tuple(rows[i])))
    for i in range(len(cols)):
        variables.append(Variable('col', i, tuple(cols[i])))

    assigned = []
    # before = perf_counter_ns()
    if cons_propagation_type == 1:
        result = CSP_backtracking(variables, assigned, MAC)
    else:
        result = CSP_backtracking(variables, assigned, forward_checking)
    # after = perf_counter_ns()

    if result:
        for var in assigned:
            print(var.gtype, var.place, var.value)
        view.start(puzzle, assigned)

    else:
        print('could not find answer')

    # print(f'The elapsed time is: {after - before}')

    # for i in range(200):
    #     assigned = []
    #     variables2 = deepcopy(variables)
    #
    #     if cons_propagation_type == 1:
    #         result = CSP_backtracking(variables2, assigned, MAC)
    #     else:
    #         result = CSP_backtracking(variables2, assigned, forward_checking)
    #
    #     if result:
    #         # for var in assigned:
    #         #     print(var.gtype, var.place, var.value)
    #         # view.start(puzzle, assigned)
    #         pass
    #
    #
    #     else:
    #         print('could not find answer')


def input_parser():
    """

    this function parse user input and finds puzzle 2D array , 2D rows array, 2D columns array

    :return: rows 2D array, columns 2D array, puzzle 2D array

    """
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

    return rows, cols, data


if __name__ == '__main__':
    main()
