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
        # If file is valid
        if userratings.filename != '' and userratings.filename.endswith(".csv"):
            userratings.save(userratings.filename)

            # Convert uploaded csv file into sql database
            con = sqlite3.connect("movies.db")
            cur = con.cursor()

            with open(userratings.filename, 'r') as file:
                dr = csv.DictReader(file)
                to_db = [(i['Name'], i['Year'], i['Rating']) for i in dr]

            # Insert user ratings into letterboxd table
            cur.executemany("INSERT INTO letterboxd (title, year, rating) VALUES (?, ?, ?);", to_db)
            con.commit()
            con.close()
            return redirect("/loading")

        # If file invalid, return error message
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
    # Establish connection to movies databse
    con = sqlite3.connect("movies.db")
    cur = con.cursor()
    INSULTNUM = 20

    # Make list for messages and counter
    messages = ["" for a in range(INSULTNUM)]
    msgcount = 0

    # Call user pretencious for tarantino, anderson or nolan movies
    movielist_user = cur.execute("SELECT title FROM letterboxd WHERE title IN (SELECT title FROM movies WHERE (crew LIKE '%quentin tarantino%') OR (crew LIKE '%christopher nolan%') OR (crew LIKE '%wes anderson%'))")
    movielist_user = cur.fetchall()
    length = len(movielist_user)
    if length != 0:
        movie =  movielist_user[random.randint(0, length-1)][0]
        messages[msgcount] = "you probably think you’re so cool for watching " + movie
        msgcount += 1

    # Call user out on movie runtime
    movielist_time = cur.execute("SELECT title FROM letterboxd WHERE title IN (SELECT title FROM movies WHERE runtime > 150)")
    movielist_time = cur.fetchall()
    length = len(movielist_time)
    if length != 0:
        movie = movielist_time[random.randint(0, length-1)][0]
        messages[msgcount] = "you sat through the entirety of " + movie + "? good for u i guess..."
        msgcount += 1

    # Enjoyed bad movie?
    movielist_bad = cur.execute("SELECT title FROM letterboxd WHERE title IN (SELECT title FROM movies WHERE vote_average <= 6) AND rating >= 5")
    movielist_bad = cur.fetchall()
    length = len(movielist_bad)
    if length != 0:
        movie = movielist_bad[random.randint(0, length-1)][0]
        messages[msgcount] = "wait... you actually enjoyed " + movie + "?"
        msgcount += 1
    
    # # Musical stan
    # movielist_music = cur.execute("SELECT title FROM letterboxd WHERE title IN (SELECT title FROM movies WHERE genres LIKE '%Music%')")
    # movielist_music = cur.fetchall()
    # length = len(movielist_music)
    # if length != 0:
    #     movie = movielist_music[random.randint(0, length-1)][0]
    #     messages[msgcount] = "ah yes... " + movie + ". you must've been a theater kid"
    #     msgcount += 1
    

    # Delete rows from letterboxd table
    allmovies = cur.execute("SELECT title FROM letterboxd")
    allmovies = cur.fetchall()
    cur.executemany("DELETE FROM letterboxd WHERE title IN (?)", allmovies)
    cur.close()

    return render_template("result.html", messages=messages, len=INSULTNUM)