#! /usr/bin/python3
import json
from os import system
from flask import Flask, jsonify
app = Flask(__name__)


@app.route('/', methods=['GET'])
def ReturnJSON():
    system('./main.py -sc')
    return jsonify(json.load(open('test.json')))


if __name__ == '__main__':
    app.run(debug=True)
