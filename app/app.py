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

@app.route('/', methods=['GET'])
def landing():

    # Check for session existance
    if logged_in():
        return render_template('index.html')
    else:
        # If not logged in, show login page
        return render_template('intro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Check for session existance
    if logged_in():
        return redirect(url_for('landing'))
    else:
        # If not logged in, show login page
        return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    # Check for session existance
    if logged_in():
        return redirect(url_for('landing'))
    else:
        # If not logged in, show login page
        return render_template('register.html')

@app.route('/<int:story_id>/edit')
def edit_story(story_id):
    pass

@app.route('/<int:story_id>')
def view_story(story_id):
    pass

@app.route('/new')
def new_story():
    pass

@app.errorhandler(404)
def not_found():
    pass

def logged_in():
    return session.get('username') is not None



if __name__ == '__main__':
    app.debug = True
    app.run()
