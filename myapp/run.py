# -*- coding: UTF-8 -*-
from flask import Flask, render_template, request, url_for
from words_puzzle import loads_sprite, solve_puzzle

app = Flask(__name__)


@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route('/puzzle', methods=['POST', 'GET'])
def app_puzzle():
    if request.method == 'POST':
        puzzle = request.form['puzzle']
        ans = solve_puzzle(puzzle, sprite_names)
        return render_template('input_puzzle.html', answer=ans)
    return render_template('input_puzzle.html')


if __name__ == '__main__':
    sprite_names = loads_sprite()
    app.run(host='0.0.0.0', debug=True)
