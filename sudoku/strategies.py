from abc import ABC, abstractmethod
from functools import partial
from itertools import chain, combinations
# from sudoku

NAME_OF_MULTIPLE = {1: 'single',
                    2: 'pair',
                    3: 'triple',
                    4: 'quad'}


def all():
    STRATEGIES = {'naked_single': NakedSingle,
                  'hidden_single': HiddenSingle,
                  'naked_pair': partial(NakedX, x=2),
                  'naked_triple': partial(NakedX, x=3),
                  'naked_quad': partial(NakedX, x=4),
                  'pointing_multiple': PointingMultiple,
                  'box_line_reduction': BoxLineReduction,
                  'x_wing': XWing,
                  'y_wing': YWing}
    return STRATEGIES


class Strategy(ABC):
    def __init__(self, *, game, logs=[]):
        self.game = game
        self.logs = logs
        self.results = set()

    @abstractmethod
    def attempt(self, logs):
        pass

    def add_values_to_grid(self):
        if not self.results:
            return False
        for (c, v) in self.results:
            self.game.add_to_grid(cell=c, value=v)
        return True

    def remove_candidates_from_group(self):
        if not self.results:
            return False
        for cells, values in self.results:
            self.game.remove_candidates(group=cells, values=values)
        return True


class NakedSingle(Strategy):
    def attempt(self):
        for cell, values in self.game.candidates_.items():
            if len(values) == 1:
                val, = values
                self.logs.append("Naked single at %s: %s" % (cell, val))
                self.results.add((cell, val))
        return self.add_values_to_grid()


class HiddenSingle(Strategy):
    def attempt(self):
        for group in self.game.group_iterator():
            for cand in self.game.candidates_in_group(group=group):
                locs = self.game.cells_with_candidate(group=group, value=cand)
                if len(locs) == 1:
                    cell, = locs
                    self.logs.append("Hidden single at %s: %s" % (cell, cand))
                    self.results.add((cell, cand))
        return self.add_values_to_grid()


class NakedX(Strategy):
    def __init__(self, *, x, game, logs):
        self.x = x
        super().__init__(game=game, logs=logs)

    def attempt(self):
        for group in self.game.group_iterator():
            unsolved = self.game.unsolved_in_group(group=group)
            if len(unsolved) <= self.x:
                continue
            for x_set in combinations(unsolved, self.x):
                cands = frozenset(self.game.candidates_in_group(group=x_set))

                if len(cands) == self.x:
                    common = self.game.unsolved_common_neighbours(cells=x_set)
                    if cwc := self.game.cells_with_candidates(group=common,
                                                              values=cands):
                        self.logs.append(f"Naked {NAME_OF_MULTIPLE[self.x]} "
                                         f"at {tuple(x_set)}: {tuple(cands)}")
                        self.results.add((frozenset(cwc), cands))
        return self.remove_candidates_from_group()


class PointingMultiple(Strategy):
    def attempt(self):
        for box in self.game.box_iterator():
            for cand in self.game.candidates_in_group(group=box):
                cwc = self.game.cells_with_candidate(group=box, value=cand)
                # nobs = neighbours_outside_box
                nobs = self.game.common_neighbours(cells=cwc) - box
                nobs_with_c = self.game.cells_with_candidate(group=nobs,
                                                             value=cand)
                if nobs_with_c:
                    self.logs.append(f"Pointing {NAME_OF_MULTIPLE[len(cwc)]} "
                                     f"at {cwc}: {cand}. "
                                     f"Removing from {list(nobs_with_c)}")
                    self.results.add((frozenset(nobs_with_c),
                                      frozenset(cand)))
        return self.remove_candidates_from_group()


class BoxLineReduction(Strategy):
    def attempt(self):
        for line in chain(self.game.row_iterator(), self.game.col_iterator()):
            for cand in self.game.candidates_in_group(group=line):
                cwc = self.game.cells_with_candidate(group=line, value=cand)
                if self.game.in_same_box(group=cwc):
                    others = self.game.cells_in_box(next(iter(cwc))) - cwc
                    rest_with_c = self.game.cells_with_candidate(group=others,
                                                                 value=cand)
                    if rest_with_c:
                        self.logs.append(f"Box-line reduction with "
                                         f" {cwc}: {cand}. "
                                         f"Removing from {list(rest_with_c)}")
                        self.results.add((frozenset(rest_with_c),
                                          frozenset(cand)))
        return self.remove_candidates_from_group()


class XWing(Strategy):
    def attempt(self):
        game = self.game
        for rectangle in game.empty_rectangles():
            shared_cands = game.shared_candidates(group=rectangle)
            for c in shared_cands:
                # top left, top right, bottom left, bottom right
                tl, tr, bl, br = rectangle
                r1 = game.cells_in_row(tl)
                r2 = game.cells_in_row(bl)
                c1 = game.cells_in_col(tl)
                c2 = game.cells_in_col(tr)

                r1_with_c = game.cells_with_candidate(group=r1, value=c)
                r2_with_c = game.cells_with_candidate(group=r2, value=c)
                c1_with_c = game.cells_with_candidate(group=c1, value=c)
                c2_with_c = game.cells_with_candidate(group=c2, value=c)

                if (len(r1_with_c) == 2 and len(r2_with_c) == 2 and
                        (len(c1_with_c) > 2 or len(c2_with_c) > 2)):
                    locked = set(rectangle)
                    remove_from = frozenset((c1_with_c | c2_with_c) - locked)
                    self.results.add((remove_from, frozenset(c)))

                if (len(c1_with_c) == 2 and len(c2_with_c) == 2 and
                        (len(r1_with_c) > 2 or len(r2_with_c) > 2)):
                    locked = set(rectangle)
                    remove_from = frozenset((r1_with_c | r2_with_c) - locked)
                    self.logs.append(f"X-wing at {rectangle}: removing {c} as "
                                     f"candidate from: {tuple(remove_from)}")
                    self.results.add((remove_from, frozenset(c)))
        return self.remove_candidates_from_group()


class YWing(Strategy):
    def attempt(self):
        game = self.game
        cells_with_two_candidates = {c: cands
                                     for c, cands in game.candidates_.items()
                                     if len(cands) == 2}

        def shared(c1, c2):
            return game.shared_candidates(group={c1, c2})

        for cell in cells_with_two_candidates:
            neighbours = game.all_neighbours(cell=cell, inc=False)
            to_consider = {n for n in cells_with_two_candidates.keys()
                           if n in neighbours
                           if len(shared(n, cell)) == 1}

            for n1, n2 in combinations(to_consider, 2):

                if (shared(n1, cell) != shared(n2, cell)
                        and (v := shared(n1, n2))):
                    cand = next(iter(v))
                    ucn = game.unsolved_common_neighbours(cells=(n1, n2))
                    updates = game.cells_with_candidate(group=ucn, value=cand)
                    if updates:
                        self.logs.append(f"Y-wing with hinge at {cell}: "
                                         f" wings: {n1} & {n2}. "
                                         f"Removing {cand} from {updates}")
                        self.results.add((frozenset(updates),
                                          frozenset(cand)))
        return self.remove_candidates_from_group()
