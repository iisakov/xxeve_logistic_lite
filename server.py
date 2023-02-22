#! /usr/bin/python3
import json
from os import system

from flask import Flask, render_template
app = Flask(__name__)


config = json.load(open('config.json'))


@app.route('/', methods=['GET'])
def index():
    path = 'index.html'
    return render_template(path, as_attachment=True)


@app.route('/sc/<string:mode>/<string:from_solar_system>/<string:to_solar_system>/', methods=['GET'])
def get_security_check(mode, from_solar_system, to_solar_system):
    mode = mode if mode in ['shortest', 'secure', 'insecure'] else config['CLI_param']['-sc']['sub_params']['scm']['default']

    system(f'./main.py -w -sc scm:{mode} scf:{from_solar_system} sct:{to_solar_system}')
    return json.load(open(f'./test.json'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
