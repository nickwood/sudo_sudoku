from collections import defaultdict
from functools import lru_cache


ALL_COLS = frozenset('ABCDEFGHJ')
ALL_ROWS = frozenset('123456789')
ALL_VALUES = frozenset('123456789')
COL_GROUPS = ['ABC', 'DEF', 'GHJ']
ROW_GROUPS = ['123', '456', '789']


def split_post(*, post_data):
    '''The raw post data conatins our entire form, which is a bit cumbersome
    to work with. This helper functrion splits it into two dicts, one contains
    the grid information, and the other contains everything else (e.g. solver
    contraints)'''
    grid_keys = set([k for k in grid_iterator()])
    grid_data = {key: post_data[key] for key in post_data.keys() & grid_keys}
    other_data = {key: post_data[key] for key in post_data.keys() - grid_keys}
    return grid_data, other_data


def invalid(*, grid):
    invalid = set()
    for cell in grid_iterator():
        cell_value = grid.get(cell, '')
        if cell_value not in (ALL_VALUES | {''}):
            invalid.add(cell)
    return invalid


def grid_iterator():
    return (col + row for row in ALL_ROWS for col in ALL_COLS)


ALL_CELLS = frozenset([cell for cell in grid_iterator()])


@lru_cache(None)
def cells_in_row(*, cell):
    _, row = cell
    return frozenset(col + row for col in ALL_COLS)


@lru_cache(None)
def cells_in_col(*, cell):
    col, _ = cell
    return frozenset(col + row for row in ALL_ROWS)


@lru_cache(None)
def cells_in_box(*, cell):
    for i in COL_GROUPS:
        if cell[0] in i:
            col_group = i
            break

    for j in ROW_GROUPS:
        if cell[1] in j:
            row_group = j
            break

    return frozenset(col + row for row in row_group for col in col_group)


@lru_cache(None)
def all_neighbours(*, cell):
    return (cells_in_row(cell=cell) |
            cells_in_col(cell=cell) |
            cells_in_box(cell=cell))


class Game:
    def __init__(self, *, grid, params):
        self.initial_grid = grid.copy()
        self.grid = grid
        self.params = params

    def initialise_candidates(self):
        candidates = defaultdict(set)
        grid = self.grid
        for cell in grid_iterator():
            if grid.get(cell, '') == '':
                values = set(ALL_VALUES - self.neighbour_values(cell=cell))
                candidates[cell] = values
        self.candidates_ = candidates

    def solve(self):
        self.initialise_candidates()
        old_state = None
        while old_state != self.grid:
            old_state = self.grid.copy()
            if entries := self.find_naked_singles():
                for (c, v) in entries:
                    self.add_to_grid(cell=c, value=v)
        return False

    def add_to_grid(self, *, cell, value):
        self.grid[cell] = value

        # update candidates
        del self.candidates_[cell]
        for n in all_neighbours(cell=cell):
            if n in self.candidates_ and value in self.candidates_[n]:
                self.candidates_[n].remove(value)

    def values_in_cells(self, *, cells):
        '''takes an iterator of cell references and returns the unique values
        occupying those cells (ignores empty cells)'''
        return set(self.grid.get(c, None) for c in cells) - {None}

    def values_in_row(self, *, cell):
        return self.values_in_cells(cells=cells_in_row(cell=cell))

    def values_in_col(self, *, cell):
        return self.values_in_cells(cells=cells_in_col(cell=cell))

    def values_in_box(self, *, cell):
        return self.values_in_cells(cells=cells_in_box(cell=cell))

    def neighbour_values(self, *, cell):
        return self.values_in_cells(cells=all_neighbours(cell=cell))

    # solvers

    def find_naked_singles(self):
        naked_singles = []
        for cell, values in self.candidates_.items():
            if len(values) == 1:
                val, = values
                naked_singles.append((cell, val))
        return naked_singles
