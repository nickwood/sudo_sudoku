from sudoku import solver


def test_split_post_data():
    pd = {'A1': 3, 'B2': 3, 'H7': 'a', 'other': 'test', 'brute': True}
    grid, other = (solver.split_post_data(post_data=pd))
    pd['A1'] = 5
    assert grid == {'A1': 3, 'B2': 3, 'H7': 'a'}
    assert other == {'other': 'test', 'brute': True}


def test_invalid():
    grid = {'A1': '3', 'B2': '3', 'H7': 'a', 'C8': 4, 'D3': '0'}
    invalid = solver.invalid(grid=grid)
    print(invalid)
    assert invalid == {'H7', 'D3'}
