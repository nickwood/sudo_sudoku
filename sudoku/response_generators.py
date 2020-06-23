from collections import ChainMap
from flask import render_template
from .solver import invalid, Game


DEFAULT_METHODS = {'naked_singles': True,
                   'hidden_singles': True,
                   'naked_pairs': True,
                   'naked_triples': True,
                   'naked_quads': True}


def split_post(*, post_data):
    '''The raw post data conatins our entire form, which is a bit cumbersome
    to work with. This helper functrion splits it into two dicts, one contains
    the grid information, and the other contains everything else (e.g. solver
    contraints)'''
    grid = filter_keys(post_data, 'grid_')
    candidates = filter_keys(post_data, 'cand_')
    methods = ChainMap(filter_keys(post_data, 'find_'), DEFAULT_METHODS)
    return grid, methods, candidates


def filter_keys(data, prefix):
    selected_keys = {k for k in data if k.startswith(prefix)}
    return {k[len(prefix):]: data[k] for k in selected_keys}


def render_invalid(*, grid, solvers, invalid):
    errors = ['Invalid entries at: ' + ', '.join(invalid)]
    return render_template('base.html',
                           grid=grid,
                           solvers=solvers,
                           errors=errors,
                           invalid=invalid)


demo_easy = {'A1': '5', 'A2': '6', 'A4': '8', 'A5': '4', 'A6': '7',
             'B1': '3', 'B3': '9', 'B7': '6', 'C3': '8', 'D2': '1',
             'D5': '8', 'D8': '4', 'E1': '7', 'E2': '9', 'E4': '6',
             'E6': '2', 'E8': '1', 'E9': '8', 'F2': '5', 'F5': '3',
             'F8': '9', 'G7': '2', 'H3': '6', 'H7': '8', 'H9': '7',
             'J4': '3', 'J5': '1', 'J6': '6', 'J8': '5', 'J9': '9'}
demo_mid = {'H7': '6', 'D3': '2', 'B3': '1', 'C6': '1', 'B6': '9',
            'D6': '5', 'B7': '7', 'J3': '6', 'J2': '8', 'E6': '6',
            'J6': '2', 'A1': '3', 'B8': '4', 'B2': '5', 'C3': '4',
            'C9': '8', 'D5': '7', 'D4': '9', 'C1': '7', 'J8': '5',
            'J1': '1', 'J7': '4', 'E7': '3', 'H2': '7', 'F3': '7',
            'D2': '3', 'C7': '5', 'E2': '1', 'J5': '9', 'H6': '4',
            'D7': '8', 'G3': '5', 'F6': '3', 'H3': '3', 'A2': '6',
            'A7': '1'}
demo_hard = {'C3': '7', 'E5': '2', 'A4': '7', 'A2': '2', 'G4': '2', 'J4': '9',
             'F6': '7', 'E6': '5', 'G2': '8', 'J7': '6', 'B6': '2', 'H5': '5',
             'H7': '9', 'F2': '9', 'F5': '4', 'J6': '1', 'F8': '6', 'D8': '1',
             'F4': '1', 'J9': '4', 'B3': '8', 'E4': '6', 'B4': '5', 'D6': '3',
             'J5': '8', 'J8': '7', 'H6': '4', 'G8': '3', 'A5': '6', 'G6': '6',
             'C9': '6', 'C4': '4', 'H1': '7', 'D5': '9', 'G7': '5', 'D4': '8',
             'G9': '1', 'G5': '7', 'H4': '3', 'A1': '3', 'G3': '9', 'C6': '8',
             'C1': '9', 'A6': '9', 'D2': '7', 'G1': '4'}
demo_x = {'E8': '5', 'A8': '1', 'G2': '6', 'D4': '2', 'H2': '8', 'G8': '8',
          'C6': '5', 'G4': '1', 'A4': '8', 'B3': '8', 'C1': '1', 'F7': '1',
          'B7': '9', 'J9': '2', 'G1': '9', 'F4': '5', 'C7': '7', 'G6': '7',
          'E3': '1', 'H4': '6', 'J7': '6', 'D8': '4', 'H6': '9', 'G5': '2',
          'F9': '3', 'E1': '8', 'G3': '4', 'H8': '7', 'J8': '9', 'H9': '1',
          'H7': '4', 'G9': '5', 'J2': '1', 'D9': '9', 'E7': '2', 'H5': '5',
          'H3': '2', 'C8': '2', 'E4': '9', 'A7': '5', 'H1': '3', 'G7': '3',
          'C9': '8', 'D7': '8', 'E6': '6', 'B4': '7', 'B8': '3', 'J4': '4',
          'F8': '6', 'C4': '3', 'A3': '3', 'E9': '7'}


def render_defaults(*, grid=demo_easy, solvers=DEFAULT_METHODS, errors=None,
                    invalid=None):
    return render_template('base.html',
                           grid=grid,
                           solvers=solvers,
                           errors=errors,
                           invalid=invalid)


def do_solve(*, post_data):
    grid, solvers, _ = split_post(post_data=dict(post_data))
    if inv := invalid(grid=grid):
        return render_invalid(grid=grid,
                              solvers=solvers,
                              invalid=inv)

    to_solve = Game(grid=grid, solvers=solvers)
    to_solve.solve()
    return render_defaults(grid=to_solve.grid,
                           solvers=solvers,
                           errors=to_solve.errors,
                           invalid=to_solve.invalid_cells)


def do_step(*, post_data):
    grid, solvers, _ = split_post(post_data=dict(post_data))
    if inv := invalid(grid=grid):
        return render_invalid(grid=grid,
                              solvers=solvers,
                              invalid=inv)

    to_solve = Game(grid=grid, solvers=solvers)
    to_solve.solve_step()
    return render_defaults(grid=to_solve.grid,
                           solvers=solvers,
                           errors=to_solve.errors,
                           invalid=to_solve.invalid_cells)


def generate(*, post_data=None):
    return render_defaults()


def clear(*, post_data=None):
    return render_defaults(grid=None)


def analyse(*, post_data):
    return generate()
    # return render_template('analyse.html')
