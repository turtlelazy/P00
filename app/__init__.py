import sqlite3
import db_builder
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'forgotten charger'

# Utility function to check if there is a session
def logged_in():
    return session.get('username') is not None

@app.route('/', methods=['GET', 'POST'])
def landing():
    # Check for session existance
    if logged_in():

        # Retrieve list of viewable and edtiable stories
        username = session['username']
        viewable_stories, editable_stories = db_builder.split_viewable_stories(username)

        # Get filter if there is a post request from the search bar
        filter=""
        if request.method == "POST":
            filter = request.form["search"]

            # Filters out the viewable and edtiable stories based on the search bar entry
            # Checks if the filter is a case-insensitive substring of the title
            viewable_stories = [(id, title) for id, title in viewable_stories if filter.lower() in title.lower()]
            editable_stories = [(id, title) for id, title in editable_stories if filter.lower() in title.lower()]

        return render_template('index.html', username=username, viewable=viewable_stories, edtiable=editable_stories, search=filter)


    else:
        # If not logged in, show login page
        return render_template('intro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    method = request.method

    # Handle regular viewing of the login page
    if method == 'GET':

        if logged_in():

            # Redirect to the main page if they are logged in
            return redirect(url_for('landing'))
        else:
            # If not logged in, show login page
            return render_template('login.html', error=False)

    if method == 'POST':

        # Get information from request.form since it is submitted via post
        username = request.form['username']
        password = request.form['password']

        # Get response from the database
        error = db_builder.login(username, password)

        if error:
            # If incorrect, give feedback to the user
            return render_template('login.html', error=error)
        else:

            # Store user info into a cookie and return to main page
            session['username'] = username
            return redirect(url_for('landing'))

@app.route('/register', methods=['GET','POST'])
def register():
    method = request.method


    if method == "GET":
        if logged_in():
            # If logged in, redirect to main page
            return redirect(url_for('landing'))
        else:
            # If not logged in, show regsiter page
            return render_template('register.html', error_message="")

    if method == "POST":

        # Get information from the form
        new_username = request.form["new_username"]
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        # Generate error message
        error_message = ""
        if not new_username:
            error_message = "Error: No username entered!"
        elif not new_password:
            error_message = "Error: No password entered!"
        elif confirm_password != new_password:
            error_message = "Error: Passwords do not match!"

        # Empty quote will return false
        if error_message:
            return render_template("register.html", error_message=error_message)

        # Check once again against the database
        error_message = db_builder.signup(new_username, new_password)

        # Empty quotes from the database method will return false
        if error_message:
            return render_template("register.html", error_message=error_message)
        else:

            # Start a session and redirect to the main page
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
@app.route('/<int:story_id>/edit', methods=['GET', 'POST'])
def edit_story(story_id):

    if not logged_in() or not db_builder.check_story(story_id):
        # If not logged in, redirect to the main page
        return redirect(url_for('landing'))


    method = request.method
    username = session['username']

    # Can only edit story that was not contributed to
    if db_builder.has_contributed(story_id, username):

        # Have the user view the full story instead
        return redirect(url_for('view_story', story_id=story_id))


    if method == "GET":

        # Get all information about a story to edit
        title, story, latest_update = db_builder.get_story(story_id)

        return render_template('edit.html', story_id=story_id, title=title, latest=latest_update)

    # submitting the edit
    elif method == "POST":


        # gets information on the story from the db
        title, story, previous_update = db_builder.get_story(story_id)


        # Check if it was a confirm post or just from the main edit page
        latest_update = request.form["contribution"]
        confirm = request.form['submit']

        if confirm == "Confirm":

            # Get the latest update and append it along with two newlines
            # Newlines are for easy formatting when viewing the story

            story += "\n\n" + latest_update

            # submits the edit to the db
            db_builder.edit_story(story_id, story, latest_update, username)
            return redirect(url_for('landing'))

        # Generate error message
        print(not latest_update)
        error_message = ""
        if not latest_update:
            error_message = "You cannot have an empty update."

        # Empty quotes will return false
        if error_message:

            # Give feedback to the user
            return render_template(
                'edit.html',
                title=title,
                latest_update=latest_update,
                story_id=story_id,
                message=error_message
            )

        else:

            # Show them a confirmation page
            return render_template(
                'confirm_edit.html',
                title=title,
                latest_update=latest_update,
                previous_update=previous_update,
                story_id=story_id
            )



# For viewing a particular story
@app.route('/<int:story_id>')
def view_story(story_id):

    if logged_in() and db_builder.check_story(story_id):

        username = session['username']

        # Can only view a story that the user has contributed to
        if db_builder.has_contributed(story_id, username):

            # Get relevant information about a story
            title, story, _ = db_builder.get_story(story_id)
            return render_template('view.html', title=title, story=story)

        else:

            # Have them contribute to the story first
            return redirect(url_for('edit_story', story_id=story_id))
    else:

        # If not logged in redirect to main page
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
        # Generate error message
        error_message = ""
        if not title:
            error_message = "Please give your story a title."
        elif not story:
            error_message = "You cannot have an empty story."

        # Empty quotes will return false
        if error_message:

            # Give feedback to the user
            return render_template(
                'new.html',
                title = title,
                story = story,
                message = error_message
            )

        else:

            # Show user a confirmation page
            return render_template(
                'confirm_add.html',
                title = title,
                story = story
            )

# Handles when a user visits a page without a route
# Ensures app will not crash
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    # db_builder.dbseteup()
    app.debug = True
    app.run()
