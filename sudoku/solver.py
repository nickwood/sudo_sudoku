from collections import defaultdict
from itertools import combinations
from functools import lru_cache


ALL_ROWS = frozenset('ABCDEFGHJ')
ALL_COLS = frozenset('123456789')
ALL_VALUES = frozenset('123456789')
ROW_GROUPS = ['ABC', 'DEF', 'GHJ']
COL_GROUPS = ['123', '456', '789']


def invalid(*, grid):
    invalid = set()
    for cell in grid_iterator():
        cell_value = grid.get(cell, '')
        if cell_value not in (ALL_VALUES | {''}):
            invalid.add(cell)
    return invalid


def grid_iterator():
    return (row + col for row in ALL_ROWS for col in ALL_COLS)


def group_iterator():
    for c in ['A1', 'D2', 'G3', 'B4', 'E5', 'H6', 'C7', 'F8', 'J9']:
        yield cells_in_row(cell=c)
        yield cells_in_col(cell=c)
        yield cells_in_box(cell=c)


@lru_cache(None)
def cells_in_row(*, cell, inc=True):
    row, _ = cell
    if inc:
        return frozenset(row + col for col in ALL_COLS)
    else:
        return frozenset(row + col for col in ALL_COLS) - {cell}


@lru_cache(None)
def cells_in_col(*, cell, inc=True):
    _, col = cell
    if inc:
        return frozenset(row + col for row in ALL_ROWS)
    else:
        return frozenset(row + col for row in ALL_ROWS) - {cell}


@lru_cache(None)
def cells_in_box(*, cell, inc=True):
    row, col = cell
    for i in COL_GROUPS:
        if col in i:
            col_group = i
            break

    for j in ROW_GROUPS:
        if row in j:
            row_group = j
            break

    box = frozenset(row + col for row in row_group for col in col_group)
    if inc:
        return box
    else:
        return box - {cell}


@lru_cache(None)
def all_neighbours(*, cell, inc=True):
    return (cells_in_row(cell=cell, inc=inc) |
            cells_in_col(cell=cell, inc=inc) |
            cells_in_box(cell=cell, inc=inc))


def common_neighbours(*, cells, inc=True):
    neighbourhoods = [all_neighbours(cell=c, inc=inc)
                      for c in cells]
    return frozenset.intersection(*neighbourhoods)


class Game:
    def __init__(self, *, grid, params=None):
        self.initial_grid = grid.copy()
        self.grid = grid
        self.params = params
        self.errors = set()
        self.invalid_cells = set()
        self.candidates_ = None
        self.solvers = self.init_solvers(params=params)

    def init_solvers(self, *, params):
        methods = {'find_naked_singles': self.find_naked_singles,
                   'find_hidden_singles': self.find_hidden_singles,
                   'find_naked_pairs': self.find_naked_pairs,
                   'find_naked_triples': self.find_naked_triples,
                   'find_naked_quads': self.find_naked_quads}
        return [m for k, m in methods.items()
                if params.get(k) is True or params.get(k) == 'True']

    def initialise_candidates(self):  # TODO: move to __init__
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
        if self.candidates_ is None:
            self.initialise_candidates()
        for method in self.solvers:
            if modified := method():
                if modified is True:
                    # TODO: make it easier to call simple methods
                    modified = False
                    for method in [self.find_naked_singles,
                                   self.find_hidden_singles]:
                        if entries := method():
                            modified = entries
                            break
                if modified:
                    for (c, v) in modified:
                        self.add_to_grid(cell=c, value=v)
                    break
        for cell, candidates in self.candidates_.items():
            if candidates == set():
                msg = 'No remaining candidates for %s' % cell
                self.add_error(msg=msg, cells={cell})

    def add_error(self, *, msg, cells={}):
        self.errors.add(msg)
        for cell in cells:
            self.invalid_cells.add(cell)

    def remove_candidates(self, *, group, values):
        for c in group:
            if self.candidates_.get(c):
                self.candidates_[c] -= values

    def add_to_grid(self, *, cell, value):
        '''update the grid with the given cell & value, also removes this value
        from the list of candidates for all it's neighbours'''
        self.grid[cell] = value
        del self.candidates_[cell]
        to_update = self.unsolved_in_group(group=all_neighbours(cell=cell))
        self.remove_candidates(group=to_update, values={value})

    def values_in_group(self, *, group):
        '''takes an iterator of cell references and returns the unique values
        occupying those cells (ignores empty cells)'''
        return set(self.grid.get(c, None) for c in group) - {None}

    def values_not_in_group(self, *, group):
        return set(ALL_VALUES - self.values_in_group(group=group))

    def candidates_in_group(self, *, group):
        return set.union(*[self.candidates_.get(c, set()) for c in group])

    def solved_cell(self, *, cell):
        '''return True if cell is solved (or provided) False otherwise'''
        if self.grid.get(cell) in ALL_VALUES:
            return True
        else:
            return False

    def solved_in_group(self, *, group):
        '''take a group of cells and return only those which are solved'''
        return {c for c in group if self.solved_cell(cell=c)}

    def unsolved_in_group(self, *, group):
        '''take a group of cells and return only those which are unsolved'''
        return {c for c in group if not self.solved_cell(cell=c)}

    def unsolved_common_neighbours(self, *, cells):
        return self.unsolved_in_group(group=common_neighbours(cells=cells,
                                                              inc=False))

    def find_naked_singles(self):
        naked_singles = []
        for cell, values in self.candidates_.items():
            if len(values) == 1:
                val, = values
                naked_singles.append((cell, val))
        # TODO: logging
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
                        self.add_error(msg=msg, cells={cell})
        # TODO: logging
        return hidden_singles.items()

    def find_naked_x(self, x):
        naked_x = set()
        for group in group_iterator():
            unsolved = self.unsolved_in_group(group=group)
            if len(unsolved) <= x:
                continue
            for x_set in combinations(unsolved, x):
                cands = frozenset(self.candidates_in_group(group=x_set))
                if len(cands) == x:
                    naked_x.add((frozenset(x_set), cands))
        if naked_x:
            for cells, values in naked_x:
                neighbours = self.unsolved_common_neighbours(cells=cells)
                self.remove_candidates(group=neighbours, values=values)
            return True
        else:
            return False

    def find_naked_pairs(self):
        return self.find_naked_x(2)

    def find_naked_triples(self):
        return self.find_naked_x(3)

    def find_naked_quads(self):
        return self.find_naked_x(4)
