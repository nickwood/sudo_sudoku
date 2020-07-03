from collections import defaultdict
from itertools import chain, combinations, product
from functools import lru_cache


ALL_ROWS = frozenset('ABCDEFGHJ')
ALL_COLS = frozenset('123456789')
ALL_VALUES = frozenset('123456789')
ROW_GROUPS = ['ABC', 'DEF', 'GHJ']
COL_GROUPS = ['123', '456', '789']


class Grid(dict):

    @staticmethod
    def grid_iterator():
        return (row + col for row in ALL_ROWS for col in ALL_COLS)

    @staticmethod
    @lru_cache(None)
    def cells_in_row(cell, inc=True):
        row, _ = cell
        if inc:
            return frozenset(row + col for col in ALL_COLS)
        else:
            return frozenset(row + col for col in ALL_COLS) - {cell}

    @staticmethod
    def row_iterator():
        for c in ['A1', 'D2', 'G3', 'B4', 'E5', 'H6', 'C7', 'F8', 'J9']:
            yield Grid.cells_in_row(cell=c)

    @staticmethod
    @lru_cache(None)
    def cells_in_col(cell, inc=True):
        _, col = cell
        if inc:
            return frozenset(row + col for row in ALL_ROWS)
        else:
            return frozenset(row + col for row in ALL_ROWS) - {cell}

    @staticmethod
    def col_iterator():
        for c in ['A1', 'D2', 'G3', 'B4', 'E5', 'H6', 'C7', 'F8', 'J9']:
            yield Grid.cells_in_col(cell=c)

    @staticmethod
    @lru_cache(None)
    def cells_in_box(cell, inc=True):
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

    @staticmethod
    def box_iterator():
        for c in ['A1', 'D2', 'G3', 'B4', 'E5', 'H6', 'C7', 'F8', 'J9']:
            yield Grid.cells_in_box(cell=c)

    @staticmethod
    def group_iterator():
        for g in chain(Grid.row_iterator(),
                       Grid.col_iterator(),
                       Grid.box_iterator()):
            yield g

    @staticmethod
    def in_same_box(group):
        'True if all cells in group are in the same box, False otherwise'
        box_containing_first = Grid.cells_in_box(next(iter(group)))
        for c in group:
            if c not in box_containing_first:
                return False
        return True

    @staticmethod
    @lru_cache(None)
    def all_neighbours(*, cell, inc=True):
        return (Grid.cells_in_row(cell=cell, inc=inc) |
                Grid.cells_in_col(cell=cell, inc=inc) |
                Grid.cells_in_box(cell=cell, inc=inc))

    @staticmethod
    def common_neighbours(*, cells, inc=True):
        neighbourhoods = [Grid.all_neighbours(cell=c, inc=inc)
                          for c in cells]
        return frozenset.intersection(*neighbourhoods)

    def __init__(self, *, grid):
        self.initial_grid = grid.copy()
        self.invalid_cells = set()
        self.grid = grid
        self.candidates_ = self.initialise_candidates()

    def initialise_candidates(self):
        candidates = defaultdict(set)
        grid = self.grid
        for cell in Grid.grid_iterator():
            if grid.get(cell, '') == '':
                neighbours = Grid.all_neighbours(cell=cell)
                values = self.values_not_in_group(group=neighbours)
                candidates[cell] = values
        return dict(candidates)

    def add_invalid(self, *, cells):
        self.invalid_cells |= cells

    def values_in_group(self, *, group):
        '''takes an iterator of cell references and returns the unique values
        occupying those cells (ignores empty cells)'''
        return set(self.grid.get(c, None) for c in group) - {None}

    def values_not_in_group(self, *, group):
        return set(ALL_VALUES - self.values_in_group(group=group))

    def add_to_grid(self, *, cell, value):
        '''update the grid with the given cell & value, also removes this value
        from the list of candidates for all it's neighbours'''
        self.grid[cell] = value
        if self.candidates_.get(cell, None):
            del self.candidates_[cell]
        neighbours = Grid.all_neighbours(cell=cell)
        self.remove_candidate(group=neighbours, value=value)

    def remove_candidate(self, *, group, value):
        self.remove_candidates(group=group, values={value})

    def remove_candidates(self, *, group, values):
        for c in group:
            if self.candidates_.get(c):
                self.candidates_[c] -= values

    def candidates_in_group(self, *, group):
        return set.union(*[self.candidates_.get(c, set()) for c in group])

    def shared_candidates(self, *, group):
        return set.intersection(*[self.candidates_.get(c, set())
                                  for c in group])

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
        common_neighbours = Grid.common_neighbours(cells=cells, inc=False)
        return self.unsolved_in_group(group=common_neighbours)

    def cells_with_candidate(self, *, group, value):
        '''return a set containing the cells in group which have 'value' as a
        candidate'''
        return {c for c in group if value in self.candidates_.get(c, set())}

    def cells_with_candidates(self, *, group, values):
        '''return a set containing the cells in group which any of 'values' in
        their candidates'''
        cells = set()
        for v in values:
            cells |= self.cells_with_candidate(group=group, value=v)
        return cells

    def empty_rectangles(self):
        '''generator function which successively returns a group of 4 empty
        cells on the corners of a rectangle
        NB. Due to the way these cells are found we can guarantee that elements
        0,1 & 2,3 will share rows and 0,2 and 1,3 share columns'''
        row_empties = {}
        for row_ref in ALL_ROWS:
            row = Grid.cells_in_row(cell=row_ref+'1', inc=True)
            empties = {c[1] for c in self.unsolved_in_group(group=row)}
            edge_sets = (product(row_ref + comp_row_ref, col_refs)
                         for comp_row_ref, comp_empties in row_empties.items()
                         if len(intersect := empties & comp_empties) >= 2
                         for col_refs in combinations(intersect, 2))
            for edge in edge_sets:
                yield sorted([r+c for r, c in edge])

            row_empties[row_ref] = empties

    def is_solved(self):
        for group in Grid.group_iterator():
            if self.values_in_group(group=group) != ALL_VALUES:
                return False
        return True
