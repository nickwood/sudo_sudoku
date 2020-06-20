from collections.abc import Iterable
from unittest.mock import Mock
from sudoku import solver

# TODO: move to response_gen tests
# def test_split_post():
#     pd = {'A1': 3, 'B2': 3, 'H7': 'a', 'other': 'test', 'brute': True}
#     grid, other = (solver.split_post(post_data=pd))
#     pd['A1'] = 5
#     assert grid == {'A1': 3, 'B2': 3, 'H7': 'a'}
#     assert other == {'other': 'test', 'brute': True}


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


def test_group_iterator():
    assert isinstance(solver.group_iterator(), Iterable)
    groups = [c for c in solver.group_iterator()]
    for g in [row_a1, row_c4, row_d3, row_j7, col_a1, col_a4, col_d3, col_j7,
              box_a1, box_d3, box_f7, box_j7]:
        assert g in groups
    assert len(groups) == 27


def test_cells_in_row():
    assert solver.cells_in_row(cell='A1') == row_a1
    assert solver.cells_in_row(cell='D3') == row_d3
    assert solver.cells_in_row(cell='J7') == row_j7
    assert solver.cells_in_row(cell='A1', inc=False) == row_a1 - {'A1'}
    assert solver.cells_in_row(cell='D3', inc=False) == row_d3 - {'D3'}
    assert solver.cells_in_row(cell='J7', inc=False) == row_j7 - {'J7'}


def test_cells_in_col():
    assert solver.cells_in_col(cell='A1') == col_a1
    assert solver.cells_in_col(cell='D3') == col_d3
    assert solver.cells_in_col(cell='J7') == col_j7
    assert solver.cells_in_col(cell='A1', inc=False) == col_a1 - {'A1'}
    assert solver.cells_in_col(cell='D3', inc=False) == col_d3 - {'D3'}
    assert solver.cells_in_col(cell='J7', inc=False) == col_j7 - {'J7'}


def test_cells_in_box():
    assert solver.cells_in_box(cell='A1') == box_a1
    assert solver.cells_in_box(cell='D3') == box_d3
    assert solver.cells_in_box(cell='J7') == box_j7
    assert solver.cells_in_box(cell='A1', inc=False) == box_a1 - {'A1'}
    assert solver.cells_in_box(cell='D3', inc=False) == box_d3 - {'D3'}
    assert solver.cells_in_box(cell='J7', inc=False) == box_j7 - {'J7'}


def test_all_neighbours():
    assert solver.all_neighbours(cell='A1') == all_a1
    assert solver.all_neighbours(cell='D3') == all_d3
    assert solver.all_neighbours(cell='J7') == all_j7
    assert solver.all_neighbours(cell='A1', inc=False) == all_a1 - {'A1'}
    assert solver.all_neighbours(cell='D3', inc=False) == all_d3 - {'D3'}
    assert solver.all_neighbours(cell='J7', inc=False) == all_j7 - {'J7'}


def test_common_neighbours():
    assert solver.common_neighbours(cells=['A1', 'A6']) == row_a1
    assert solver.common_neighbours(cells=['A1', 'D1']) == col_a1
    assert solver.common_neighbours(cells=['D8', 'F7']) == box_f7
    T1 = {'D4', 'E4', 'F4', 'D5', 'E5', 'F5', 'D6', 'E6', 'F6', 'A4', 'B4',
          'C4', 'G4', 'H4', 'J4'}
    assert solver.common_neighbours(cells=['E4', 'D4']) == T1
    T2 = {'A7', 'A8', 'A9', 'B7', 'B8', 'B9', 'C7', 'C8', 'C9'}
    assert solver.common_neighbours(cells=['C9', 'B8']) == T2
    assert solver.common_neighbours(cells=['A1', 'J7']) == {'J1', 'A7'}

    assert solver.common_neighbours(cells=['A1', 'A6'], inc=False) == row_a1 - {'A1', 'A6'}  # noqa: E501
    assert solver.common_neighbours(cells=['A1', 'D1'], inc=False) == col_a1 - {'A1', 'D1'}  # noqa: E501
    assert solver.common_neighbours(cells=['D8', 'F7'], inc=False) == box_f7 - {'F7', 'D8'}  # noqa: E501
    T3 = {'F4', 'D5', 'E5', 'F5', 'D6', 'E6', 'F6', 'A4', 'B4', 'C4', 'G4',
          'H4', 'J4'}
    assert solver.common_neighbours(cells=['E4', 'D4'], inc=False) == T3
    T4 = {'A7', 'A8', 'A9', 'B7', 'B9', 'C7', 'C8'}
    assert solver.common_neighbours(cells=['C9', 'B8'], inc=False) == T4
    assert solver.common_neighbours(cells=['A1', 'J7'], inc=False) == {'J1', 'A7'}  # noqa: E501


