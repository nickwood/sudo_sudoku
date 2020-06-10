def split_post_data(*, post_data):
    '''The raw post data conatins our entiure form, which is a bit cuimbersome
    to work with. This helper functrion splits it into two dicts, one contains
    the grid information, and the other contains everything else (e.g. solver
    contraints)'''
    grid_keys = set([k for k in grid_iterator()])
    grid_data = {key: post_data[key] for key in post_data.keys() & grid_keys}
    other_data = {key: post_data[key] for key in post_data.keys() - grid_keys}
    return grid_data, other_data


def invalid(*, grid):
    invalid = set()
    for cell in grid_iterator():
        if str(grid.get(cell, '')) not in '123456789':
            invalid.add(cell)
    return invalid


def grid_iterator():
    return (col + row for row in '123456789' for col in 'ABCDEFGHJ')


def solve(*, grid, params):
    pass