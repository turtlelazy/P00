'''
Forgotten Charger: Lewis Cass, Aryaman Goenka, Oscar Wang, Owen Yaggy
Softdev
P00: Cookie and Sessions Introduction
2021-10-29
time spent: 0.5
'''
import sqlite3
import db_builder
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'forgotten charger'

# Utility function to check if there is a session
def logged_in():
    return session.get('username') is not None

@app.route('/', methods=['GET'])
def landing():
    # Check for session existance
    if logged_in():

        username = session['username']

        viewable_stories = db_builder.get_viewable_stories(username)
        editable_stories = db_builder.get_editable_stories(username)

        return render_template('index.html', username=username,viewable=viewable_stories, edtiable=editable_stories)

    else:
        # If not logged in, show login page
        return render_template('intro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    method = request.method

    # Check for session existance
    if method == 'GET':

        if logged_in():

            return redirect(url_for('landing'))
        else:
            # If not logged in, show login page
            return render_template('login.html', error=False)

    if method == 'POST':

        # Get information from request.form since it is submitted via post
        username = request.form['username']
        password = request.form['password']
        error = db_builder.login(username, password)

        if error:
            # If incorrect, give feedback to the user
            return render_template('login.html', error=error)
        else:
            # Store user info into a cookie
            session['username'] = username
            return redirect(url_for('landing'))

@app.route('/register', methods=['GET','POST'])
def register():
    method = request.method

    # Check for session existence
    if method == "GET":
        if logged_in():

            return redirect(url_for('landing'))
        else:
            # If not logged in, show regsiter page
            return render_template('register.html', error_message="")

    if method == "POST":
        new_username = request.form["new_username"]
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        error_message = ""
        if not new_username:
            error_message = "Error: No username entered!"
        elif not new_password:
            error_message = "Error: No password entered!"
        elif confirm_password != new_password:
            error_message = "Error: Passwords do not match!"

        if error_message:
            return render_template("register.html", error_message=error_message)

        error_message = db_builder.signup(new_username, new_password)

        if error_message:
            return render_template("register.html", error_message=error_message)
        else:
            session['username'] = new_username
            return redirect(url_for('landing'))


@app.route('/logout', methods=['GET', 'POST'])
def logout():

    # Once again check for a key before popping it
    if logged_in():
        session.pop('username')

    # After logout, return to login page
    return redirect(url_for('landing'))

# For editing a particular story
@app.route('/<int:story_id>/edit')
def edit_story(story_id):

    if logged_in():

        username = session['username']

        if db_builder.has_contributed(story_id, username):

            # Can only edit story that was not contributed to

            return redirect(url_for('view_story', story_id=story_id))
        else:
            title, story, latest_update = db_builder.view_story(story_id)
            return render_template('edit.html', latest=latest_update)

    else:
        return redirect(url_for('landing'))

@app.route('/edit')
def submit_edit():
    method = request.method

    if method == "GET":
        return redirect(url_for('landing'))

# For viewing a particular story
@app.route('/<int:story_id>/view')
def view_story(story_id):

    if logged_in():

        title, story, last_update = db_builder.view_story(story_id)
        return render_template('view.html', title=title, story=story)

    else:
        return redirect(url_for('landing'))


# For handling submission of a new story
@app.route('/new', methods=['GET','POST'])
def add_story():

    method = request.method

    if method == 'GET':
        return render_template('new.html')

    if method == 'POST':

        title = request.form['title']
        story = request.form['story_text']
        confirm = request.form['submit']

        # Checks if form submited was either to confirm or add
        if confirm == "Confirm":

            # make changes in database
            db_builder.new_story(title, story, session['username'])

            return redirect(url_for('landing'))

        error_message = ""
        if not title:
            error_message = "Please give your story a title."
        elif not story:
            error_message = "You cannot have an empty story."

        print(error_message)
        if error_message:
            return render_template(
                'new.html',
                title = title,
                story = story,
                message = error_message
            )
        return render_template(
            'confirm_add.html',
            title = title,
            story = story
        )

# Handles when a user visits a page without a route
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.debug = True
    app.run()
