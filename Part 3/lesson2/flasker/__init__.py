from flask import Flask, jsonify
import os


def create_app(test_config=None):
    app = Flask(__name__)

    @app.route('/')
    def hello():
        return jsonify({'message': 'Hello World'})

    @app.route('/happy')
    def happy():
        return ':)'

    return app
