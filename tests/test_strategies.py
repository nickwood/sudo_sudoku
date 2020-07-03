from sudoku import strategies
from sudoku.grid import Grid


# TODO: test_all


class GridInstance():
    def __init__(self, *, grid):
        self.grid = grid.copy()

    def __enter__(self):
        g = Grid(grid=self.grid)
        return g

    def __exit__(self, *args, **kwargs):
        pass


NAKED_SINGLES = {'A1': '5', 'A2': '6', 'A4': '8', 'A5': '4', 'A6': '7',
                 'B1': '3', 'B3': '9', 'B7': '6', 'C3': '8', 'D2': '1',
                 'D5': '8', 'D8': '4', 'E1': '7', 'E2': '9', 'E4': '6',
                 'E6': '2', 'E8': '1', 'E9': '8', 'F2': '5', 'F5': '3',
                 'F8': '9', 'G7': '2', 'H3': '6', 'H7': '8', 'H9': '7',
                 'J4': '3', 'J5': '1', 'J6': '6', 'J8': '5', 'J9': '9'}


def test_naked_single():
    with GridInstance(grid=NAKED_SINGLES) as game:
        assert game.grid.get('H8') is None
        assert game.grid.get('J7') is None
        assert game.grid.get('F7') is None
        assert game.grid.get('E5') is None
        assert strategies.NakedSingle(game=game, logs=[]).attempt()
        assert game.grid['H8'] == '3'
        assert game.grid['J7'] == '4'
        assert game.grid['F7'] == '7'
        assert game.grid['E5'] == '5'


def test_hidden_single():
    with GridInstance(grid=NAKED_SINGLES) as game:
        assert strategies.HiddenSingle(game=game, logs=[]).attempt()
        exp_singles = [('A7', '9'), ('F1', '8'), ('G3', '5'), ('B8', '8'),
                       ('C5', '6'), ('C6', '3'), ('G5', '7'), ('E3', '4'),
                       ('G6', '8'), ('H1', '1'), ('G8', '6'), ('G9', '1')]

        for (c, v) in exp_singles:
            assert game.grid[c] == v


NAKED_PAIR = {'H7': '6', 'D3': '2', 'B3': '1', 'C6': '1', 'B6': '9',
              'D6': '5', 'B7': '7', 'J3': '6', 'J2': '8', 'E6': '6',
              'J6': '2', 'A1': '3', 'B8': '4', 'B2': '5', 'C3': '4',
              'C9': '8', 'D5': '7', 'D4': '9', 'C1': '7', 'J8': '5',
              'J1': '1', 'J7': '4', 'E7': '3', 'H2': '7', 'F3': '7',
              'D2': '3', 'C7': '5', 'E2': '1', 'J5': '9', 'H6': '4',
              'D7': '8', 'G3': '5', 'F6': '3', 'H3': '3', 'A2': '6',
              'A7': '1'}


def test_naked_pair():
    # TODO: test_unhappy_path
    with GridInstance(grid=NAKED_PAIR) as game:
        assert game.candidates_['A3'] == set(list('89'))
        assert game.candidates_['A4'] == set(list('24578'))
        assert game.candidates_['A5'] == set(list('2458'))
        assert game.candidates_['A6'] == set(list('78'))
        assert game.candidates_['A8'] == set(list('29'))
        assert game.candidates_['A9'] == set(list('29'))
        assert game.candidates_['B9'] == set(list('236'))
        assert game.candidates_['C8'] == set(list('2369'))
        assert strategies.NakedX(game=game, logs=[], x=2).attempt()
        assert game.candidates_['A3'] == set(list('8'))
        assert game.candidates_['A4'] == set(list('4578'))
        assert game.candidates_['A5'] == set(list('458'))
        assert game.candidates_['A6'] == set(list('78'))
        assert game.candidates_['A8'] == set(list('29'))
        assert game.candidates_['A9'] == set(list('29'))
        assert game.candidates_['B9'] == set(list('36'))
        assert game.candidates_['C8'] == set(list('36'))


NAKED_TRIPLE = {'C3': '7', 'E5': '2', 'A4': '7', 'A2': '2', 'G4': '2',
                'J4': '9', 'F6': '7', 'E6': '5', 'G2': '8', 'J7': '6',
                'B6': '2', 'H5': '5', 'H7': '9', 'F2': '9', 'F5': '4',
                'J6': '1', 'F8': '6', 'D8': '1', 'F4': '1', 'J9': '4',
                'B3': '8', 'E4': '6', 'B4': '5', 'D6': '3', 'J5': '8',
                'J8': '7', 'H6': '4', 'G8': '3', 'A5': '6', 'G6': '6',
                'C9': '6', 'C4': '4', 'H1': '7', 'D5': '9', 'G7': '5',
                'D4': '8', 'G9': '1', 'G5': '7', 'H4': '3', 'A1': '3',
                'G3': '9', 'C6': '8', 'C1': '9', 'A6': '9', 'D2': '7',
                'G1': '4'}


