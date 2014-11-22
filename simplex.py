from string import ascii_lowercase
from fractions import Fraction

VARS = ascii_lowercase[-3:] + ascii_lowercase[:-3]


def print_func(coefficients):
    signs = {
        1: " + ",
        -1: " - ",
        0: ""
    }
    fnc_str = "{:s}{:s}".format(str(coefficients[0]), VARS[0])
    for constant, var in zip(coefficients[1:], VARS[1:]):
        sign = signs[cmp(constant, 0)]
        if sign:
            if abs(constant) == 1:
                fnc_str += "{:s}{:s}".format(sign, var)
            else:
                fnc_str += "{:s}{:s}{:s}".format(sign, str(abs(constant)), var)
    return fnc_str


def print_problem(objective, constraint_array, constraint_constants, is_equality=False):
    problem_str = "We seek to minimize the function\n\nZ = {:s}\n\n".format(print_func(objective))
    problem_str += "Subject to the constraints\n\n"
    if is_equality:
        comparator = " = "
    else:
        comparator = " <= "
    for constraint, constraint_constant in zip(constraint_array, constraint_constants):
        problem_str += "{:s}{:s}{:s}\n".format(print_func(constraint), comparator, str(constraint_constant))

    problem_str += "\nand the constraint that each variable must be nonnegative.\n"
    return problem_str


def simplex(objective, constraint_array, constraint_constants, is_equality=False):
    problem_str = print_problem(objective, constraint_array, constraint_constants, is_equality)
    tab = tableaux(objective, constraint_array, constraint_constants)
    problem_str += "\n\nThe canonical tableaux is\n"
    problem_str += pretty_print(tab) + "\n"
    while any(j > 0 for j in tab[0][1:]):
        row, col = pivot_coords(tab)
        problem_str += "Select row {:d}, column {:d} as the pivot and reduce to get\n".format(row + 1, col + 1)
        reduce_mat(tab)
        problem_str += pretty_print(tab) + "\n"

    problem_str += "Now the first row is entirely nonpositive, so the minimum value of Z is {:s}".format(tab[0][-1])
    return problem_str


def tableaux(objective, constraint_array, constraint_constants, is_equality=False):
    num_slack_variables = len(constraint_array)
    tab = [[1]]
    for j in objective:
        tab[-1].append(-j)
    tab[-1] += [0 for _ in range(num_slack_variables + 1)]

    for row_num, row in enumerate(constraint_array):
        tab.append([0])
        tab[-1] += row
        tab[-1] += [int(slack_var_idx == row_num) for slack_var_idx in range(num_slack_variables)]
        tab[-1].append(constraint_constants[row_num])
    for j in range(len(tab)):
        tab[j] = [Fraction(k, 1) for k in tab[j]]
    return tab


def pivot_columns(tableaux_mat):
    transposed = map(list, zip(*tableaux_mat))[:-1]  # hack way of transposing list of lists, dropping the last column
    not_pivot = [0 for _ in range(len(transposed[0]) - 1)] + [1]
    return [col_idx for col_idx, col in enumerate(transposed) if
            sorted(col) != not_pivot and tableaux_mat[0][col_idx] > 0]


def pivot_coords(tableaux_mat):
    pivot_col = min(pivot_columns(tableaux_mat))  # this could be any column in this list
    pivot_row = min(
        [row_idx for row_idx in range(len(tableaux_mat)) if row_idx > 0 and tableaux_mat[row_idx][pivot_col] > 0],
        key=lambda j: tableaux_mat[j][-1] / tableaux_mat[j][pivot_col])
    return pivot_row, pivot_col


def reduce_mat(tableaux_mat):
    pivot_row, pivot_col = pivot_coords(tableaux_mat)
    pivot = tableaux_mat[pivot_row][pivot_col]
    tableaux_mat[pivot_row] = [entry / pivot for entry in tableaux_mat[pivot_row]]
    for row_idx, row in enumerate(tableaux_mat):
        if row_idx != pivot_row:
            multiple = row[pivot_col]
            tableaux_mat[row_idx] = [row_entry - pivot_entry * multiple for row_entry, pivot_entry in
                                     zip(row, tableaux_mat[pivot_row])]


def pretty_print(matrix):
    str_matrix = [["|"] + map(str, row) + ["|"] for row in matrix]
    longest_str = max(max(len(entry) for entry in row) for row in str_matrix) + 2
    return "\n" + "\n".join("".join(entry.ljust(longest_str) for entry in row) for row in str_matrix) + "\n"


def main():
    print(simplex([-2, -3, -4], [[3, 2, 1], [2, 5, 3]], [10, 15]))


if __name__ == '__main__':
    main()