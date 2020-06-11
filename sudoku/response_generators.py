from flask import render_template
from .solver import split_post, invalid, Game

DEFAULT_PARAMS = None


def home(*, grid):
    return render_template('base.html',
                           grid=grid,
                           params=DEFAULT_PARAMS,
                           errors=None,
                           invalid=None)


def do_solve(*, post_data):
    initial_grid, params = split_post(post_data=dict(post_data))
    invalid_cells = invalid(grid=initial_grid)
    if invalid_cells:
        errors = ['Invalid entries at: ' + ', '.join(invalid_cells)]
        return render_template('base.html',
                               grid=initial_grid,
                               params=params,
                               errors=errors,
                               invalid=invalid_cells)

    to_solve = Game(grid=initial_grid, params=params)
    if to_solve.solve():
        return render_template('base.html',
                               grid=to_solve.solution,
                               params=params,
                               errors=None)
    else:
        errors = ['Could not solve']
        return render_template('base.html',
                               grid=to_solve.grid,
                               params=params,
                               errors=None)


def generate():
    return render_template('generate.html')


def analyse():
    return render_template('analyse.html')
