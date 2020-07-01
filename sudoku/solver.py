from itertools import chain, combinations, product
from sudoku.grid import Grid


ALL_ROWS = frozenset('ABCDEFGHJ')
ALL_COLS = frozenset('123456789')
ALL_VALUES = frozenset('123456789')
ROW_GROUPS = ['ABC', 'DEF', 'GHJ']
COL_GROUPS = ['123', '456', '789']

NAME_OF_MULTIPLE = {1: 'single',
                    2: 'pair',
                    3: 'triple',
                    4: 'quad'}


# TODO MOVE TO RESPONSE GEN
def invalid(*, grid):
    invalid = set()
    for cell in Grid.grid_iterator():
        cell_value = grid.get(cell, '')
        if cell_value not in (ALL_VALUES | {''}):
            invalid.add(cell)
    return invalid


class Game(Grid):
    def __init__(self, *, grid, solvers=None):
        self.errors = set()
        self.logs = []
        self.solvers = self.init_solvers(solvers=solvers)
        super().__init__(grid=grid)

    def init_solvers(self, *, solvers):
        methods = {'naked_singles': self.find_naked_singles,
                   'hidden_singles': self.find_hidden_singles,
                   'naked_pairs': self.find_naked_pairs,
                   'naked_triples': self.find_naked_triples,
                   'naked_quads': self.find_naked_quads,
                   'pointing_multiples': self.find_pointing_multiples,
                   'box_line_reductions': self.find_box_line_reductions,
                   'x_wings': self.find_x_wings,
                   'y_wings': self.find_y_wings}
        return [m for k, m in methods.items()
                if solvers.get(k) is True or solvers.get(k) == 'True']

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
            for k in sorted(self.candidates_.keys()):
                print(f"{k}: {sorted(self.candidates_[k])}")
            return False

    def is_solved(self):
        for group in Grid.group_iterator():
            if self.values_in_group(group=group) != ALL_VALUES:
                return False
        return True

    def solve_step(self):
        print({k: v for k, v in self.grid.items() if v != ''})
        for method in self.solvers:
            if method() is True:
                return True

        # TODO: move to standalone method?
        for cell, candidates in self.candidates_.items():
            if candidates == set():
                msg = 'No remaining candidates for %s' % cell
                self.add_error(msg=msg, cells={cell})

    def add_error(self, *, msg, cells={}):
        self.errors.add(msg)
        if cells:
            self.add_invalid(cells=cells)

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

    def find_naked_singles(self):
        found = set()
        for cell, values in self.candidates_.items():
            if len(values) == 1:
                val, = values
                found.add((cell, next(iter(values))))

        if found:
            for (c, v) in found:
                self.logs.append("Naked single at %s: %s" % (c, v))
                self.add_to_grid(cell=c, value=v)
            return True
        else:
            return False

    def find_naked_x(self, x):
        naked_x = set()
        for group in Grid.group_iterator():
            unsolved = self.unsolved_in_group(group=group)
            if len(unsolved) <= x:
                continue
            for x_set in combinations(unsolved, x):
                cands = frozenset(self.candidates_in_group(group=x_set))
                if len(cands) == x:
                    naked_x.add((frozenset(x_set), cands))
        if naked_x:
            for cells, values in naked_x:
                resp = False
                common = self.unsolved_common_neighbours(cells=cells)
                cwc = self.cells_with_candidates(group=common, values=values)
                if cwc:
                    resp = True
                    self.logs.append(f"Naked {NAME_OF_MULTIPLE[x]} at "
                                     f"{tuple(cells)}: {tuple(values)}")
                    self.remove_candidates(group=cwc, values=values)
            return resp
        else:
            return False

    def find_naked_pairs(self):
        return self.find_naked_x(2)

    def find_naked_triples(self):
        return self.find_naked_x(3)

    def find_naked_quads(self):
        return self.find_naked_x(4)

    def find_hidden_singles(self):
        hidden_singles = set()
        for group in Grid.group_iterator():
            for cand in self.candidates_in_group(group=group):
                possible = self.cells_with_candidate(group=group, value=cand)
                if len(possible) == 1:
                    hidden_singles.add((next(iter(possible)), cand))

        if hidden_singles:
            for (c, v) in hidden_singles:
                self.logs.append("Hidden single at %s: %s" % (c, v))
                self.add_to_grid(cell=c, value=v)
            return True
        else:
            return False

    def find_pointing_multiples(self):
        pointing_multiples = set()
        for box in Grid.box_iterator():
            for cand in self.candidates_in_group(group=box):
                cwc = self.cells_with_candidate(group=box, value=cand)
                # nobs = neighbours_outside_box
                nobs = Grid.common_neighbours(cells=cwc) - box
                nobs_with_c = self.cells_with_candidate(group=nobs, value=cand)
                if nobs_with_c:
                    self.logs.append(f"Pointing {NAME_OF_MULTIPLE[len(cwc)]} "
                                     f"at {cwc}: {cand}. "
                                     f"Removing from {list(nobs_with_c)}")
                    pointing_multiples.add((frozenset(nobs_with_c), cand))

        if pointing_multiples:
            for (cells, v) in pointing_multiples:
                self.remove_candidate(group=cells, value=v)
            return True
        else:
            return False

    def find_box_line_reductions(self):
        bl_reductions = set()
        for line in chain(Grid.row_iterator(), Grid.col_iterator()):
            for cand in self.candidates_in_group(group=line):
                cwc = self.cells_with_candidate(group=line, value=cand)
                if Grid.in_same_box(group=cwc):
                    rest_of_box = Grid.cells_in_box(next(iter(cwc))) - cwc
                    rest_with_c = self.cells_with_candidate(group=rest_of_box,
                                                            value=cand)
                    if rest_with_c:
                        self.logs.append(f"Box-line reduction with "
                                         f" {cwc}: {cand}. "
                                         f"Removing from {list(rest_with_c)}")
                        bl_reductions.add((frozenset(rest_with_c), cand))
        if bl_reductions:
            for (cells, v) in bl_reductions:
                self.remove_candidate(group=cells, value=v)
            return True
        else:
            return False

    def find_x_wings(self):
        x_wings = set()
        for rectangle in self.empty_rectangles():
            shared_cands = self.shared_candidates(group=rectangle)
            for c in shared_cands:
                # top left, top right, bottom left, bottom right
                tl, tr, bl, br = rectangle
                r1 = Grid.cells_in_row(tl)
                r2 = Grid.cells_in_row(bl)
                c1 = Grid.cells_in_col(tl)
                c2 = Grid.cells_in_col(tr)

                r1_with_c = self.cells_with_candidate(group=r1, value=c)
                r2_with_c = self.cells_with_candidate(group=r2, value=c)
                c1_with_c = self.cells_with_candidate(group=c1, value=c)
                c2_with_c = self.cells_with_candidate(group=c2, value=c)

                if (len(r1_with_c) == 2 and len(r2_with_c) == 2 and
                        (len(c1_with_c) > 2 or len(c2_with_c) > 2)):
                    locked = set(rectangle)
                    remove_from = frozenset((c1_with_c | c2_with_c) - locked)
                    x_wings.add((tuple(rectangle), c, remove_from))

                if (len(c1_with_c) == 2 and len(c2_with_c) == 2 and
                        (len(r1_with_c) > 2 or len(r2_with_c) > 2)):
                    locked = set(rectangle)
                    remove_from = frozenset((r1_with_c | r2_with_c) - locked)
                    x_wings.add((tuple(rectangle), c, remove_from))

        if x_wings:
            for (rectangle, v, remove_from) in x_wings:
                self.logs.append(f"X_wing at {rectangle}: removing {v} as "
                                 f"candidate from: {tuple(remove_from)}")
                self.remove_candidate(group=remove_from, value=v)
            return True
        else:
            return False

    def find_y_wings(self):
        cells_with_two_candidates = {c: cands
                                     for c, cands in self.candidates_.items()
                                     if len(cands) == 2}

        def shared(c1, c2):
            return self.shared_candidates(group={c1, c2})

        y_wings = set()
        for cell in cells_with_two_candidates:
            neighbours = Grid.all_neighbours(cell=cell, inc=False)
            to_consider = {n for n in cells_with_two_candidates.keys()
                           if n in neighbours
                           if len(shared(n, cell)) == 1}

            for n1, n2 in combinations(to_consider, 2):

                if (shared(n1, cell) != shared(n2, cell)
                        and (v := shared(n1, n2))):
                    cand = next(iter(v))
                    ucn = self.unsolved_common_neighbours(cells=(n1, n2))
                    updates = self.cells_with_candidate(group=ucn, value=cand)
                    if updates:
                        self.logs.append(f"Y-wing with hinge at {cell}: "
                                         f" wings: {n1} & {n2}. "
                                         f"Removing {cand} from {updates}")
                        y_wings.add((frozenset(updates), cand))

        if y_wings:
            for (cells, cand) in y_wings:
                self.remove_candidate(group=cells, value=cand)
            return True
        else:
            return False
