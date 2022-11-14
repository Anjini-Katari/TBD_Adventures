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
c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT)")
db.commit()



app = Flask(__name__)    #create Flask object

app.secret_key = os.urandom(32) #creates random secret key

@app.route("/", methods=['GET', 'POST'])
def disp_loginpage():
    msg = ""
    if request.method == 'POST':
        msg = "You have been successfully logged out"
    return render_template( 'login.html', msg=msg)

@app.route("/newUser", methods=['GET','POST'])
def addNewUser():
    msg = "An error occurred. Try again."
    if request.method == 'POST':
#        if 'username' in request.form and 'password' in request.form:
            # need to check the input to make sure it's valid
            c.execute("INSERT INTO users VALUES('{}', '{}')".format(request.form['username'],request.form['password'])) # adds user pass combo into the db
            #            c.execute("INSERT INTO user VALUES('{}', '{}')".format(i['username'], i['password'])) # adds user pass combo into the db
            db.commit() #saves the inputs to the db
            print(c.execute("SELECT * from users"))
    return render_template('login.html', msg=msg)

@app.route("/signUp", methods=['GET','POST'])
def signUp():
    
    return render_template('signup.html')

# going to the sign up page to collect the new username and password is a different step from going to the login page after 
# the values have been submitted which is why we need two app routes 

@app.route("/login", methods =['GET', 'POST'])
def authenticate():
    msg = ""

    pwd_check = c.execute("SELECT password from users where username = '{}'".format(request.form['username']))
    if pwd_check == request.form['password']:
        session['username']=request.form['username']
        session['password']=request.form['password']
    else:
        session['username']='None'
        session['password']='None'

    # if 'username' in request.form: # error otherwise because request.form could be empty

    #     if session['username'] == request.form['username']: # assumes username exists within session (it does rn because we hard code it)
    #         if session['password'] == request.form['password']:
    #             msg = "you're logged in"
    #             return render_template( 'user.html', user=(request.form['username']))  # response to a form submission
    #         else:
    #             msg = "you're not logged in because your password was wrong"
    #             return render_template( 'login.html', msg=msg)
    #     else:
    #         if session['password'] == request.form['password']:
    #             msg = "you're not logged in because your username was wrong"
    #         else:
    #             msg = "you're not logged in because your username and password were wrong"
    #         return render_template( 'login.html', msg=msg)

    return render_template( 'home.html', msg="", user=session['username']) 



if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
