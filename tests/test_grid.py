from sudoku.grid import Grid
from collections.abc import Iterable
from unittest.mock import Mock


def test_grid_iterator():
    assert isinstance(Grid.grid_iterator(), Iterable)
    act_grid = set([c for c in Grid.grid_iterator()])
    exp_grid = {'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9',
                'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9',
                'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9',
                'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9',
                'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9',
                'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9',
                'J1', 'J2', 'J3', 'J4', 'J5', 'J6', 'J7', 'J8', 'J9'}
    assert act_grid == exp_grid


col_a1 = {'A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'J1'}
col_a4 = {'A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'H4', 'J4'}
col_d3 = {'A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3', 'J3'}
col_j7 = {'A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7', 'J7'}
row_a1 = {'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9'}
row_c4 = {'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'}
row_d3 = {'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9'}
row_j7 = {'J1', 'J2', 'J3', 'J4', 'J5', 'J6', 'J7', 'J8', 'J9'}
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


def test_cells_in_row():
    assert Grid.cells_in_row(cell='A1') == row_a1
    assert Grid.cells_in_row(cell='D3') == row_d3
    assert Grid.cells_in_row(cell='J7') == row_j7
    assert Grid.cells_in_row(cell='A1', inc=False) == row_a1 - {'A1'}
    assert Grid.cells_in_row(cell='D3', inc=False) == row_d3 - {'D3'}
    assert Grid.cells_in_row(cell='J7', inc=False) == row_j7 - {'J7'}


def test_row_iterator():
    assert isinstance(Grid.row_iterator(), Iterable)
    rows = [r for r in Grid.row_iterator()]
    exp_in = [row_a1, row_c4, row_d3, row_j7]
    exp_out = [col_d3, box_d3, all_a1]
    for g in exp_in:
        assert g in rows
    for g in exp_out:
        assert g not in rows


def test_cells_in_col():
    assert Grid.cells_in_col(cell='A1') == col_a1
    assert Grid.cells_in_col(cell='D3') == col_d3
    assert Grid.cells_in_col(cell='J7') == col_j7
    assert Grid.cells_in_col(cell='A1', inc=False) == col_a1 - {'A1'}
    assert Grid.cells_in_col(cell='D3', inc=False) == col_d3 - {'D3'}
    assert Grid.cells_in_col(cell='J7', inc=False) == col_j7 - {'J7'}


def test_col_iterator():
    assert isinstance(Grid.col_iterator(), Iterable)
    cols = [r for r in Grid.col_iterator()]
    exp_in = [col_a1, col_a4, col_d3, col_j7]
    exp_out = [row_a1, box_d3, all_a1]
    for g in exp_in:
        assert g in cols
    for g in exp_out:
        assert g not in cols


def test_cells_in_box():
    assert Grid.cells_in_box(cell='A1') == box_a1
    assert Grid.cells_in_box(cell='D3') == box_d3
    assert Grid.cells_in_box(cell='J7') == box_j7
    assert Grid.cells_in_box(cell='A1', inc=False) == box_a1 - {'A1'}
    assert Grid.cells_in_box(cell='D3', inc=False) == box_d3 - {'D3'}
    assert Grid.cells_in_box(cell='J7', inc=False) == box_j7 - {'J7'}


def test_box_iterator():
    assert isinstance(Grid.box_iterator(), Iterable)
    boxes = [r for r in Grid.box_iterator()]
    exp_in = [box_a1, box_d3, box_f7, box_j7]
    exp_out = [row_a1, col_d3, all_a1]
    for g in exp_in:
        assert g in boxes
    for g in exp_out:
        assert g not in boxes


def test_group_iterator():
    assert isinstance(Grid.group_iterator(), Iterable)
    groups = [c for c in Grid.group_iterator()]
    for g in [row_a1, row_c4, row_d3, row_j7, col_a1, col_a4, col_d3, col_j7,
              box_a1, box_d3, box_f7, box_j7]:
        assert g in groups
    assert len(groups) == 27


def test_in_same_box():
    assert Grid.in_same_box(group=['A1', 'A2', 'B3'])
    assert Grid.in_same_box(group=['A1', 'B3', 'C2'])
    assert Grid.in_same_box(group=['F3', 'F3', 'G6']) is False
    assert Grid.in_same_box(group=['F1', 'F2', 'F3', 'F4', 'F5']) is False
    assert Grid.in_same_box(group=['F1', 'F2', 'F3'])
    assert Grid.in_same_box(group={'G4', 'G5', 'E6'}) is False
    assert Grid.in_same_box(group={'A1', 'A5'}) is False
    assert Grid.in_same_box(group=['J8', 'H9', 'B7']) is False
    assert Grid.in_same_box(group=box_a1)
    assert Grid.in_same_box(group=row_j7) is False
    assert Grid.in_same_box(group=col_d3) is False
    assert Grid.in_same_box(group=all_d3) is False


def test_all_neighbours():
    assert Grid.all_neighbours(cell='A1') == all_a1
    assert Grid.all_neighbours(cell='D3') == all_d3
    assert Grid.all_neighbours(cell='J7') == all_j7
    assert Grid.all_neighbours(cell='A1', inc=False) == all_a1 - {'A1'}
    assert Grid.all_neighbours(cell='D3', inc=False) == all_d3 - {'D3'}
    assert Grid.all_neighbours(cell='J7', inc=False) == all_j7 - {'J7'}


def test_common_neighbours():
    common = Grid.common_neighbours
    assert common(cells=['A1', 'A6']) == row_a1
    assert common(cells=['A1', 'D1']) == col_a1
    assert common(cells=['D8', 'F7']) == box_f7
    T1 = {'D4', 'E4', 'F4', 'D5', 'E5', 'F5', 'D6', 'E6', 'F6', 'A4', 'B4',
          'C4', 'G4', 'H4', 'J4'}
    assert common(cells=['E4', 'D4']) == T1
    T2 = {'A7', 'A8', 'A9', 'B7', 'B8', 'B9', 'C7', 'C8', 'C9'}
    assert common(cells=['C9', 'B8']) == T2
    assert common(cells=['A1', 'J7']) == {'J1', 'A7'}

    assert common(cells=['A1', 'A6'], inc=False) == row_a1 - {'A1', 'A6'}
    assert common(cells=['A1', 'D1'], inc=False) == col_a1 - {'A1', 'D1'}
    assert common(cells=['D8', 'F7'], inc=False) == box_f7 - {'F7', 'D8'}
    T3 = {'F4', 'D5', 'E5', 'F5', 'D6', 'E6', 'F6', 'A4', 'B4', 'C4', 'G4',
          'H4', 'J4'}
    assert common(cells=['E4', 'D4'], inc=False) == T3
    T4 = {'A7', 'A8', 'A9', 'B7', 'B9', 'C7', 'C8'}
    assert common(cells=['C9', 'B8'], inc=False) == T4
    assert common(cells=['A1', 'J7'], inc=False) == {'J1', 'A7'}


TEST_GRID = {'A1': '5', 'A2': '6', 'A4': '8', 'A5': '4', 'A6': '7', 'B1': '3',
             'B3': '9', 'B7': '6', 'C3': '8', 'D2': '1', 'D5': '8', 'D8': '4',
             'E1': '7', 'E2': '9', 'E4': '6', 'E6': '2', 'E8': '1', 'E9': '8',
             'F2': '5', 'F5': '3', 'F8': '9', 'G7': '2', 'H3': '6', 'H7': '8',
             'H9': '7', 'J4': '3', 'J5': '1', 'J6': '6', 'J8': '5', 'J9': '9'}


class GridInstance():
    def __init__(self, grid=TEST_GRID):
        self.grid = grid.copy()

    def __enter__(self):
        g = Grid(grid=self.grid)
        return g

    def __exit__(self, *args, **kwargs):
        pass


def test_values_in_group():
    with GridInstance() as game:
        assert game.values_in_group(group=col_a1) == set(list('357'))
        assert game.values_in_group(group=col_a4) == set(list('368'))
        assert game.values_in_group(group=row_c4) == set(list('8'))
        assert game.values_in_group(group=box_f7) == set(list('1489'))
        assert game.values_in_group(group=all_j7) == set(list('12356789'))


def test_values_not_in_group():
    with GridInstance() as game:
        assert game.values_not_in_group(group=col_a1) == set(list('124689'))
        assert game.values_not_in_group(group=col_a4) == set(list('124579'))
        assert game.values_not_in_group(group=row_c4) == set(list('12345679'))
        assert game.values_not_in_group(group=box_f7) == set(list('23567'))
        assert game.values_not_in_group(group=all_j7) == set(list('4'))


def test_add_to_grid():
    with GridInstance() as game:
        game.remove_candidate = Mock()
        game.add_to_grid(cell='A3', value='1')
        assert game.grid['A3'] == '1'
        game.remove_candidate.assert_called()
        game.add_to_grid(cell='A3', value='3')
        assert game.grid['A3'] == '3'


def test_remove_candidate():
    with GridInstance() as game:
        game.remove_candidate(group=row_a1, value='2')
        print(game.candidates_)
        assert game.candidates_['A3'] == {'1'}
        assert game.candidates_['A7'] == {'1', '3', '9'}
        assert game.candidates_['A8'] == {'3'}
        assert game.candidates_['A9'] == {'1', '3'}


def test_remove_candidates():
    with GridInstance() as game:
        game.remove_candidates(group=row_a1, values={'2', '8', '7', '9'})
        assert game.candidates_['A3'] == {'1'}
        assert game.candidates_['A7'] == {'1', '3'}
        assert game.candidates_['A8'] == {'3'}
        assert game.candidates_['A9'] == {'1', '3'}


def test_candidates_in_group():
    with GridInstance() as game:
        cig = game.candidates_in_group
        assert cig(group=col_a1) == set(list('124689'))
        assert cig(group=box_f7) == set(list('23567'))
        assert cig(group=['H2', 'H4']) == set(list('23459'))
        assert cig(group=['J1', 'J2', 'J3']) == set(list('2478'))


def test_shared_candidates():
    with GridInstance() as game:
        sc = game.shared_candidates
        assert sc(group=['C1', 'C2']) == {'2', '4'}
        assert sc(group=col_a1) == set()
        assert sc(group=box_f7) == set()
        assert sc(group=['C1', 'F7']) == set()
        assert sc(group=['G1', 'H1', 'J1']) == {'4'}


def test_solved_cell():
    with GridInstance() as game:
        assert game.solved_cell(cell='A1')
        assert game.solved_cell(cell='A2')
        assert game.solved_cell(cell='A4')
        assert game.solved_cell(cell='A5')
        assert game.solved_cell(cell='A8') is False
        assert game.solved_cell(cell='B2') is False
        assert game.solved_cell(cell='F6') is False
        game.grid['G7'] == ''
        assert game.solved_cell(cell='F6') is False


def test_solved_in_group():
    with GridInstance() as game:
        sig = game.solved_in_group
        assert sig(group=col_a1) == {'A1', 'B1', 'E1'}
        assert sig(group=row_j7) == {'J4', 'J5', 'J6', 'J8', 'J9'}
        assert sig(group=box_f7) == {'D8', 'E8', 'E9', 'F8'}

        T1 = {'G7', 'H7', 'H9', 'B7', 'J4', 'J5', 'J6', 'J8', 'J9'}
        assert game.solved_in_group(group=all_j7) == T1

        G1 = {'A7', 'A8', 'A9', 'B7', 'B8', 'B9', 'C7', 'C8', 'C9'}
        assert game.solved_in_group(group=G1) == {'B7'}


def test_unsolved_in_group():
    with GridInstance() as game:
        uig = game.unsolved_in_group
        assert uig(group=row_j7) == {'J1', 'J2', 'J3', 'J7'}
        assert uig(group=box_f7) == {'D7', 'E7', 'F7', 'D9', 'F9'}

        T1 = {'J3', 'J2', 'A7', 'C7', 'F7', 'J1', 'G9',
              'G8', 'J7', 'H8', 'D7', 'E7'}
        assert uig(group=all_j7) == T1

        G1 = {'A7', 'A8', 'A9', 'B7', 'B8', 'B9', 'C7', 'C8', 'C9'}
        assert uig(group=G1) == G1 - {'B7'}


def test_unsolved_common_neighbours():
    with GridInstance() as game:
        ucn = game.unsolved_common_neighbours
        assert ucn(cells=('A1', 'A9')) == {'A3', 'A7', 'A8'}
        assert ucn(cells=('J7', 'J2')) == {'J1', 'J3'}
        exp = {'B2', 'C2', 'D1', 'D3', 'E3', 'F1', 'F3', 'G2', 'H2', 'J2'}
        assert ucn(cells=('D2', 'E2')) == exp


def test_cells_with_candidate():
    with GridInstance() as game:
        cwc = game.cells_with_candidate
        assert cwc(group=['J2', 'A9', 'B9', 'E5'], value='7') == {'J2'}
        assert cwc(group=row_a1, value='9') == {'A7'}
        assert cwc(group=col_d3, value='4') == {'E3', 'F3', 'G3', 'J3'}
        assert cwc(group=box_f7, value='7') == {'F7', 'D7'}
        assert cwc(group=row_j7, value='7') == {'J2', 'J3'}


def test_cells_with_candidates():
    with GridInstance() as game:
        cwc = game.cells_with_candidates
        assert cwc(group=row_a1, values={'3', '9'}) == {'A7', 'A8', 'A9'}
        assert cwc(group=col_d3, values={'1', '5'}) == {'G3', 'A3'}
        assert cwc(group=box_f7, values={'2', '6'}) == {'F9', 'D9'}
        assert cwc(group=row_j7, values={'7', '2'}) == {'J1', 'J2', 'J3'}


def test_empty_rectangles():
    with GridInstance() as game:
        rectangles = [r for r in game.empty_rectangles()]
        assert len(rectangles) == 191
        assert (['H1', 'H2', 'J1', 'J2'] in rectangles)
