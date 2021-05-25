# server.py
from flask import Flask, request, jsonify
import sys
import json
from uuid import uuid4
from base64 import b64decode

server = Flask(__name__)

credential = {
    'user' : 'genesys',
    'password': 'Pa55w0rd'
}

def log(str):
    print(str, file=sys.stderr)

# avoid CORS problem: https://stackoverflow.com/questions/26980713/solve-cross-origin-resource-sharing-with-flask
def enableCORS(js):
    response = jsonify(js)
    response.headers.add('Access-Control-Allow-Origin', '*')
    log(js)
    return response

def getUuid():
    return uuid4()

def checkAuth(basicAuthStr):
    auth = basicAuthStr.split()
    if len(auth)!=2:
        return False
    else:
        secret = b64decode(auth[1]).decode('utf-8').split(":")
        if len(secret) != 2:
            return False
        return (secret[0]==credential["user"] and secret[1]==credential["password"])

def prepareResponse(data):
    res = {}
    res["id"] = getUuid()
    res["data"] = data
    return res

@server.route('/getmsg/', methods=['GET'])
def respond():
    return enableCORS({'msg': 'http log server is running'})

@server.route('/post/', methods=['POST'])
def post_something():
    if 'Authorization' in request.headers:
        if checkAuth(request.headers['Authorization']):
            return enableCORS(prepareResponse(json.loads(request.data)))
    return enableCORS({'msg': 'Authentication Error!!!'})

# A welcome message to test our server
@server.route('/')
def index():
    return "<h1>Welcome to our server!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    server.run(threaded=True, port=5000, debug=True)