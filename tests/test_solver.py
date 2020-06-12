from collections.abc import Iterable
from sudoku import solver


def test_split_post():
    pd = {'A1': 3, 'B2': 3, 'H7': 'a', 'other': 'test', 'brute': True}
    grid, other = (solver.split_post(post_data=pd))
    pd['A1'] = 5
    assert grid == {'A1': 3, 'B2': 3, 'H7': 'a'}
    assert other == {'other': 'test', 'brute': True}


def test_invalid():
    grid = {'A1': '3', 'B2': '3', 'H7': 'a', 'C8': 4, 'D3': '0'}
    invalid = solver.invalid(grid=grid)
    assert invalid == {'C8', 'H7', 'D3'}


def test_grid_iterator():
    assert isinstance(solver.grid_iterator(), Iterable)
    grid = set([c for c in solver.grid_iterator()])
    exp_grid = {'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9',
                'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9',
                'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9',
                'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9',
                'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9',
                'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9',
                'J1', 'J2', 'J3', 'J4', 'J5', 'J6', 'J7', 'J8', 'J9'}
    assert grid == exp_grid


row_a1 = {'A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'J1'}
row_a4 = {'A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'H4', 'J4'}
row_d3 = {'A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3', 'J3'}
row_j7 = {'A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7', 'J7'}
col_a1 = {'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9'}
col_c4 = {'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'}
col_d3 = {'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9'}
col_j7 = {'J1', 'J2', 'J3', 'J4', 'J5', 'J6', 'J7', 'J8', 'J9'}
box_a1 = {'A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3'}
box_d3 = {'D1', 'D2', 'D3', 'E1', 'E2', 'E3', 'F1', 'F2', 'F3'}
box_f7 = {'D7', 'D8', 'D9', 'E7', 'E8', 'E9', 'F7', 'F8', 'F9'}
box_j7 = {'G7', 'G8', 'G9', 'H7', 'H8', 'H9', 'J7', 'J8', 'J9'}
all_a1 = {'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'B1', 'B2',
          'B3', 'C1', 'C2', 'C3', 'D1', 'E1', 'F1', 'G1', 'H1', 'J1'}
all_d3 = {'A3', 'B3', 'C3', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8',
          'D9', 'E1', 'E2', 'E3', 'F1', 'F2', 'F3', 'G3', 'H3', 'J3'}
all_j7 = {'A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'G8', 'G9', 'H7', 'H8',
          'H9', 'J1', 'J2', 'J3', 'J4', 'J5', 'J6', 'J7', 'J8', 'J9'}


def test_group_iterator():
    assert isinstance(solver.group_iterator(), Iterable)
    groups = [c for c in solver.group_iterator()]
    for g in [row_a1, row_a4, row_d3, row_j7, col_a1, col_c4, col_d3, col_j7,
              box_a1, box_d3, box_f7, box_j7]:
        assert g in groups
    assert len(groups) == 27


def test_cells_in_row():
    assert solver.cells_in_row(cell='A1') == row_a1
    assert solver.cells_in_row(cell='D3') == row_d3
    assert solver.cells_in_row(cell='J7') == row_j7


def test_cells_in_col():
    assert solver.cells_in_col(cell='A1') == col_a1
    assert solver.cells_in_col(cell='D3') == col_d3
    assert solver.cells_in_col(cell='J7') == col_j7


def test_cells_in_box():
    assert solver.cells_in_box(cell='A1') == box_a1
    assert solver.cells_in_box(cell='D3') == box_d3
    assert solver.cells_in_box(cell='J7') == box_j7


def test_all_neighbours():
    assert solver.all_neighbours(cell='A1') == all_a1
    assert solver.all_neighbours(cell='D3') == all_d3
    assert solver.all_neighbours(cell='J7') == all_j7


TEST_GRID = {'A1': '5', 'A2': '6', 'A4': '8', 'A5': '4', 'A6': '7', 'B1': '3',
             'B3': '9', 'B7': '6', 'C3': '8', 'D2': '1', 'D5': '8', 'D8': '4',
             'E1': '7', 'E2': '9', 'E4': '6', 'E6': '2', 'E8': '1', 'E9': '8',
             'F2': '5', 'F5': '3', 'F8': '9', 'G7': '2', 'H3': '6', 'H7': '8',
             'H9': '7', 'J4': '3', 'J5': '1', 'J6': '6', 'J8': '5', 'J9': '9'}


def test_values_in_group():
    game = solver.Game(grid=TEST_GRID, params=None)
    assert game.values_in_group(group=row_a1) == set(list('357'))
    assert game.values_in_group(group=row_a4) == set(list('368'))
    assert game.values_in_group(group=col_c4) == set(list('8'))
    assert game.values_in_group(group=box_f7) == set(list('1489'))
    assert game.values_in_group(group=all_j7) == set(list('12356789'))


def test_values_not_in_group():
    game = solver.Game(grid=TEST_GRID, params=None)
    assert game.values_not_in_group(group=row_a1) == set(list('124689'))
    assert game.values_not_in_group(group=row_a4) == set(list('124579'))
    assert game.values_not_in_group(group=col_c4) == set(list('12345679'))
    assert game.values_not_in_group(group=box_f7) == set(list('23567'))
    assert game.values_not_in_group(group=all_j7) == set(list('4'))


def test_find_naked_singles():
    game = solver.Game(grid=TEST_GRID, params=None)
    game.initialise_candidates()
    act = game.find_naked_singles()
    assert ('H8', '3') in act
    assert ('J7', '4') in act
    assert ('F7', '7') in act
    assert ('E5', '5') in act
    assert len(act) == 4


def test_find_hidden_singles():
    game = solver.Game(grid=TEST_GRID, params=None)
    game.initialise_candidates()
    singles = [('A7', '9'), ('F1', '8'), ('G3', '5'), ('B8', '8'), ('C5', '6'),
               ('C6', '3'), ('G5', '7'), ('E3', '4'), ('G6', '8'), ('H1', '1'),
               ('G8', '6'), ('G9', '1')]
    act = game.find_hidden_singles()

    for s in singles:
        assert s in act
