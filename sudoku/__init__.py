from flask import Flask, request
from flask_scss import Scss
import sudoku.response_generators as response


def create_app(test_config=None):
    app = Flask(__name__)
    Scss(app)

    @app.route('/')
    @app.route('/solve', methods=['GET', 'POST'])
    def solve_sudoku():
        if request.method == 'GET':
            demo = {'A1': '5', 'A2': '6', 'A4': '8', 'A5': '4', 'A6': '7',
                    'B1': '3', 'B3': '9', 'B7': '6', 'C3': '8', 'D2': '1',
                    'D5': '8', 'D8': '4', 'E1': '7', 'E2': '9', 'E4': '6',
                    'E6': '2', 'E8': '1', 'E9': '8', 'F2': '5', 'F5': '3',
                    'F8': '9', 'G7': '2', 'H3': '6', 'H7': '8', 'H9': '7',
                    'J4': '3', 'J5': '1', 'J6': '6', 'J8': '5', 'J9': '9'}
            return response.home(grid=demo)
        else:
            return response.do_solve(post_data=request.form)

    @app.route('/generate')
    def generate_route():
        return response.generate()

    @app.route('/analyse', methods=['GET', 'POST'])
    def analyse_route():
        if request.method == 'GET':
            pass
        else:
            return response.analyse(post_data=request.form)

    return app
