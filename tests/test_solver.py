from sudoku import solver

# TODO: move to response_gen tests
# def test_split_post():
#     pd = {'A1': 3, 'B2': 3, 'H7': 'a', 'other': 'test', 'brute': True}
#     grid, other = (solver.split_post(post_data=pd))
#     pd['A1'] = 5
#     assert grid == {'A1': 3, 'B2': 3, 'H7': 'a'}
#     assert other == {'other': 'test', 'brute': True}

# TODO: move to response_gen tests
# def test_invalid():
#     grid = {'A1': '3', 'B2': '3', 'H7': 'a', 'C8': 4, 'D3': '0'}
#     invalid = solver.invalid(grid=grid)
#     assert invalid == {'C8', 'H7', 'D3'}


TEST_GRID = {'A1': '5', 'A2': '6', 'A4': '8', 'A5': '4', 'A6': '7', 'B1': '3',
             'B3': '9', 'B7': '6', 'C3': '8', 'D2': '1', 'D5': '8', 'D8': '4',
             'E1': '7', 'E2': '9', 'E4': '6', 'E6': '2', 'E8': '1', 'E9': '8',
             'F2': '5', 'F5': '3', 'F8': '9', 'G7': '2', 'H3': '6', 'H7': '8',
             'H9': '7', 'J4': '3', 'J5': '1', 'J6': '6', 'J8': '5', 'J9': '9'}

DEFAULT_PARAMS = {'find_naked_singles': True,
                  'find_hidden_singles': True,
                  'find_naked_pairs': True}


class GameInstance():
    def __init__(self, grid=TEST_GRID, solvers=DEFAULT_PARAMS):
        self.grid = grid.copy()
        self.solvers = solvers

    def __enter__(self):
        g = solver.Game(grid=self.grid, solvers=self.solvers)
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
