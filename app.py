import os
import re
import time
import csv
import random
import sqlite3
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def landing():
    # POST
    if request.method == "POST":
        userratings = request.files['ratings']
        # if file is okay
        if userratings.filename != '' and userratings.filename.endswith(".csv"):
            userratings.save(userratings.filename)

            # convert uploaded csv file into sql database
            con = sqlite3.connect("letterboxd.db")
            cur = con.cursor()

            with open(userratings.filename, 'r') as file:
                dr = csv.DictReader(file)
                to_db = [(i['Name'], i['Year'], i['Rating']) for i in dr]

            # create table?
            cur.executemany("INSERT INTO letterboxd (name, year, rating) VALUES (?, ?, ?);", to_db)
            con.commit()
            con.close()
            return redirect("/loading")

        # return error message
        else:
            return render_template("landing.html", error="invalid file")

    # GET
    else:
        return render_template("landing.html", error="")

@app.route("/loading", methods=["GET"])
def loading():
    return render_template("loading.html")

@app.route("/result", methods=["GET"])
def result():
    con = sqlite3.connect("letterboxd.db")
    cur = con.cursor()
    con1 = sqlite3.connect("movies.db")
    cur1 = con1.cursor()
    INSULTNUM = 20
    messages = ["" for a in range(INSULTNUM)]
    msgcount = 0

    movielist_dir = cur1.execute("SELECT title FROM movies WHERE (crew LIKE '%quentin tarantino%') OR (crew LIKE '%christopher nolan%') OR (crew LIKE '%wes anderson%')")
    movielist_dir = cur1.fetchall()
    movielist_user = cur.executemany("SELECT name FROM letterboxd WHERE name IN (?)", movielist_dir)
    movielist_user = cur.fetchall()
    print(movielist_user)
    length = len(movielist_user)
    if length != 0:
        messages[msgcount] = "you probably think you’re so cool for watching %s" , movielist_user[random.randint(0, length)]['name']
        msgcount += 1

    allmovies = cur.execute("SELECT name FROM letterboxd")
    allmovies = cur.fetchall()
    cur.executemany("DELETE FROM letterboxd WHERE name IN (?)", allmovies)
    cur.close()
    cur.close()
    return render_template("result.html", messages=messages, len=INSULTNUM)