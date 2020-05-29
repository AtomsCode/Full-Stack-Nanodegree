from flask import Flask , request

app = Flask(__name__)


@app.route('/headers')
def headers():
    print('hello world')
    return "not implimented"
