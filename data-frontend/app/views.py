import json

from flask import render_template, redirect, request, url_for

from . import app


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        questions = list()
        with open(app.config['QUESTIONS_FILE']) as f:
            for l in f:
                questions.append(l.strip())

        return render_template('index.html', l=questions)

    data = json.loads(request.form['data'])
    with open(app.config['DATA_FILE'], 'a') as f:
        for d in data['tagged']:
            f.write(d.strip() + '\n')

    print(data)
    return redirect(url_for('thanks'))


@app.route('/thanks')
def thanks():
    return render_template('thanks.html')
