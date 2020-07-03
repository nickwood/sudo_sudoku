from sudoku import Grid
from sudoku import strategies


ALL_VALUES = frozenset('123456789')


# TODO MOVE TO RESPONSE GEN
def invalid(*, grid):
    invalid = set()
    for cell in Grid.grid_iterator():
        cell_value = grid.get(cell, '')
        if cell_value not in (ALL_VALUES | {''}):
            invalid.add(cell)
    return invalid


class Solution(Grid):
    def __init__(self, *, grid, solvers=None):
        self.errors = set()
        self.logs = []
        self.strategies_ = strategies.allowed(params=solvers)
        super().__init__(grid=grid)

    def solve(self):
        changed = True
        while changed:
            changed = self.solve_step()
            if self.errors:
                return False

        if self.is_solved():
            return True
        else:
            self.add_error(msg='Unable to solve with current methods')
            return False

    def solve_step(self):
        # print({k: v for k, v in self.grid.items() if v != ''})
        for strategy_ in self.strategies_:
            strategy_(game=self, logs=self.logs)
            if strategy_(game=self, logs=self.logs).attempt():
                return True
        return False
        # TODO: move to standalone method?
        # for cell, candidates in self.candidates_.items():
        #     if candidates == set():
        #         msg = 'No remaining candidates for %s' % cell
        #         self.add_error(msg=msg, cells={cell})

    def add_error(self, *, msg, cells={}):
        self.errors.add(msg)
        if cells:
            self.add_invalid(cells=cells)
