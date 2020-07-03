from flask import Flask, request
from flask_scss import Scss

from sudoku.grid import Grid
from sudoku.solution import Solution

__all__ = ['Grid', 'Solution']
import sudoku.response_generators as response


def create_app(test_config=None):
    app = Flask(__name__)
    Scss(app)

    @app.route('/')
    def home_route():
        return response.generate()

    @app.route('/solve', methods=['POST'])
    def solve_sudoku():
        return response.do_solve(post_data=request.form)

    @app.route('/step', methods=['POST'])
    def step_route():
        return response.do_step(post_data=request.form)

    @app.route('/generate', methods=['POST', 'GET'])
    def generate_route():
        return response.generate(post_data=request.form)

    @app.route('/analyse', methods=['POST'])
    def analyse_route():
        return response.analyse(post_data=request.form)

    @app.route('/clear', methods=['POST', 'GET'])
    def clear_route():
        return response.clear()

    return app


# if __name__ == "__main__":
#     create_app().run()
