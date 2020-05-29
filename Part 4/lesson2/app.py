from flask import Flask , request

app = Flask(__name__)


@app.route('/headers')
def headers():

    auth_header = request.headers['Authorization']

    print(auth_header)
    return "not implimented"
