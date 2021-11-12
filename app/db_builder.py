import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O
import werkzeug.security

DB_FILE="StoryCharger.db"

# Drops each table and resets them
def dbseteup():
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()

    c.execute("DROP TABLE IF EXISTS Users")
    command = "CREATE TABLE Users (ID INTEGER PRIMARY KEY AUTOINCREMENT, Username TEXT, Password TEXT)"
    c.execute(command)

    c.execute("DROP TABLE IF EXISTS Stories")
    command = "CREATE TABLE Stories (ID INTEGER PRIMARY KEY AUTOINCREMENT, Title TEXT, FullStory TEXT, LatestUpdate TEXT)"
    c.execute(command)      # test SQL stmt in sqlite3 shell, save as string
    # run SQL statement

    c.execute("DROP TABLE IF EXISTS Contributions")
    command = "CREATE TABLE Contributions (ID INTEGER PRIMARY KEY AUTOINCREMENT, UserID INTEGER, StoryID INTEGER, Contribution TEXT)"
    c.execute(command)

    db.commit() #save changes
    db.close()  #close database

# Returns a list of viewable stories and editable stories
def split_viewable_stories(username):
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

    # Gets a set of all storyIDs
    c.execute("SELECT ID FROM Stories")
    all_story_ids = set([entry[0] for entry in c.fetchall()])

    user_id = get_id(username)
    c.execute("SELECT StoryID FROM Contributions WHERE UserID=?", [user_id])

    # Uses a set since there are many contributions to each story
    contributed_story_id_set = set([entry[0] for entry in c.fetchall()])

    # Viewable stories are those the user has contributed to
    # Editable ones are the existing stories removing the viewable ones
    # Each is a list of tuples containing story_ids and their associated story title
    viewable_story_list = [(story_id, get_story_title_by_id(story_id)) for story_id in contributed_story_id_set]

    editable_story_list = [(story_id, get_story_title_by_id(story_id)) for story_id in all_story_ids.difference(contributed_story_id_set)]


    db.commit() #save changes
    db.close()  #close database

    return (viewable_story_list, editable_story_list)


# returns True if the user has contributed to the story and False otherwise
def has_contributed(story_id, username):
    contributions, _ = split_viewable_stories(username)

    # Each entry is a tuple containing story_id and its associated title
    # Entry[0] is thus the story id
    if story_id in [entry[0] for entry in contributions]:
        return True
    else:
        return False

# Adds to the user database if the username is availible
# Returns an error message to display if there was an issue or an empty string otherwise
def signup(username, password):
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()

    # Checks if username already exists
    c.execute("""SELECT Username FROM Users WHERE Username=?""",[username])
    result = c.fetchone()

    if result:
        return "Error: Username already exists"

    else:
        c.execute('INSERT INTO Users VALUES (null, ?, ?)', (username, password))

        db.commit()
        db.close()

        # Uses empty quotes since it will return false when checked as a boolean
        return  ""

# Tries to check if the username and password are valid
def login(username, password):
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()

    # Checks if username and password combination exists
    c.execute("""SELECT Username FROM Users WHERE Username=? AND Password=?""",[username, password])
    result = c.fetchone()

    if result:
        ##access this specifc user data
        return False

    else:
        return True


# Creates a new story under a user
def new_story(title, story, username):
    db = sqlite3.connect(DB_FILE)  # open if file exists, otherwise create
    c = db.cursor()

    # Adds an entry into the Story database
    c.execute('INSERT INTO Stories VALUES (null, ?, ?, ?)', (title, story, story))

    # Gets relevant story and user ids
    c.execute("SELECT ID FROM Stories WHERE Title=? AND LatestUpdate=? AND FullStory=?", [title, story, story])
    story_id = c.fetchone()[0]
    user_id = get_id(username)

    # Records contribution into contribution database
    c.execute('INSERT INTO Contributions VALUES (null, ?, ?, ?)', (user_id, story_id, story))

    db.commit()
    db.close()

# Adds another contribution to a story
def edit_story(story_id, story, new_update, username):
    db = sqlite3.connect(DB_FILE)  # open if file exists, otherwise create
    c = db.cursor()

    # Modofies the stories fullstory and the latestupdate
    c.execute('UPDATE Stories SET FullStory=?, LatestUpdate=? WHERE ID=?', [story, new_update, story_id])

    # Inserts another contribution into contribution database
    user_id = get_id(username)
    c.execute('INSERT INTO Contributions VALUES (null, ?, ?, ?)', (user_id, story_id, new_update))

    db.commit()
    db.close()

# Returns all the relevant information regarding a story
def get_story(story_id):
    db = sqlite3.connect(DB_FILE)  # open if file exists, otherwise create
    c = db.cursor()

    # Retrieves all relevant information given a story_id
    c.execute("SELECT Title, FullStory, LatestUpdate FROM Stories WHERE ID=?", [story_id])
    row = c.fetchone()

    title = row[0]
    full_story = row[1]
    latest_update = row[2]

    db.commit()
    db.close()


    return title, full_story, latest_update

# Gets the title of a story given a story_id
def get_story_title_by_id(story_id):
    db = sqlite3.connect(DB_FILE)  # open if file exists, otherwise create
    c = db.cursor()

    c.execute("SELECT Title FROM Stories WHERE ID=?", [story_id])
    title = c.fetchone()[0]

    db.commit()
    db.close()

    return title

# gets the user
def get_id(username):
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

    user_ID = None
    c.execute("SELECT ID FROM Users WHERE Username=?", [username])
    row = c.fetchone()
    if row is not None:
        user_ID = row[0]

    return user_ID

def check_story(story_id):
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

    c.execute("SELECT * FROM Stories WHERE ID=?", [story_id])
    row = c.fetchone()

    return row is not None