TEST_GRID = {'A1': '5', 'A2': '6', 'A4': '8', 'A5': '4', 'A6': '7', 'B1': '3',
             'B3': '9', 'B7': '6', 'C3': '8', 'D2': '1', 'D5': '8', 'D8': '4',
             'E1': '7', 'E2': '9', 'E4': '6', 'E6': '2', 'E8': '1', 'E9': '8',
             'F2': '5', 'F5': '3', 'F8': '9', 'G7': '2', 'H3': '6', 'H7': '8',
             'H9': '7', 'J4': '3', 'J5': '1', 'J6': '6', 'J8': '5', 'J9': '9'}

DEFAULT_PARAMS = {'find_naked_singles': True,
                  'find_hidden_singles': True,
                  'find_naked_pairs': True}


class GameInstance():
    def __init__(self, grid=TEST_GRID, params=DEFAULT_PARAMS):
        self.grid = grid.copy()
        self.params = params

    def __enter__(self):
        g = solver.Game(grid=self.grid, params=self.params)
        g.initialise_candidates()
        return g

    def __exit__(self, *args, **kwargs):
        pass


def test_add_error():
    with GameInstance() as game:
        game.add_error(msg='foo')
        game.add_error(msg='bar', cells={'C6'})
        game.add_error(msg='bash', cells={'C6', 'D7'})
        game.add_error(msg='bang', cells={'E8', 'F7'})

        assert game.errors == {'foo', 'bar', 'bash', 'bang'}
        assert game.invalid_cells == {'C6', 'D7', 'E8', 'F7'}


def test_remove_candidates():
    with GameInstance() as game:
        game.remove_candidates(group=row_a1, values={'2', '8', '7', '9'})
        assert game.candidates_['A3'] == {'1'}
        assert game.candidates_['A7'] == {'1', '3'}
        assert game.candidates_['A8'] == {'3'}
        assert game.candidates_['A9'] == {'1', '3'}


def test_add_to_grid():
    with GameInstance() as game:
        game.remove_candidates = Mock()
        game.add_to_grid(cell='A3', value='1')
        assert game.grid['A3'] == '1'
        game.remove_candidates.assert_called()


def test_values_in_group():
    with GameInstance() as game:
        assert game.values_in_group(group=col_a1) == set(list('357'))
        assert game.values_in_group(group=col_a4) == set(list('368'))
        assert game.values_in_group(group=row_c4) == set(list('8'))
        assert game.values_in_group(group=box_f7) == set(list('1489'))
        assert game.values_in_group(group=all_j7) == set(list('12356789'))


def test_values_not_in_group():
    with GameInstance() as game:
        assert game.values_not_in_group(group=col_a1) == set(list('124689'))
        assert game.values_not_in_group(group=col_a4) == set(list('124579'))
        assert game.values_not_in_group(group=row_c4) == set(list('12345679'))
        assert game.values_not_in_group(group=box_f7) == set(list('23567'))
        assert game.values_not_in_group(group=all_j7) == set(list('4'))


