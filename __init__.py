# TBD's Adventures: Samantha Hua, Anjini Katari, and Emerson Gelobter
# SoftDev
# P00 -- Blogs | Move Slowly and Fix Things
# 2022-11-10
# time spent: 1hrs
# Target ship date: {2022-11-15}

import os
from flask import Flask             #facilitate flask webserving
from flask import render_template   #facilitate jinja templating
from flask import request           #facilitate form submission
from flask import session


#the conventional way:
#from flask import Flask, render_template, request

app = Flask(__name__)    #create Flask object

app.secret_key = os.urandom(32)

@app.route("/", methods=['GET', 'POST'])
def disp_loginpage():
    msg = ""
    if request.method == 'POST':
        msg = "You have been successfully logged out"
    return render_template( 'login.html', msg=msg)

@app.route("/newUser", methods=['GET','POST'])
def addNewUser():
    # if request.method == 'POST':
    #     if !(request.form['username'] in session):
    #
    msg = "working on it"
    return render_template('login.html', msg=msg)

@app.route("/auth", methods =['GET', 'POST'])
def authenticate():
    msg = ""

    session['username'] = "x" #hard coded username and password
    session['password'] = "y"

    if 'username' in request.form: # error otherwise because request.form could be empty
        if session['username'] == request.form['username']: # assumes username exists within session (it does rn because we hard code it)
            if session['password'] == request.form['password']:
                msg = "you're logged in"
                return render_template( 'user.html', user=(request.form['username']))  # response to a form submission
            else:
                msg = "you're not logged in because your password was wrong"
                return render_template( 'login.html', msg=msg)
        else:
            if session['password'] == request.form['password']:
                msg = "you're not logged in because your username was wrong"
            else:
                msg = "you're not logged in because your username and password were wrong"
            return render_template( 'login.html', msg=msg)

    return render_template( 'login.html', msg="Sorry, an error occured. Try again.") # should not ever get to this point but just in case it does



if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
