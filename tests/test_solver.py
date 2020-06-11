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


TEST_GRID = {'A1': '5', 'A2': '6', 'A4': '8', 'A5': '4', 'A6': '7', 'B1': '3',
             'B3': '9', 'B7': '6', 'C3': '8', 'D2': '1', 'D5': '8', 'D8': '4',
             'E1': '7', 'E2': '9', 'E4': '6', 'E6': '2', 'E8': '1', 'E9': '8',
             'F2': '5', 'F5': '3', 'F8': '9', 'G7': '2', 'H3': '6', 'H7': '8',
             'H9': '7', 'J4': '3', 'J5': '1', 'J6': '6', 'J8': '5', 'J9': '9'}


def test_neighbour_values():
    game = solver.Game(grid=TEST_GRID, params=None)
    print(game.neighbour_values(cell='A3'))


def test_values_in_row():
    game = solver.Game(grid=TEST_GRID, params=None)
    assert game.values_in_row(cell='A1') == {'3', '7', '5'}


def test_values_in_column():
    game = solver.Game(grid=TEST_GRID, params=None)
    assert game.values_in_col(cell='B1') == {'3', '6', '9'}


def test_cells_in_box():
    act1 = solver.cells_in_box(cell='B3')
    exp1 = set(['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3'])
    assert act1 == exp1

    act2 = solver.cells_in_box(cell='D6')
    exp2 = set(['D4', 'D5', 'D6', 'E4', 'E5', 'E6', 'F4', 'F5', 'F6'])
    assert act2 == exp2


def test_values_in_box():
    game = solver.Game(grid=TEST_GRID, params=None)
    assert game.values_in_box(cell='J4') == {'3', '1', '6'}


def test_find_naked_singles():
    game = solver.Game(grid=TEST_GRID, params=None)
    game.initialise_candidates()
    act = game.find_naked_singles()
    assert ('H8', '3') in act
    assert ('J7', '4') in act
    assert ('F7', '7') in act
    assert ('E5', '5') in act
    assert len(act) == 4
