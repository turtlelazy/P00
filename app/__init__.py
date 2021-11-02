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

# Temporary username and password system
TEMP_USER = 'user'
TEMP_PASS = 'pass'

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

    method = request.method

    if method == 'GET':

        # Check for session existance
        if logged_in():
            return redirect(url_for('landing'))
        else:
            # If not logged in, show login page
            return render_template('login.html', error=False)

    if method == 'POST':

        # Get information from request.form since it is submitted via post
        username = request.form['username']
        password = request.form['password']

        if username == TEMP_USER and password == TEMP_PASS:
            # Store user info into a cookie
            session['username'] = username
            return redirect(url_for('landing'))

        else:

            # If incorrect, give feedback to the user
            return render_template('login.html', error=True)

@app.route('/logout', methods=['GET', 'POST'])
def logout():

    # Once again check for a key before popping it
    if logged_in():
        session.pop('username')

    # After logout, return to login page
    return redirect(url_for('landing'))



@app.route('/register', methods=['GET','POST'])
def register():
    # Check for session existance
    if logged_in():
        return redirect(url_for('landing'))
    else:
        # If not logged in, show login page
        return render_template('register.html')

# For editing a particular story
@app.route('/<int:story_id>/edit')
def edit_story(story_id):
    pass

# For viewing a particular story
@app.route('/<int:story_id>')
def view_story(story_id):
    pass

# For creating a new story
@app.route('/new')
def new_story():
    pass

# Handles when a user visits a page without a route
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

# Utility function to check if there is a session
def logged_in():
    return session.get('username') is not None



if __name__ == '__main__':
    app.debug = True
    app.run()