def test_candidates_in_group():
    with GameInstance() as game:
        assert game.candidates_in_group(group=col_a1) == set(list('124689'))
        assert game.candidates_in_group(group=box_f7) == set(list('23567'))
        assert game.candidates_in_group(group=['H2', 'H4']) == set(list('23459'))  # noqa: E501
        assert game.candidates_in_group(group=['J1', 'J2', 'J3']) == set(list('2478'))  # noqa: E501


def test_solved_cell():
    with GameInstance() as game:
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
    with GameInstance() as game:
        assert game.solved_in_group(group=col_a1) == {'A1', 'B1', 'E1'}
        assert game.solved_in_group(group=row_j7) == {'J4', 'J5', 'J6', 'J8', 'J9'}  # noqa: E501
        assert game.solved_in_group(group=box_f7) == {'D8', 'E8', 'E9', 'F8'}

        T1 = {'G7', 'H7', 'H9', 'B7', 'J4', 'J5', 'J6', 'J8', 'J9'}
        assert game.solved_in_group(group=all_j7) == T1

        G1 = {'A7', 'A8', 'A9', 'B7', 'B8', 'B9', 'C7', 'C8', 'C9'}
        assert game.solved_in_group(group=G1) == {'B7'}


def test_unsolved_in_group():
    with GameInstance() as game:
        assert game.unsolved_in_group(group=row_j7) == {'J1', 'J2', 'J3', 'J7'}
        assert game.unsolved_in_group(group=box_f7) == {'D7', 'E7', 'F7', 'D9', 'F9'}  # noqa: E501

        T1 = {'J3', 'J2', 'A7', 'C7', 'F7', 'J1', 'G9', 'G8', 'J7', 'H8', 'D7', 'E7'}  # noqa: E501
        assert game.unsolved_in_group(group=all_j7) == T1

        G1 = {'A7', 'A8', 'A9', 'B7', 'B8', 'B9', 'C7', 'C8', 'C9'}
        assert game.unsolved_in_group(group=G1) == G1 - {'B7'}


def test_unsolved_common_neighbours():
    with GameInstance() as game:
        T1 = {'A3', 'A7', 'A8'}
        assert game.unsolved_common_neighbours(cells=('A1', 'A9')) == T1
        T2 = {'B2', 'C2', 'D1', 'D3', 'E3', 'F1', 'F3', 'G2', 'H2', 'J2'}
        assert game.unsolved_common_neighbours(cells=('D2', 'E2')) == T2
        T3 = {'J1', 'J3'}
        assert game.unsolved_common_neighbours(cells=('J7', 'J2')) == T3


def test_find_naked_singles():
    with GameInstance() as game:
        act = game.find_naked_singles()
        assert ('H8', '3') in act
        assert ('J7', '4') in act
        assert ('F7', '7') in act
        assert ('E5', '5') in act
        assert len(act) == 4


def test_find_hidden_singles():
    with GameInstance() as game:
        singles = [('A7', '9'), ('F1', '8'), ('G3', '5'), ('B8', '8'),
                   ('C5', '6'), ('C6', '3'), ('G5', '7'), ('E3', '4'),
                   ('G6', '8'), ('H1', '1'), ('G8', '6'), ('G9', '1')]
        act = game.find_hidden_singles()

        for s in singles:
            assert s in act


GRID_NAKED_PAIR = {'H7': '6', 'D3': '2', 'B3': '1', 'C6': '1', 'B6': '9',
                   'D6': '5', 'B7': '7', 'J3': '6', 'J2': '8', 'E6': '6',
                   'J6': '2', 'A1': '3', 'B8': '4', 'B2': '5', 'C3': '4',
                   'C9': '8', 'D5': '7', 'D4': '9', 'C1': '7', 'J8': '5',
                   'J1': '1', 'J7': '4', 'E7': '3', 'H2': '7', 'F3': '7',
                   'D2': '3', 'C7': '5', 'E2': '1', 'J5': '9', 'H6': '4',
                   'D7': '8', 'G3': '5', 'F6': '3', 'H3': '3', 'A2': '6',
                   'A7': '1'}


