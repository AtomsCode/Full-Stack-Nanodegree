from flask import Flask, jsonify
from flask_cors import CORS

def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)
  

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/')
    def hello():
        return jsonify({'message': 'Hello World'})

    @app.route('/entrees/<int:entree_id>')
    def retrieve_entree(entree_id):
        return 'Entree %d' % entree_id


    return app
