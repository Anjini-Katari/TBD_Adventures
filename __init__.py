# TBD's Adventures: Samantha Hua, Anjini Katari, and Emerson Gelobter
# SoftDev
# P00 -- Blogs | Move Slowly and Fix Things
# 2022-11-10
# time spent: 1hrs
# Target ship date: {2022-11-15}

import os
from flask import Flask, render_template, request, session
import sqlite3

# Reading db

DB_FILE="users.db"

db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

# Initializing db
c.execute("DROP TABLE users")
c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT);")
db.commit() # unsure if this is the right place to put this. supposedly saves changes - according to prev hw


app = Flask(__name__)    #create Flask object

app.secret_key = os.urandom(32) #creates random secret key

@app.route("/", methods=['GET', 'POST'])
def disp_loginpage():
    msg = ""
    if request.method == 'POST':
        msg = "You have been successfully logged out"
        session.pop('username') # these are the fields within session that we want to remove
        session.pop('password')
    if 'username' in session:
        return render_template('user.html', user=session['username'])
    # a = c.execute("SELECT IIF(500<1000, 'YES', 'NO');")
    # print(list(a)[0][0]) # list() is needed to make the sqlite3 cursor object readable. the first [0] is to get the item out of the list. the second [0] is to get the item out of the tuple (?)
    return render_template( 'login.html', msg=msg)

@app.route("/newUser", methods=['GET','POST'])
def addNewUser():
    msg = ""
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form: # need to check the input to make sure it's valid
            c.execute("INSERT INTO users VALUES('{}', '{}')".format(request.form['username'],request.form['password'])) # adds user pass combo into the db
            db.commit()
            print(list(c.execute("SELECT * from users;"))) # if it doesn't work try db.commit()
            return render_template('login.html', msg="successfully created account")
        else:
            msg = "An error occurred. Try again."
    return render_template('signup.html', msg=msg)

@app.route("/login", methods =['GET', 'POST'])
def authenticate():
    msg = ""

    # session['username'] = "x" #hard coded username and password
    # session['password'] = "y"
    print(list(c.execute("SELECT * from users;")))
    # print(list(c.execute("SELECT password from users where username = 'a';"))) # [('b',)]
    pwd_check = c.execute("SELECT password from users where username = '{}'".format(request.form['username']))
    try:
        if list(pwd_check)[0][0] == request.form['password']:
            session['username']=request.form['username']
            session['password']=request.form['password']
            print(session)
            return render_template( 'user.html', user=session['username'])  # response to a form submission
        else:
            msg = "your password is incorrect"
    except:
        msg = "could not find username in our database"
    # if 'username' in request.form and 'password' in request.form: # error otherwise because request.form could be empty
    #
    #     if session['username'] == request.form['username']: # assumes username exists within session (it does rn because we hard code it)
    #         if session['password'] == request.form['password']:
    #             msg = "you're logged in"
    #             return render_template( 'user.html', user=session['username'])  # response to a form submission
    #         else:
    #             msg = "you're not logged in because your password was wrong"
    #             return render_template( 'login.html', msg=msg)
    #     else:
    #         if session['password'] == request.form['password']:
    #             msg = "you're not logged in because your username was wrong"
    #         else:
    #             msg = "you're not logged in because your username and password were wrong"
    #         return render_template( 'login.html', msg=msg)
    print("incorrect comparison")
    return render_template( 'login.html', msg=msg) # should not ever get to this point but just in case it does

@app.route("/home", methods =['GET', 'POST'])
def homepage():
    return "slay queen"

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