def test_naked_triple():
    # TODO: test_unhappy_path
    with GridInstance(grid=NAKED_TRIPLE) as game:
        assert game.candidates_['H2'] == set(list('16'))
        assert game.candidates_['H3'] == set(list('126'))
        assert game.candidates_['J1'] == set(list('25'))
        assert game.candidates_['J2'] == set(list('35'))
        assert game.candidates_['J3'] == set(list('235'))
        assert game.candidates_['A9'] == set(list('58'))
        assert game.candidates_['B9'] == set(list('379'))
        assert game.candidates_['D9'] == set(list('25'))
        assert game.candidates_['E9'] == set(list('3789'))
        assert game.candidates_['F9'] == set(list('2358'))
        assert game.candidates_['H9'] == set(list('28'))
        assert strategies.NakedX(game=game, logs=[], x=3).attempt()
        assert game.candidates_['H2'] == set(list('16'))
        assert game.candidates_['H3'] == set(list('16'))
        assert game.candidates_['J1'] == set(list('25'))
        assert game.candidates_['J2'] == set(list('35'))
        assert game.candidates_['J3'] == set(list('235'))
        assert game.candidates_['A9'] == set(list('58'))
        assert game.candidates_['B9'] == set(list('379'))
        assert game.candidates_['D9'] == set(list('25'))
        assert game.candidates_['E9'] == set(list('379'))
        assert game.candidates_['F9'] == set(list('3'))
        assert game.candidates_['H9'] == set(list('28'))


NAKED_QUAD = {'A5': '6', 'E5': '2', 'A2': '2', 'C4': '4', 'F6': '7',
              'J6': '1', 'A1': '3', 'J4': '9', 'G1': '4', 'G2': '8',
              'D2': '7', 'G7': '5', 'C6': '8', 'C3': '7', 'G5': '7',
              'J7': '6', 'A4': '7', 'D4': '8', 'G4': '2', 'H5': '5',
              'C9': '6', 'J8': '7', 'F5': '4', 'F2': '9', 'J9': '4',
              'J5': '8', 'B4': '5', 'D6': '3', 'G8': '3', 'D8': '1',
              'G3': '9', 'C1': '9', 'H1': '7', 'G6': '6', 'G9': '1',
              'H6': '4', 'A6': '9', 'B6': '2', 'B3': '8', 'E4': '6',
              'F8': '6', 'D5': '9', 'H7': '9', 'E6': '5', 'H4': '3',
              'F4': '1'}


def test_naked_quad():
    # TODO: test_unhappy_path
    with GridInstance(grid=NAKED_QUAD) as game:
        assert strategies.NakedX(game=game, logs=[], x=4).attempt()
        assert game.candidates_['A9'] == set(list('58'))
        assert game.candidates_['B9'] == set(list('79'))
        assert game.candidates_['D9'] == set(list('25'))
        assert game.candidates_['E9'] == set(list('79'))
        assert game.candidates_['F9'] == set(list('2358'))
        assert game.candidates_['H9'] == set(list('28'))


POINTING_MULT = {'F7': '2', 'A2': '1', 'F2': '6', 'C7': '5', 'D3': '2',
                 'C1': '9', 'J8': '2', 'J3': '5', 'F8': '5', 'G8': '6',
                 'A3': '7', 'A4': '9', 'J4': '6', 'D2': '7', 'E4': '4',
                 'E8': '7', 'F5': '7', 'D5': '1', 'G1': '7', 'A6': '3',
                 'B5': '8', 'E6': '2', 'G3': '1', 'D7': '4', 'F4': '3',
                 'H5': '3', 'J7': '7', 'A7': '6', 'G9': '5', 'D8': '3',
                 'C9': '7', 'F3': '4', 'J6': '1'}


def test_pointing_multiple():
    with GridInstance(grid=POINTING_MULT) as game:
        expected_3 = ['B1', 'B2', 'B3']
        expected_9 = ['E5', 'E7', 'E9']
        for c in expected_3:
            assert '3' in game.candidates_[c]
        for c in expected_9:
            assert '9' in game.candidates_[c]
        assert strategies.PointingMultiple(game=game, logs=[]).attempt()
        for c in expected_3:
            assert '3' not in game.candidates_in_group(group=expected_3)
        for c in expected_9:
            assert '9' not in game.candidates_in_group(group=expected_9)


