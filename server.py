#! /usr/bin/python3
import json
from os import system
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    path = 'index.html'
    return render_template(path, as_attachment=True)


@app.route('/sc/', methods=['GET'])
def get_security_check():
    system('./main.py -w -sc')
    return json.load(open('test.json'))


if __name__ == '__main__':
    app.run()
