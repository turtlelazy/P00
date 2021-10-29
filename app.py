'''
Forgotten Charger: Lewis Cass, Aryaman Goenka, Oscar Wang
Softdev
P00: Cookie and Sessions Introduction
2021-10-29
time spent: 0.5
'''

from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'forgotten charger'

@app.route('/', methods=['GET', 'POST'])
def landing():

    # Check for session existance
    if session.get('username') is not None:

        return render_template('index.html')
    else:

        # If not logged in, show login page
        return render_template('intro.html')

@app.route('/login')
def login():
    pass


if __name__ == '__main__':
    app.debug = True
    app.run()
