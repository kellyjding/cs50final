how you implemented your project and why you made the design decisions you did.

## Python
Our project used two python files: *app.py* and *database.py*. *app.py* contains all the functionality of the web app while *database.py* converts the movies.csv file into a sqlite database. The *app.py* file contains 3 different routes: "/", which produces the landing page, "/loading" which produces the loading page, and "/result" which produces the result and summary pages. 

In the "/" route, if the user accesses the route through POST, so just accessing the site, we return the landing html page, with no error message. If the user accesses through GET, meaning they have (hopefully) uploaded a file and pressed the submit button, we iterate through the csv file and insert into a letterboxd table in the sql database, and redirect to the loading page. 

The "/loading" route renders the loading.html page. 

The "result" route creates two lists and two counters, one for the messages to be displayed in the results and the other for messages in the summary page. The two lists are created to be empty, then we fill in the message if it applies to the user. When we display them, we don't display the empty list items.For each of our 23 pre-determined insults, we use a sql query to get the corresponding list of movies, and write a corresponding message and summary message if applicable. Then, if the route is reached through GET, meaning the user was redirected to the page, we render the result.html page with the messages generated. If the route is reached through POST, meaning the user has clicked the "get summary" button, it renders the summary.html page with the summary messages generated.

## HTML


## CSS


## SQLite3

    ### Converting CSV file to SQL database ###

    Our project asks the user to input a CSV file on the landing page. Once this CSV file is submitted, we use python to read this file as a dictionary and go through it line by line. As it goes through, we save the information in the form of a list of tuples so it can be passed as a SQL query. In order to continuously insert each tuple, we used the executemany function to insert the information into a table titled "letterboxd" in movies.db. This table includes movie title, year, and rating. 

    ### SQL queries to analyze films ###

    To analyze the user's movie taste, we derived a movie database from an outside source and saved it as a SQL table in movies.db, which is included in the project's ZIP file. This database was derived from themoviedb.org and saved in a table titled "movies." This table includes, movie title, genre, production company, release date, runtime, rating, cast, and crew. In order to analyze the movies found in the user's Letterboxd account, we used subqueries (nested SELECT statements) to use information from both the "movies" table and "letterboxd" table. 

    ### Clear letterboxd table ###

    To ensure that the Letterboxd table is cleared each time you input a new CSV file, we deleted each row through a SQL query which runs at the summary page, the last page of the site. This way, there will be a clear restart, and files won't combine when the analysis page is run. 