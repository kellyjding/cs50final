import csv
import sqlite3

 # convert uploaded csv file into sql database
con = sqlite3.connect("movies.db")
cur = con.cursor()

with open('movies.csv', newline='') as file:
    dr = csv.DictReader(file)
    to_db = [(i['title'], i['genres'], i['production_companies'],i['release_date'], i['runtime'], i['vote_average'], i['cast'], i['crew']) for i in dr]

cur.executemany("INSERT INTO movies (title, genres, production_companies, release_date, runtime, vote_average, cast, crew) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_db)
con.commit()
con.close()