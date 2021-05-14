# server.py
from flask import Flask, request, jsonify
import sys
import json

server = Flask(__name__)

def log(str):
    print(str, file=sys.stderr)

# avoid CORS problem: https://stackoverflow.com/questions/26980713/solve-cross-origin-resource-sharing-with-flask
def enableCORS(js):
    response = jsonify(js)
    response.headers.add('Access-Control-Allow-Origin', '*')
    log(js)
    return response

@server.route('/getmsg/', methods=['GET'])
def respond():
    return enableCORS({'msg': 'http log server is running'})

@server.route('/post/', methods=['POST'])
def post_something():
    return enableCORS(json.loads(request.data))

# A welcome message to test our server
@server.route('/')
def index():
    return "<h1>Welcome to our server!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    server.run(threaded=True, port=5000, debug=True)