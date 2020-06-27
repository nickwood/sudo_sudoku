from collections import ChainMap
from flask import render_template
from .solver import invalid, Game


DEFAULT_METHODS = {'naked_singles': True,
                   'hidden_singles': True,
                   'naked_pairs': True,
                   'naked_triples': True,
                   'naked_quads': True,
                   'pointing_multiples': True,
                   'box_line_reductions': True,
                   'x_wings': True}


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
demo_pointing_pairs = {'J8': '2', 'H5': '3', 'E8': '7', 'A6': '3', 'C9': '7',
                       'J7': '7', 'G9': '5', 'D5': '1', 'G1': '7', 'B5': '8',
                       'F3': '4', 'J4': '6', 'D8': '3', 'F7': '2', 'C7': '5',
                       'D7': '4', 'A2': '1', 'F8': '5', 'F2': '6', 'F5': '7',
                       'G3': '1', 'A3': '7', 'A7': '6', 'J6': '1', 'D2': '7',
                       'G8': '6', 'C1': '9', 'E6': '2', 'A4': '9', 'D3': '2',
                       'E4': '4', 'F4': '3', 'J3': '5'}
demo_bl_red = {'J3': '3', 'D8': '7', 'G2': '6', 'C1': '4', 'B8': '2',
               'D9': '5', 'J4': '5', 'E5': '8', 'F8': '4', 'G3': '4',
               'J1': '1', 'E3': '7', 'A5': '4', 'A7': '7', 'F3': '1',
               'E2': '4', 'G9': '1', 'H3': '8', 'H5': '3', 'A8': '8',
               'B9': '4', 'B2': '7', 'F7': '2', 'D7': '6', 'A6': '2',
               'B4': '6', 'F9': '8'}
demo_x = {'D3': '2', 'G5': '4', 'D6': '4', 'J7': '2', 'F6': '7', 'F7': '3',
          'B8': '5', 'A4': '4', 'D2': '5', 'E3': '1', 'F5': '5', 'C4': '5',
          'C3': '3', 'C7': '7', 'H2': '2', 'E1': '3', 'C8': '8', 'B3': '6',
          'H7': '9', 'C5': '6', 'J1': '5', 'G2': '3', 'E6': '6', 'F8': '2',
          'A9': '2', 'C9': '4', 'A7': '6', 'D4': '3', 'H6': '5', 'B7': '1',
          'J8': '4', 'J3': '7', 'G6': '2', 'E9': '5', 'C1': '2', 'C6': '1',
          'E4': '2', 'A3': '5', 'D7': '8', 'B5': '2', 'E7': '4', 'H3': '4',
          'J6': '9', 'C2': '9', 'G8': '6', 'G7': '5'}


def render_defaults(*, grid=demo_bl_red, solvers=DEFAULT_METHODS,
                    errors=None, invalid=None, logs=None):
    return render_template('base.html',
                           grid=grid,
                           solvers=solvers,
                           errors=errors,
                           invalid=invalid,
                           logs=logs)


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
                           logs=to_solve.logs,
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
                           logs=to_solve.logs,
                           invalid=to_solve.invalid_cells)


def generate(*, post_data=None):
    return render_defaults()


def clear(*, post_data=None):
    return render_defaults(grid=None)


def analyse(*, post_data):
    return generate()
    # return render_template('analyse.html')
