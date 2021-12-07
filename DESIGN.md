how you implemented your project and why you made the design decisions you did.

## Python
Our project used two python files: *app.py* and *database.py*. *app.py* contains all the functionality of the web app while *database.py* converts the movies.csv file into a sqlite database. The *app.py* file contains 3 different routes: "/", which is the landing page, "/loading" which is the loading page, and the ""

## HTML


## CSS


## SQLite3

    ### Converting CSV file to SQL database ###

    Our project asks the user to input a CSV file on the landing page. Once this CSV file is submitted, we use python to read this file as a dictionary and go through it line by line. As it goes through, we save the information in the form of a list of tuples so it can be passed as a SQL query. In order to continuously insert each tuple, we used the executemany function to insert the information into a table titled "letterboxd" in movies.db. This table includes movie title, year, and rating. 

    ### SQL queries to analyze films ###

    To analyze the user's movie taste, we derived a movie database from an outside source and saved it as a SQL table in movies.db, which is included in the project's ZIP file. This database was derived from themoviedb.org and saved in a table titled "movies." This table includes, movie title, genre, production company, release date, runtime, rating, cast, and crew. In order to analyze the movies found in the user's Letterboxd account, we used subqueries (nested SELECT statements) to use information from both the "movies" table and "letterboxd" table. 

    ### Clear letterboxd table ###

    To ensure that the Letterboxd table is cleared each time you input a new CSV file, we deleted each row through a SQL query which runs at the summary page, the last page of the site. This way, there will be a clear restart, and files won't combine when the analysis page is run. 