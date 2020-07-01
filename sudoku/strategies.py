from abc import ABC, abstractmethod
from itertools import chain, combinations

NAME_OF_MULTIPLE = {1: 'single',
                    2: 'pair',
                    3: 'triple',
                    4: 'quad'}


def all():
    STRATEGIES = {'naked_single': NakedSingle,
                  'hidden_single': HiddenSingle,
                  'naked_pair': NakedPair,
                  'naked_triple': NakedTriple,
                  'naked_quad': NakedQuad,
                  'pointing_multiple': PointingMultiple,
                  'box_line_reduction': BoxLineReduction,
                  'x_wing': XWing,
                  'y_wing': YWing}
    return STRATEGIES


class Strategy(ABC):

    @abstractmethod
    def attempt(grid, logs):
        pass


class NakedSingle(Strategy):
    def attempt(grid, logs):
        found = set()
        for cell, values in grid.candidates_.items():
            if len(values) == 1:
                val, = values
                found.add((cell, next(iter(values))))

        if found:
            for (c, v) in found:
                logs.append("Naked single at %s: %s" % (c, v))
                grid.add_to_grid(cell=c, value=v)
            return True
        else:
            return False


class HiddenSingle(Strategy):
    def attempt(grid, logs):
        hidden_singles = set()
        for group in grid.group_iterator():
            for cand in grid.candidates_in_group(group=group):
                possible = grid.cells_with_candidate(group=group, value=cand)
                if len(possible) == 1:
                    hidden_singles.add((next(iter(possible)), cand))

        if hidden_singles:
            for (c, v) in hidden_singles:
                logs.append("Hidden single at %s: %s" % (c, v))
                grid.add_to_grid(cell=c, value=v)
            return True
        else:
            return False


def naked_x_attempt(grid, logs, x):
    naked_x = set()
    for group in grid.group_iterator():
        unsolved = grid.unsolved_in_group(group=group)
        if len(unsolved) <= x:
            continue
        for x_set in combinations(unsolved, x):
            cands = frozenset(grid.candidates_in_group(group=x_set))
            if len(cands) == x:
                naked_x.add((frozenset(x_set), cands))
    if naked_x:
        for cells, values in naked_x:
            resp = False
            common = grid.unsolved_common_neighbours(cells=cells)
            cwc = grid.cells_with_candidates(group=common, values=values)
            if cwc:
                resp = True
                logs.append(f"Naked {NAME_OF_MULTIPLE[x]} at "
                            f"{tuple(cells)}: {tuple(values)}")
                grid.remove_candidates(group=cwc, values=values)
        return resp
    else:
        return False


class NakedPair(Strategy):
    def attempt(grid, logs):
        return naked_x_attempt(grid=grid, logs=logs, x=2)


class NakedTriple(Strategy):
    def attempt(grid, logs):
        return naked_x_attempt(grid=grid, logs=logs, x=3)


class NakedQuad(Strategy):
    def attempt(grid, logs):
        return naked_x_attempt(grid=grid, logs=logs, x=4)


class PointingMultiple(Strategy):
    def attempt(grid, logs):
        pointing_multiples = set()
        for box in grid.box_iterator():
            for cand in grid.candidates_in_group(group=box):
                cwc = grid.cells_with_candidate(group=box, value=cand)
                # nobs = neighbours_outside_box
                nobs = grid.common_neighbours(cells=cwc) - box
                nobs_with_c = grid.cells_with_candidate(group=nobs, value=cand)
                if nobs_with_c:
                    logs.append(f"Pointing {NAME_OF_MULTIPLE[len(cwc)]} "
                                f"at {cwc}: {cand}. "
                                f"Removing from {list(nobs_with_c)}")
                    pointing_multiples.add((frozenset(nobs_with_c), cand))

        if pointing_multiples:
            for (cells, v) in pointing_multiples:
                grid.remove_candidate(group=cells, value=v)
            return True
        else:
            return False


class BoxLineReduction(Strategy):
    def attempt(grid, logs):
        bl_reductions = set()
        for line in chain(grid.row_iterator(), grid.col_iterator()):
            for cand in grid.candidates_in_group(group=line):
                cwc = grid.cells_with_candidate(group=line, value=cand)
                if grid.in_same_box(group=cwc):
                    rest_of_box = grid.cells_in_box(next(iter(cwc))) - cwc
                    rest_with_c = grid.cells_with_candidate(group=rest_of_box,
                                                            value=cand)
                    if rest_with_c:
                        logs.append(f"Box-line reduction with "
                                    f" {cwc}: {cand}. "
                                    f"Removing from {list(rest_with_c)}")
                        bl_reductions.add((frozenset(rest_with_c), cand))
        if bl_reductions:
            for (cells, v) in bl_reductions:
                grid.remove_candidate(group=cells, value=v)
            return True
        else:
            return False


class XWing(Strategy):
    def attempt(grid, logs):
        x_wings = set()
        for rectangle in grid.empty_rectangles():
            shared_cands = grid.shared_candidates(group=rectangle)
            for c in shared_cands:
                # top left, top right, bottom left, bottom right
                tl, tr, bl, br = rectangle
                r1 = grid.cells_in_row(tl)
                r2 = grid.cells_in_row(bl)
                c1 = grid.cells_in_col(tl)
                c2 = grid.cells_in_col(tr)

                r1_with_c = grid.cells_with_candidate(group=r1, value=c)
                r2_with_c = grid.cells_with_candidate(group=r2, value=c)
                c1_with_c = grid.cells_with_candidate(group=c1, value=c)
                c2_with_c = grid.cells_with_candidate(group=c2, value=c)

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
                logs.append(f"X-wing at {rectangle}: removing {v} as "
                            f"candidate from: {tuple(remove_from)}")
                grid.remove_candidate(group=remove_from, value=v)
            return True
        else:
            return False


class YWing(Strategy):
    def attempt(grid, logs):
        cells_with_two_candidates = {c: cands
                                     for c, cands in grid.candidates_.items()
                                     if len(cands) == 2}

        def shared(c1, c2):
            return grid.shared_candidates(group={c1, c2})

        y_wings = set()
        for cell in cells_with_two_candidates:
            neighbours = grid.all_neighbours(cell=cell, inc=False)
            to_consider = {n for n in cells_with_two_candidates.keys()
                           if n in neighbours
                           if len(shared(n, cell)) == 1}

            for n1, n2 in combinations(to_consider, 2):

                if (shared(n1, cell) != shared(n2, cell)
                        and (v := shared(n1, n2))):
                    cand = next(iter(v))
                    ucn = grid.unsolved_common_neighbours(cells=(n1, n2))
                    updates = grid.cells_with_candidate(group=ucn, value=cand)
                    if updates:
                        logs.append(f"Y-wing with hinge at {cell}: "
                                    f" wings: {n1} & {n2}. "
                                    f"Removing {cand} from {updates}")
                        y_wings.add((frozenset(updates), cand))

        if y_wings:
            for (cells, cand) in y_wings:
                grid.remove_candidate(group=cells, value=cand)
            return True
        else:
            return False
