from flask import Flask, render_template, request
from flask_scss import Scss
from .solver import split_post_data, invalid


def create_app(test_config=None):
    app = Flask(__name__)

    Scss(app)

    @app.route('/')
    @app.route('/solve', methods=['GET', 'POST'])
    def solve():
        if request.method == 'GET':
            return render_template('base.html')
        else:
            grid, params = split_post_data(post_data=dict(request.form))
            invalid_cells = invalid(grid=grid)
            if invalid_cells:
                errors = ['Invalid entries at: ' + ', '.join(invalid_cells)]
            else:
                errors = None

            return render_template('base.html',
                                   grid=grid,
                                   params=params,
                                   errors=errors,
                                   invalid=invalid_cells)

    @app.route('/generate')
    def generate():
        return render_template('generate.html')

    @app.route('/analyse', methods=['GET', 'POST'])
    def analyse():
        if request.method == 'GET':
            return render_template('analyse.html')
        else:
            data = request.form
            return render_template('analyse.html', data=data)

    return app