BL_REDUCTION = {'B7': '6', 'J2': '9', 'E9': '3', 'G2': '4', 'H7': '2',
                'F1': '4', 'G8': '8', 'A4': '9', 'D5': '8', 'C2': '5',
                'G3': '2', 'E1': '2', 'G9': '1', 'J4': '2', 'J7': '5',
                'C1': '7', 'F6': '2', 'B1': '9', 'E7': '4', 'C8': '4',
                'J6': '8', 'A6': '3', 'H6': '4', 'H3': '5', 'F4': '3',
                'J9': '4', 'A9': '5', 'A7': '7', 'H8': '6', 'D4': '4',
                'B3': '4', 'A8': '1', 'F5': '5', 'E8': '5', 'A5': '4',
                'A2': '2', 'D1': '5'}


def test_box_line_reduction():
    with GridInstance(grid=BL_REDUCTION) as game:
        expected = {'1': {'H2', 'J3'},
                    '3': {'H2', 'J3'},
                    '6': {'E3', 'D3', 'F3', 'C3'},
                    '7': {'J5', 'H4', 'H5'},
                    '8': {'F2', 'F3', 'C3', 'B2'},
                    '9': {'D9', 'F9', 'D7', 'F7'}}
        for v, cells in expected.items():
            for c in cells:
                assert v in game.candidates_[c]
        assert strategies.BoxLineReduction(game=game, logs=[]).attempt()
        for v, cells in expected.items():
            for c in cells:
                assert v not in game.candidates_[c]


X_WING = {'E8': '5', 'A8': '1', 'G2': '6', 'D4': '2', 'H2': '8',
          'G8': '8', 'C6': '5', 'G4': '1', 'A4': '8', 'B3': '8',
          'C1': '1', 'F7': '1', 'B7': '9', 'J9': '2', 'G1': '9',
          'F4': '5', 'C7': '7', 'G6': '7', 'E3': '1', 'H4': '6',
          'J7': '6', 'D8': '4', 'H6': '9', 'G5': '2', 'F9': '3',
          'E1': '8', 'G3': '4', 'H8': '7', 'J8': '9', 'H9': '1',
          'H7': '4', 'G9': '5', 'J2': '1', 'D9': '9', 'E7': '2',
          'H5': '5', 'H3': '2', 'C8': '2', 'E4': '9', 'A7': '5',
          'H1': '3', 'G7': '3', 'C9': '8', 'D7': '8', 'E6': '6',
          'B4': '7', 'B8': '3', 'J4': '4', 'F8': '6', 'C4': '3',
          'A3': '3', 'E9': '7'}


def test_x_wing():
    with GridInstance(grid=X_WING) as game:
        expected_updates = ['A2', 'B2', 'F2', 'A5', 'B5', 'F5']
        for c in expected_updates:
            assert '4' in game.candidates_[c]
        assert strategies.XWing(game=game, logs=[]).attempt()
        assert '4' not in game.candidates_in_group(group=expected_updates)


Y_WING = {'J1': '1', 'H9': '7', 'G1': '2', 'D5': '1', 'A3': '2',
          'H3': '9', 'E7': '6', 'J6': '6', 'H1': '6', 'H5': '8',
          'D6': '8', 'B9': '8', 'C2': '7', 'A4': '8', 'F1': '7',
          'F8': '2', 'C7': '4', 'H2': '4', 'J9': '2', 'C1': '8',
          'G9': '6', 'D2': '2', 'F9': '9', 'G3': '8', 'G5': '3',
          'A9': '1', 'C4': '3', 'F4': '5', 'H7': '3', 'D4': '6',
          'D3': '3', 'G8': '4', 'G2': '5', 'E9': '3', 'D1': '9',
          'F5': '4', 'J2': '3', 'D9': '4', 'J3': '7', 'J4': '4',
          'B7': '2', 'B5': '6', 'C9': '5', 'E1': '4', 'F6': '3',
          'C5': '2', 'B3': '4', 'A6': '4', 'G6': '7', 'E3': '5'}


def test_y_wing():
    with GridInstance(grid=Y_WING) as game:
        assert '9' in game.candidates_['B8']
        assert '9' in game.candidates_['A5']
        assert strategies.YWing(game=game, logs=[]).attempt()
        assert '9' not in game.candidates_['B8']
        assert '9' not in game.candidates_['A5']
