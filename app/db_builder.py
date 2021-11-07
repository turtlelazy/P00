'''
Forgotten Charger: Lewis Cass, Aryaman Goenka, Oscar Wang, Owen Yaggy
Softdev
P00: Cookie and Sessions Introduction
2021-10-29
time spent: 0.5
'''

import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O

DB_FILE="StoryCharger.db"

def dbseteup():
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

    c.execute("DROP TABLE IF EXISTS Users")
    command = "CREATE TABLE Users (ID INTEGER PRIMARY KEY AUTOINCREMENT, Username TEXT, Password TEXT)"    
    c.execute(command)      # test SQL stmt in sqlite3 shell, save as string
    # run SQL statement

    c.execute("DROP TABLE IF EXISTS Stories")
    command = "CREATE TABLE Stories (ID INTEGER PRIMARY KEY AUTOINCREMENT, Title TEXT, FullStory TEXT, Latest_Update TEXT)"
    c.execute(command)      # test SQL stmt in sqlite3 shell, save as string
    # run SQL statement

    c.execute("DROP TABLE IF EXISTS Contributions")
    command = "CREATE TABLE Contributions (ID INTEGER PRIMARY KEY AUTOINCREMENT, UserID INTEGER, StoryID INTEGER, Contribution TEXT)"
    c.execute(command)

    db.commit() #save changes
    db.close()  #close database

# gets the user I
def get_id(username):
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

    command = "SELECT * FROM Users"
    c.execute(command)

    table = c.fetchall()

    for row in table:      #searches for the username in Users
        if row[1] == username:
            return row[0]    #returns the User ID of the user

# returns a list of story IDs for the stories the user has contributed to
# same function for all the stories the user can view
def get_viewable_stories(username):
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

    contribution_ids = []

    command = "SELECT * FROM Contributions"
    c.execute(command)
    
    table = c.fetchall()

    user_id = get_id(username)

    for row in table:
        uid = row[2]
        if user_id == uid:
            story_id = row[1]
            contribution_ids.append((story_id, get_story_title_by_id(story_id)))
    
    return contribution_ids

# returns a list of story IDs for the stories the user has not contributed to
def get_editable_stories(username):
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events
    command = "SELECT * FROM Contributions"
    c.execute(command)
    table = c.fetchall()
    user_id = get_id(username)

    editable_stories = []    #stores the IDs of all stories the user has not contributed to
    for row in table:
        uid = row[2]
        if uid != user_id:
            story_id = row[1]
            if not editable_stories.__contains__(story_id):
                editable_stories.append((story_id, get_story_title_by_id(story_id)))
    
    return editable_stories

# returns True if the user has contributed to the story and False otherwise
def has_contributed(username, story_id):
    contributions = get_viewable_stories(username)
    if story_id in contributions:
        return True
    else:
        return False

def signup(username, password):
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create

    c = db.cursor()

    ##dbseteup()

    c.execute("""SELECT Username FROM Users WHERE Username=?""",[username])
    result = c.fetchone()

    if result:
        return(True, "Username already exists")

    else:
        c.execute('INSERT INTO Users VALUES (null, ?, ?)', (username, password))
        db.commit()
        db.close()
        return(False, "Welcome")


def login(username, password):
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create

    c = db.cursor()

    c.execute("""SELECT Username FROM Users WHERE Username=? AND Password=?""",[username, password])
    result = c.fetchone()

    if result:
        ##access this specifc user data
        return(False)

    else:
        return(True)


def new_story(title, story, username):
    db = sqlite3.connect(DB_FILE)  # open if file exists, otherwise create
    c = db.cursor()

    c.execute('INSERT INTO Stories VALUES (null, ?, ?, ?)', (title, story, story))

    c.execute("SELECT ID FROM Stories WHERE Title=? AND Latest_Update=? AND FullStory=?", [title, story, story])
    story_id = c.fetchone()[0]

    c.execute("SELECT ID FROM Users WHERE Username=?", [username])
    user_id = c.fetchone()[0]

    c.execute('INSERT INTO Contributions VALUES (null, ?, ?, ?)', (story_id, user_id, story))

    db.commit()
    db.close()


def edit_story(story_id, story, new_update, username):
    db = sqlite3.connect(DB_FILE)  # open if file exists, otherwise create
    c = db.cursor()

    c.execute('UPDATE Stories SET FullStory=? AND Latest_Update=? WHERE ID=?', (story, new_update, story_id))

    c.execute("SELECT ID FROM Users WHERE Username=?", [username])
    user_id = c.fetchone()[0]

    c.execute('INSERT INTO Contributions VALUES (null, ?, ?, ?)', (story_id, user_id, new_update))

    db.commit()
    db.close()

def view_story(story_id):
    db = sqlite3.connect(DB_FILE)  # open if file exists, otherwise create
    c = db.cursor()

    c.execute("SELECT Title FROM Stories WHERE ID=?", [story_id])
    row = c.fetchone()
    if row is not None:
        Title = row[0]

    c.execute("SELECT FullStory FROM Stories WHERE ID=?", [story_id])
    row = c.fetchone()
    if row is not None:
        Story = row[0]

    c.execute("SELECT Latest_Update FROM Stories WHERE ID=?", [story_id])
    row = c.fetchone()
    if row is not None:
        LatestUpdate = row[0]
    
    return (Title, Story, LatestUpdate)

def get_story_title_by_id(story_id):
    db = sqlite3.connect(DB_FILE)  # open if file exists, otherwise create
    c = db.cursor()

    c.execute("SELECT Title FROM Stories WHERE ID=?", [story_id])
    title = c.fetchone()[0]

    db.commit()
    db.close()

    return title
