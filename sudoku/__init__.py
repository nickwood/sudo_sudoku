from flask import Flask, render_template


def create_app(test_config=None):
    app = Flask(__name__)

    @app.route('/')
    @app.route('/<grid>')
    def solve(grid=None):
        return render_template('solve.html', grid=grid)

    @app.route('/generate')
    def generate(grid=None):
        return render_template('generate.html', grid=grid)

    @app.route('/analyse')
    def analyse(grid=None):
        return render_template('analyse.html', grid=grid)

    return app
