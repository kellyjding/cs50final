how you implemented your project and why you made the design decisions you did.

## Python
Our project used two python files: *app.py* and *database.py*. *app.py* contains all the functionality of the web app while *database.py* converts the movies.csv file into a sqlite database. The *app.py* file contains 3 different routes: "/", which produces the landing page, "/loading" which produces the loading page, and "/result" which produces the result and summary pages. 

In the "/" route, if the user accesses the route through POST, so just accessing the site, we return the landing html page, with no error message. If the user accesses through GET, meaning they have (hopefully) uploaded a file and pressed the submit button, we iterate through the csv file and insert into a letterboxd table in the sql database, and redirect to the loading page. 

The "/loading" route renders the loading.html page. 

The "result" route creates two lists and two counters, one for the messages to be displayed in the results and the other for messages in the summary page. The two lists are created to be empty, then we fill in the message if it applies to the user. When we display them, we don't display the empty list items.For each of our 23 pre-determined insults, we use a sql query to get the corresponding list of movies, and write a corresponding message and summary message if applicable. Then, if the route is reached through GET, meaning the user was redirected to the page, we render the result.html page with the messages generated. If the route is reached through POST, meaning the user has clicked the "get summary" button, it renders the summary.html page with the summary messages generated.

## HTML


## CSS


## SQLite3

