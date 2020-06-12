from collections import defaultdict
from functools import lru_cache


ALL_COLS = frozenset('ABCDEFGHJ')
ALL_ROWS = frozenset('123456789')
ALL_VALUES = frozenset('123456789')
COL_GROUPS = ['ABC', 'DEF', 'GHJ']
ROW_GROUPS = ['123', '456', '789']


# TODO: consider moving to response_generators
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


def group_iterator():
    for c in ['A1', 'D2', 'G3', 'B4', 'E5', 'H6', 'C7', 'F8', 'J9']:
        yield cells_in_row(cell=c)
        yield cells_in_col(cell=c)
        yield cells_in_box(cell=c)


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
        self.errors = set()
        self.invalid_cells = set()

    def initialise_candidates(self):
        candidates = defaultdict(set)
        grid = self.grid
        for cell in grid_iterator():
            if grid.get(cell, '') == '':
                neighbours = all_neighbours(cell=cell)
                values = self.values_not_in_group(group=neighbours)
                candidates[cell] = values
        self.candidates_ = dict(candidates)

    def solve(self):
        self.initialise_candidates()
        old_state = None
        while old_state != self.grid:
            old_state = self.grid.copy()
            self.solve_step()
            if self.errors:
                return False
        if self.is_solved():
            return True
        else:
            self.add_error(msg='Unable to solve with current methods')
            return False

    def is_solved(self):
        for group in group_iterator():
            if self.values_in_group(group=group) != ALL_VALUES:
                return False
        return True

    def solve_step(self):
        for method in [self.find_naked_singles, self.find_hidden_singles]:
            if entries := method():
                for (c, v) in entries:
                    self.add_to_grid(cell=c, value=v)
                break
        for cell, candidates in self.candidates_.items():
            if candidates == set():
                msg = 'No remaining candidates for %s' % cell
                self.add_error(msg=msg, cell=cell)

    def add_error(self, *, msg, cell=None):
        self.errors.add(msg)
        if cell:
            self.invalid_cells.add(cell)

    def add_to_grid(self, *, cell, value):
        '''update the grid with the given cell & value, also removes this value
        from the list of candidates for all it's neighbours'''
        self.grid[cell] = value
        del self.candidates_[cell]
        for n in all_neighbours(cell=cell):
            if n in self.candidates_ and value in self.candidates_[n]:
                self.candidates_[n].remove(value)

    def values_in_group(self, *, group):
        '''takes an iterator of cell references and returns the unique values
        occupying those cells (ignores empty cells)'''
        return set(self.grid.get(c, None) for c in group) - {None}

    def values_not_in_group(self, *, group):
        return set(ALL_VALUES - self.values_in_group(group=group))

    # solvers

    def find_naked_singles(self):
        naked_singles = []
        for cell, values in self.candidates_.items():
            if len(values) == 1:
                val, = values
                naked_singles.append((cell, val))
        return naked_singles

    def find_hidden_singles(self):
        hidden_singles = {}

        for group in group_iterator():
            hidden_candidates = defaultdict(set)
            for c in (group & self.candidates_.keys()):
                for v in self.candidates_[c]:
                    hidden_candidates[v].add(c)

            for val, cells in hidden_candidates.items():
                if len(cells) == 1:
                    cell, = cells
                    if cell not in hidden_singles:
                        hidden_singles[cell] = val
                    elif hidden_singles[cell] != val:
                        hidden_singles[cell] = ''
                        msg = 'Conflicting hidden single at %s' % cell
                        self.add_error(msg=msg, cell=cell)
        return hidden_singles.items()
