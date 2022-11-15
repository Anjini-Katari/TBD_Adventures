# TBD's Adventures: Samantha Hua, Anjini Katari, and Emerson Gelobter
# SoftDev
# P00 -- Blogs | Move Slowly and Fix Things
# 2022-11-10
# time spent: 1hrs
# Target ship date: {2022-11-15}

import os
from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3

# Reading db

DB_FILE="site.db"

db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
c = db.cursor() #facilitate db ops -- you will use cursor to trigger db events

# Initializing db
c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT);") #username/password db
c.execute("CREATE TABLE IF NOT EXISTS blogs(username TEXT, blogName TEXT, entry TEXT);") #blog db with entry
db.commit() # saves changes 

app = Flask(__name__)    #create Flask object

app.secret_key = os.urandom(32) #creates random secret key


@app.route("/newUser", methods=['GET','POST'])
def addNewUser():
    msg = ""
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form: # need to check the input to make sure it's valid
            passing = [request.form['username'], request.form['password']]
            c.execute("INSERT INTO users VALUES (?, ?)", passing) # adds user pass combo into the db
            db.commit()
            return render_template('login.html', msg="successfully created account")
        else:
            msg = "An error occurred. Try again."
    return render_template('signup.html', msg=msg)

@app.route("/login", methods =['GET', 'POST'])
def authenticate():
    msg = ""

    passing = [request.form['username']]
    pwd_check = c.execute("SELECT password from users where username = ?", passing)
    try:
        if list(pwd_check)[0][0] == request.form['password']:
            session['username']=request.form['username']
            session['password']=request.form['password']
            userBlogs = list(c.execute("SELECT * from blogs WHERE username = (?)", passing))
            # return redirect(url_for('userpage'))
            return render_template('user.html', user=session['username'], blogList=userBlogs)  # response to a form submission
        else:
            msg = "your password is incorrect"
    except:
        msg = "could not find username in our database"

    return render_template( 'login.html', msg=msg)

@app.route("/", methods=['GET', 'POST'])
def disp_loginpage():
    
    return render_template( 'login.html')

@app.route("/logout", methods=['GET', 'POST'])
def disp_logoutpage():
    msg = ""
    
    if request.method == 'POST':
<<<<<<< HEAD
        if 'username' in session:
            msg = "You have been successfully logged out"
            session.pop('username') # these are the fields within session that we want to remove
            session.pop('password')
        return render_template('login.html', msg=msg)
    return render_template( 'login.html', msg=msg)
=======
        if 'newBlog' in request.form and 'blogName' in request.form:
            passing = [request.form['newBlog'], request.form['blogName']]
            c.execute("INSERT INTO blogs VALUES (?, ?)", passing) # adds user pass combo into the db
            db.commit()
            return render_template("user.html", msg = "blog has been successfully created")
>>>>>>> 27db13710a7abf24bed7747a39659d07163cc3a6

@app.route("/user", methods =['GET', 'POST'])
def userpage():
    try:
        passing = [session['username']]
    except:
        return render_template('login.html', msg="Forbidden access. Log in first")
    userBlogs = list(c.execute("SELECT * from blogs WHERE username = (?)", passing))
    if request.method == 'POST': 
        if 'newEntry' in request.form and 'blogName' in request.form:
            passing = [session['username'], request.form['blogName']]
            try:
                oldEntry = list(c.execute("SELECT entry FROM blogs WHERE username = (?) AND blogName = (?)", passing))[0][0]
                print(oldEntry)
                print("blog alr exists")
                passing = [(oldEntry + " " + request.form['newEntry']), request.form['blogName'], session['username']]
                c.execute("UPDATE blogs SET entry=(?) WHERE blogName=(?) AND username=(?)", passing)
                db.commit()
            except:
                passing = [session['username'], request.form['blogName'], request.form['newEntry']]
                c.execute("INSERT INTO blogs VALUES (?, ?, ?)", passing)
                db.commit()
            return render_template("user.html", user=session['username'], blogList=userBlogs, msg = "blog has been successfully created " + str(session['username']))
        return render_template("user.html", user=session['username'], blogList=userBlogs, msg="You did not submit a complete blog entry")
    return render_template("user.html", user=session['username'], blogList=userBlogs, msg = "blog has been successfully created")

@app.route("/home", methods = ['GET','POST'])
def disp_home():
    msg=""
    try:
        blogList = c.execute("SELECT * from blogs;")
    except:
        msg = "There are currently no blogs in our system :("
    return render_template("home.html", blogList=blogList, msg=msg)

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()