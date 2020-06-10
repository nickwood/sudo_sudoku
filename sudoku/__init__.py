from flask import Flask, render_template, request
from flask_scss import Scss


def create_app(test_config=None):
    app = Flask(__name__)

    Scss(app)

    @app.route('/')
    @app.route('/solve', methods=['GET', 'POST'])
    def solve():
        if request.method == 'GET':
            return render_template('solve.html')
        else:
            post_data = request.form
            return render_template('solve.html', data=post_data)

    @app.route('/generate')
    def generate():
        return render_template('generate.html')

    @app.route('/analyse', methods=['GET', 'POST'])
    def analyse():
        if request.method == 'GET':
            return render_template('analyse.html')
        else:
            post_data = request.form
            return render_template('analyse.html', data=post_data)


    return app
