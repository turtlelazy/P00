'''
Forgotten Charger: Lewis Cass, Aryaman Goenka, Oscar Wang
Softdev
P00: Cookie and Sessions Introduction
2021-10-29
time spent: 0.5
'''

import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O

DB_FILE="StoryCharger.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

#==========================================================

# < < < INSERT YOUR TEAM'S POPULATE-THE-DB CODE HERE > > >

c.execute("Drop Table if exists Users")
command = "Create Table Users (Username Text, Password Integer, UserID Primary Key)"    
c.execute(command)      # test SQL stmt in sqlite3 shell, save as string
# run SQL statement

c.execute("Drop Table if exists Stories")
command = "Create Table Stories (Title Text, FullStory Text, Latest_Update Text, StoryID Primary Key)"    
c.execute(command)      # test SQL stmt in sqlite3 shell, save as string
# run SQL statement

c.execute("Drop Table if exists Contributions")
command = "Create Table Contributions (UserID Integer, StoryID Integer, id Primary Key)"    
c.execute(command)      # test SQL stmt in sqlite3 shell, save as string
# run SQL statement

#==========================================================

db.commit() #save changes
db.close()  #close database