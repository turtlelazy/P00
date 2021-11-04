'''
Forgotten Charger: Lewis Cass, Aryaman Goenka, Oscar Wang
Softdev
P00: Cookie and Sessions Introduction
2021-10-29
time spent: 0.5
'''

import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O

def dbseteup():
    DB_FILE="StoryCharger.db"

    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

    #==========================================================

    # < < < INSERT YOUR TEAM'S POPULATE-THE-DB CODE HERE > > >

    c.execute("Drop Table if exists Users")
    command = "Create Table Users (Username Text, Password Integer)"    
    c.execute(command)      # test SQL stmt in sqlite3 shell, save as string
    # run SQL statement

    c.execute("Drop Table if exists Stories")
    command = "Create Table Stories (Title Text, FullStory Text, Latest_Update Text)"    
    c.execute(command)      # test SQL stmt in sqlite3 shell, save as string
    # run SQL statement

    c.execute("Drop Table if exists Contributions")
    command = "Create Table Contributions (UserID Integer, StoryID Integer, id Primary Key)"    
    c.execute(command)      # test SQL stmt in sqlite3 shell, save as string
    # run SQL statement

    #==========================================================
    db.commit() #save changes
    db.close()  #close database

def signup(username, password):
    DB_FILE="StoryCharger.db"
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create

    c = db.cursor()  
    ##dbseteup()

    c.execute("""SELECT Username FROM Users WHERE Username=?""",[username])
    result = c.fetchone()

    if result:
        return(True, "Username already exists")
    else: 
        c.execute("INSERT INTO Users VALUES (?, ?)", (username, password))
        db.commit() 
        db.close() 
        return(False, "Welcome")


def login(username, password):
    DB_FILE="StoryCharger.db"
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create

    c = db.cursor()  
    
    c.execute("""SELECT Username FROM Users WHERE Username=? AND Password=?""",[username, password])
    result = c.fetchone()

    if result:
        ##access this specifc user data
        return(False)
        
    else: 
        return(True)

def new_story(title, story):
    DB_FILE = "StoryCharger.db"

    db = sqlite3.connect(DB_FILE)  # open if file exists, otherwise create
    c = db.cursor()
    dbseteup()

    c.execute("INSERT INTO Stories VALUES (?, ?, ?)", (title, story, story))

    db.commit()
    db.close()
   