def test_naked_pairs():
    # TODO: test_unhappy_path
    with GameInstance(grid=GRID_NAKED_PAIR) as game:
        assert game.candidates_['A3'] == set(list('89'))
        assert game.candidates_['A4'] == set(list('24578'))
        assert game.candidates_['A5'] == set(list('2458'))
        assert game.candidates_['A6'] == set(list('78'))
        assert game.candidates_['A8'] == set(list('29'))
        assert game.candidates_['A9'] == set(list('29'))
        assert game.candidates_['B9'] == set(list('236'))
        assert game.candidates_['C8'] == set(list('2369'))
        assert game.find_naked_pairs()
        assert game.candidates_['A3'] == set(list('8'))
        assert game.candidates_['A4'] == set(list('4578'))
        assert game.candidates_['A5'] == set(list('458'))
        assert game.candidates_['A6'] == set(list('78'))
        assert game.candidates_['A8'] == set(list('29'))
        assert game.candidates_['A9'] == set(list('29'))
        assert game.candidates_['B9'] == set(list('36'))
        assert game.candidates_['C8'] == set(list('36'))


GRID_NAKED_TRIPLE = {'C3': '7', 'E5': '2', 'A4': '7', 'A2': '2', 'G4': '2',
                     'J4': '9', 'F6': '7', 'E6': '5', 'G2': '8', 'J7': '6',
                     'B6': '2', 'H5': '5', 'H7': '9', 'F2': '9', 'F5': '4',
                     'J6': '1', 'F8': '6', 'D8': '1', 'F4': '1', 'J9': '4',
                     'B3': '8', 'E4': '6', 'B4': '5', 'D6': '3', 'J5': '8',
                     'J8': '7', 'H6': '4', 'G8': '3', 'A5': '6', 'G6': '6',
                     'C9': '6', 'C4': '4', 'H1': '7', 'D5': '9', 'G7': '5',
                     'D4': '8', 'G9': '1', 'G5': '7', 'H4': '3', 'A1': '3',
                     'G3': '9', 'C6': '8', 'C1': '9', 'A6': '9', 'D2': '7',
                     'G1': '4'}


def test_naked_triples():
    # TODO: test_unhappy_path
    with GameInstance(grid=GRID_NAKED_TRIPLE) as game:
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
        assert game.find_naked_triples()
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


GRID_NAKED_QUAD = {'A5': '6', 'E5': '2', 'A2': '2', 'C4': '4', 'F6': '7',
                   'J6': '1', 'A1': '3', 'J4': '9', 'G1': '4', 'G2': '8',
                   'D2': '7', 'G7': '5', 'C6': '8', 'C3': '7', 'G5': '7',
                   'J7': '6', 'A4': '7', 'D4': '8', 'G4': '2', 'H5': '5',
                   'C9': '6', 'J8': '7', 'F5': '4', 'F2': '9', 'J9': '4',
                   'J5': '8', 'B4': '5', 'D6': '3', 'G8': '3', 'D8': '1',
                   'G3': '9', 'C1': '9', 'H1': '7', 'G6': '6', 'G9': '1',
                   'H6': '4', 'A6': '9', 'B6': '2', 'B3': '8', 'E4': '6',
                   'F8': '6', 'D5': '9', 'H7': '9', 'E6': '5', 'H4': '3',
                   'F4': '1'}


def test_naked_quads():
    # TODO: test_unhappy_path
    with GameInstance(grid=GRID_NAKED_QUAD) as game:
        assert game.find_naked_quads()
        assert game.candidates_['A9'] == set(list('58'))
        assert game.candidates_['B9'] == set(list('79'))
        assert game.candidates_['D9'] == set(list('25'))
        assert game.candidates_['E9'] == set(list('79'))
        assert game.candidates_['F9'] == set(list('2358'))
        assert game.candidates_['H9'] == set(list('28'))
