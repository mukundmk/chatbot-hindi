import json
from random import shuffle

from flask import render_template, redirect, request, session, url_for

from . import app


@app.route('/')
def index():
    questions = list()
    with open(app.config['QUESTIONS_FILE']) as f:
        for l in f:
            questions.append(l.strip())

    if request.method == 'GET':
        if 'unanswered' in session and session['unanswered']:
            q = list(reversed([int(x) for x in session['unanswered'].split(',')]))

        elif 'questions' in session and session['questions']:
            q = [int(x) for x in session['questions'].split(',')]

        elif 'questions' not in session:
            q = list(range(len(questions)))
            shuffle(q)

        else:
            return redirect(url_for('thanks'))

        l = list()
        u = list()
        for i in range(10):
            if q:
                temp = q.pop()
                u.append(temp)
                l.append(questions[temp])
            else:
                break

        session['unanswered'] = ','.join([str(x) for x in u])
        session['questions'] = ','.join(q)

        return render_template('index.html', l=l)

    session['unanswered'] = ''
    data = json.loads(request.form['data'])
    with open(app.config['DATA_FILE'], 'a') as f:
        for d in data['tagged']:
            f.write(d + '\n')

    if 'questions' in session and session['questions']:
        return redirect(url_for('index'))

    return redirect(url_for('thanks'))


@app.route('/thanks')
def thanks():
    return render_template('thanks.html')
