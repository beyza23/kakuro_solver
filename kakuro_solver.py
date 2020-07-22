import functools
import itertools
import json
import numpy as np

# TODO: extend the solution by variable puzzle sizes
MAX_PUZZLE_HEIGHT_IN_CELLS = 3
MAX_PUZZLE_WIDTH_IN_CELLS = 3

# kakuro rules
ALLOWED_CELL_VALUES = list(range(1, 10))
ALLOWED_GROUP_SUMS = list(range(3, sum(ALLOWED_CELL_VALUES)+1))

FILEPATH = "C:\\Users\\Beyza\\Desktop\\python_projects\\kakuro_solver\\3x3_example_1.json"

class CellGroup:
    """
    Class represeting a vertical or horizontal group of cells
    that belong to same sum.
    """

    def __init__(
            self, 
            sum_value,
            row_num,
            column_num
        ):

        self.sum_value = sum_value
        self.row_num = row_num
        self.column_num = column_num
        self.cells = []
        self._possible_combinations = None

    @property
    def possible_combinations(self):
        if self._possible_combinations is None:
            self._possible_combinations =  [seq for seq in itertools.combinations(ALLOWED_CELL_VALUES, len(self.cells))
                                                                                  if sum(seq) == self.sum_value]
        return self._possible_combinations

    def remove_impossible_values_from_cells(self):
        possible_cell_values = set(itertools.chain.from_iterable(self.possible_combinations))
        for cell in self.cells:
            cell.possible_values = [value for value in cell.possible_values if value in possible_cell_values]

    def remove_duplicate_values(self):
        for cell in self.cells:
            if len(cell.possible_values) != 1:
                continue
            fixed_value = cell.possible_values[0]
            for next_cell in self.cells:
                if next_cell != cell:
                    try:
                        next_cell.possible_values.remove(fixed_value)
                    except ValueError:
                        pass

class Cell:

    def __init__(self, groups):
        self.possible_values = ALLOWED_CELL_VALUES[:]
        self.groups = groups
        self.value = 0
        for group in groups:
            group.cells.append(self)

class KakuroSolver:

    def __init__(self, groups, cells):
        self.groups = groups
        self.cells = cells

def load_kakuro_from_json(filepath):
    """
    Given a file path, return lists of CellGroup's.
    """
    with open(filepath, "r") as infile:
        kakuro_as_dict = json.load(infile)

    cell_groups = []

    # save the position of the kakuro numbers
    for row_number, row_values in kakuro_as_dict.items():
        row_number = int(row_number)
        if isinstance(row_values, list):
            for i, number in enumerate(row_values):
                cell_groups.append(CellGroup(number, row_num=row_number,
                                             column_num=i+1))
        else:
            cell_groups.append(CellGroup(row_values, row_num=row_number,
                                         column_num=0))
    return cell_groups

def create_cells_for(groups):
    cells = []
    for row_num in range(1, MAX_PUZZLE_HEIGHT_IN_CELLS+1):
        for column_num in range(1, MAX_PUZZLE_WIDTH_IN_CELLS+1):
            groups_for_cos = [cg for cg in groups if cg.row_num == row_num or
                                                     cg.column_num == column_num]
            cells.append(Cell(groups_for_cos))
    return cells

def _check_if_the_sum_is_correct(kakuro_solver):

    for cg in kakuro_solver.groups:
        sum_value = 0
        for cell in cg.cells:
            sum_value += cell.value
        if sum_value != cg.sum_value:
            return False

    return True

def _check_if_the_cell_value_repeating(kakuro_solver):

    for cg in kakuro_solver.groups:
        cell_values = []
        for cell in cg.cells:
            cell_values.append(cell.value)
        if len(cell_values) != len(set(cell_values)):
            return True

    return False

def _check_if_the_solution_is_correct(kakuro_solver):

    sum_is_correct = _check_if_the_sum_is_correct(kakuro_solver)
    is_value_repeating = _check_if_the_cell_value_repeating(kakuro_solver)

    if sum_is_correct and is_value_repeating == False:
        return True

    return False

def main():
    groups = load_kakuro_from_json(FILEPATH)
    cells = create_cells_for(groups)

    for cg in groups:
        cg.remove_impossible_values_from_cells()
    for cg in groups:
        cg.remove_duplicate_values()

    all_list = []
    for cell in cells:
        all_list.append(cell.possible_values)

    possible_solutions = list(itertools.product(*all_list))

    kakuro_solver = KakuroSolver(groups, cells)
    for possible_solution in possible_solutions:
        for i, cell in enumerate(kakuro_solver.cells):
            cell.value = possible_solution[i]
        is_solution_correct = _check_if_the_solution_is_correct(kakuro_solver)
        if is_solution_correct:
            for cell in kakuro_solver.cells:
                print(cell.value)

if __name__ == "__main__":
    main()