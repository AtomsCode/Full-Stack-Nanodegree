from flask import Flask , request , abort

app = Flask(__name__)

def get_token_header():

    if 'Authorization' not in request.headers:
        abort(401)

    auth_header = request.headers['Authorization']
    header_parts = auth_header.split(' ')

    if len(header_parts) != 2:
        abort(401)
    elif header_parts[0].lower().strip() != 'bearer':
        abort(401)
    return header_parts[1]

@app.route('/headers')
def headers():

    jwt = get_token_header()

    print(jwt)

    return "not implimented"
