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

@app.route("/result", methods=["GET", "POST"])
def result():
    # Establish connection to movies databse
    con = sqlite3.connect("movies.db")
    cur = con.cursor()
    INSULTNUM = 23
    SUMMARYNUM = 15

    # Make list for messages and counter
    messages = ["" for a in range(INSULTNUM)]
    msgcount = 0

    # Make summary message
    summary = ["" for b in range(SUMMARYNUM)]
    summarycount = 0

    if request.method == "GET":
        
        # Call user pretentious for tarantino or anderson movies
        movielist_user = cur.execute("SELECT title FROM letterboxd WHERE title IN (SELECT title FROM movies WHERE (crew LIKE '%quentin tarantino%') OR (crew LIKE '%wes anderson%'))")
        movielist_user = cur.fetchall()
        length = len(movielist_user)
        if length != 0:
            movie =  movielist_user[random.randint(0, length-1)][0]
            messages[msgcount] = "you probably think you’re so cool for watching " + movie + "."
            msgcount += 1
            summary[summarycount] = "extremely pretentious"
            summarycount += 1

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
            summary[summarycount] = "taste is stinky"
            summarycount += 1
        
        # Musical stan
        movielist_music = cur.execute("SELECT title FROM letterboxd WHERE title IN (SELECT title FROM movies WHERE genres LIKE '%Music%')")
        movielist_music = cur.fetchall()
        length = len(movielist_music)
        if length != 0:
            movie = movielist_music[random.randint(0, length-1)][0]
            messages[msgcount] = movie + "... you must've been a theater kid."
            msgcount += 1
            summary[summarycount] = "probably singing broadway tunes in the shower"
            summarycount += 1
        
        # Romance stan
        movielist_romance = cur.execute("SELECT title FROM letterboxd WHERE title IN (SELECT title FROM movies WHERE genres LIKE '%Romance%')")
        movielist_romance = cur.fetchall()
        length = len(movielist_romance)
        if length != 0:
            movie = movielist_romance[random.randint(0, length-1)][0]
            messages[msgcount] = movie + "? looks like you reallyyyy like romance movies... do you need a hug?"
            msgcount += 1
            summary[summarycount] = "still in love with your ex"
            summarycount += 1

        # Western stan
        movielist_western = cur.execute("SELECT title FROM letterboxd WHERE title IN (SELECT title FROM movies WHERE genres LIKE '%Western%')")
        movielist_western = cur.fetchall()
        length = len(movielist_western)
        if length != 0:
            movie = movielist_western[random.randint(0, length-1)][0]
            messages[msgcount] = "you watched " + movie + "? who are you? who watches westerns anymore??"
            msgcount += 1
            summary[summarycount] = "non existent (like seriously no one watches westerns)"
            summarycount += 1

        # War stan
        movielist_war = cur.execute("SELECT title FROM letterboxd WHERE title IN (SELECT title FROM movies WHERE genres LIKE '%War%')")
        movielist_war = cur.fetchall()
        length = len(movielist_war)
        if length != 0:
            movie = movielist_war[random.randint(0, length-1)][0]
            messages[msgcount] = "why did you watch " + movie + "? are you my dad?"
            msgcount += 1
            summary[summarycount] = "kelly ding's dad who specifically likes war movies"
            summarycount += 1

        # Marvel stan
        movielist_marvel = cur.execute("SELECT COUNT(title) FROM letterboxd WHERE title IN (SELECT title FROM movies WHERE production_companies LIKE '%Marvel%')")
        movielist_marvel = cur.fetchall()
        if movielist_marvel[0][0] != 0:
            messages[msgcount] = "you watched " + str(movielist_marvel[0][0]) +" marvel movies. i bet you think marvel is the pinnacle of cinema."
            msgcount += 1

        # DC stan
        movielist_dc = cur.execute("SELECT title FROM letterboxd WHERE title IN (SELECT title FROM movies WHERE production_companies LIKE '%DC Comics%')")
        movielist_dc = cur.fetchall()
        length = len(movielist_dc)
        if length != 0:
            movie = movielist_dc[random.randint(0, length-1)][0]
            messages[msgcount] = "you enjoyed " + movie +"? u wouldn’t know good cinema even if it slapped u in the face. - a marvel fan"
            msgcount += 1
            summary[summarycount] = "wrong. about superhero movies that is."
            summarycount += 1


        # Jesse Eisenberg stan
        movielist_jesse = cur.execute("SELECT title FROM letterboxd WHERE title IN (SELECT title FROM movies WHERE movies.cast LIKE '%Jesse Eisenberg%')")
        movielist_jesse = cur.fetchall()
        length = len(movielist_jesse)
        if length != 0:
            movie = movielist_jesse[random.randint(0, length-1)][0]
            messages[msgcount] = movie + " starring jesse eisenberg??? were u able to understand the dialogue, dummy?"
            msgcount += 1
            summary[summarycount] = "a mark zuckerberg apologist"
            summarycount += 1

        # Jake Gyllenhaal stan
        movielist_jake = cur.execute("SELECT title FROM letterboxd WHERE title IN (SELECT title FROM movies WHERE movies.cast LIKE '%Jake Gyllenhaal%')")
        movielist_jake = cur.fetchall()
        length = len(movielist_jake)
        if length != 0:
            movie = movielist_jake[random.randint(0, length-1)][0]
            messages[msgcount] = "oh my god you know that jake gyllenhaal is in " + movie + " right??? if u care about taylor swift you can no longer support this movie." 
            msgcount += 1
            summary[summarycount] = "a jake gyllenhaal supporter"
            summarycount += 1

        # The Rock stan
        movielist_rock = cur.execute("SELECT title FROM letterboxd WHERE title IN (SELECT title FROM movies WHERE movies.cast LIKE '%Dwayne Johnson%')")
        movielist_rock = cur.fetchall()
        length = len(movielist_rock)
        if length != 0:
            movie = movielist_rock[random.randint(0, length-1)][0]
            messages[msgcount] = movie + " starring dwayne the rock johnson??? ITS ABOUT DRIVE IT’S ABOUT POWER WE STAY HUNGRY WE DEVOUR PUT INT THEWORKDPUTINRHTHOURD DIT"
            msgcount += 1
            summary[summarycount] = "dwayne the rock johnson"
            summarycount += 1
        
        # Red flags
        movielist_red = cur.execute("SELECT title FROM letterboxd WHERE title IN (SELECT title FROM movies WHERE (title LIKE '%Fight Club%') OR (title LIKE '%Inception%') OR (title LIKE '%Wolf of Wall Street%') OR (title LIKE '%Godfather%') OR (title LIKE '%Pulp Fiction%') OR (title LIKE '%Inception%') OR (title LIKE '%Wolf of Wall Street%') OR (title LIKE '%Godfather%') OR (title LIKE '%Inglorious Bastards%'))")
        movielist_red = cur.fetchall()
        length = len(movielist_red)
        if length != 0:
            movie = movielist_red[random.randint(0, length-1)][0]
            messages[msgcount] = movie + " ??? red flag red flag red flag red flag"
            msgcount += 1
            summary[summarycount] = "a male-manipulating film bro"
            summarycount += 1

        # Horror stan
        movielist_horror = cur.execute("SELECT title FROM letterboxd WHERE title IN (SELECT title FROM movies WHERE genres LIKE '%Horror%')")
        movielist_horror = cur.fetchall()
        length = len(movielist_horror)
        if length != 0:
            movie = movielist_horror[random.randint(0, length-1)][0]
            messages[msgcount] = movie + " definitely made you piss your pants."
            msgcount += 1
            summary[summarycount] = "a scared baby"
            summarycount += 1

        # Star wars stan
        movielist_starwars = cur.execute("SELECT title FROM letterboxd WHERE title IN (SELECT title FROM movies WHERE production_companies LIKE '%Lucasfilm%')")
        movielist_starwars = cur.fetchall()
        length = len(movielist_starwars)
        if length != 0:
            movie = movielist_starwars[random.randint(0, length-1)][0]
            messages[msgcount] = movie + "? you're a star wars fan? hope you didn't actually enjoy the prequels..."
            msgcount += 1
            summary[summarycount] = "a total nerd"
            summarycount += 1
        
        # Disney stan
        movielist_disney = cur.execute("SELECT title FROM letterboxd WHERE title IN (SELECT title FROM movies WHERE production_companies LIKE '%Disney%')")
        movielist_disney = cur.fetchall()
        length = len(movielist_disney)
        if length != 0:
            movie = movielist_disney[random.randint(0, length-1)][0]
            messages[msgcount] = movie + "? are you... an infant? a little baby maybe? a tiny little child?"
            msgcount += 1
            summary[summarycount] = "a literal baby"
            summarycount += 1

        # Tim Burton stan
        movielist_tim = cur.execute("SELECT title FROM letterboxd WHERE title IN (SELECT title FROM movies WHERE production_companies LIKE '%Tim Burton Productions%')")
        movielist_tim = cur.fetchall()
        length = len(movielist_tim)
        if length != 0:
            movie = movielist_tim[random.randint(0, length-1)][0]
            messages[msgcount] = movie + "? you def went through an emo phase in middle school… #tøpforever #mcr #patd!"
            msgcount += 1
            summary[summarycount] = "a quirky tim burton emo phase middle schooler"
            summarycount += 1

        # Attention span baby
        movielist_time = cur.execute("SELECT title FROM letterboxd WHERE title IN (SELECT title FROM movies WHERE runtime < 90)")
        movielist_time = cur.fetchall()
        length = len(movielist_time)
        if length != 0:
            movie = movielist_time[random.randint(0, length-1)][0]
            messages[msgcount] = movie + " is literally so short, does it even count as a movie... do you have the attention span of an ipad kid?"
            msgcount += 1

        # Weird movies
        movielist_weird = cur.execute("SELECT title FROM letterboxd WHERE title IN (SELECT title FROM movies WHERE (crew LIKE '%stanley kubrick%') OR (crew LIKE '%guillermo del toro%') OR (crew LIKE '%robert eggers%') OR (crew LIKE '%ari aster%'))")
        movielist_weird = cur.fetchall()
        length = len(movielist_weird)
        if length != 0:
            movie =  movielist_weird[random.randint(0, length-1)][0]
            messages[msgcount] = movie + "... such a weird movie.... i mean, it makes sense why YOU watched it... weirdo..."
            msgcount += 1

        # Danny Devito
        movielist_danny = cur.execute("SELECT title FROM letterboxd WHERE title IN (SELECT title FROM movies WHERE movies.cast LIKE '%danny devito%')")
        movielist_danny = cur.fetchall()
        length = len(movielist_danny)
        if length != 0:
            movie =  movielist_danny[random.randint(0, length-1)][0]
            messages[msgcount] = "did u watch " + movie + " or were you just staring at danny devito the whole time?"
            msgcount += 1

        # Adam Sandler
        movielist_adam = cur.execute("SELECT title FROM letterboxd WHERE title IN (SELECT title FROM movies WHERE movies.cast LIKE '%adam sandler%')")
        movielist_adam = cur.fetchall()
        length = len(movielist_adam)
        if length != 0:
            movie =  movielist_adam[random.randint(0, length-1)][0]
            messages[msgcount] = movie + " was such a good movie. fun fact: co-creator rave andrews has the same bday as adam sandler"
            msgcount += 1
        
        # Dreamworks - shrek
        movielist_dreamworks = cur.execute("SELECT title FROM letterboxd WHERE title IN (SELECT title FROM movies WHERE production_companies LIKE '%Dreamworks%') AND title NOT IN (SELECT title FROM movies WHERE title LIKE '%Shrek%')")
        movielist_dreamworks = cur.fetchall()
        length = len(movielist_dreamworks)
        if length != 0:
            movie =  movielist_dreamworks[random.randint(0, length-1)][0]
            messages[msgcount] = "ahh i see you watched " + movie + "... you know shrek is the only good dreamworks movie, right?"
            msgcount += 1

        # A24
        movielist_a24 = cur.execute("SELECT title FROM letterboxd WHERE title IN (SELECT title FROM movies WHERE production_companies LIKE '%A24%')")
        movielist_a24 = cur.fetchall()
        length = len(movielist_a24)
        if length != 0:
            movie = movielist_a24[random.randint(0, length-1)][0]
            messages[msgcount] = "you liked " + movie + "? ugh another a24-obsessed-tote-bag-carrying film lover?"
            msgcount += 1

        return render_template("result.html", messages=messages, len=INSULTNUM)

    else: 
        # Delete rows from letterboxd table and clear lists
        cur.execute("DELETE FROM letterboxd")
        con.commit()
        con.close()
        return render_template("summary.html", summary=summary, len2=SUMMARYNUM)