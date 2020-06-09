from flask import Flask, render_template


def create_app(test_config=None):
    app = Flask(__name__)

    @app.route('/')
    @app.route('/solve')
    # @app.route('/solve?grid=<grid>')
    # @app.route('/<grid>')
    def solve():
        return render_template('solve.html')

    @app.route('/generate')
    def generate():
        return render_template('generate.html')

    @app.route('/analyse')
    def analyse():
        return render_template('analyse.html')

    return app
