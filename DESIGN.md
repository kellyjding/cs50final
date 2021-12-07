## Python
Our project used two python files: *app.py* and *database.py*. *app.py* contains all the functionality of the web app while *database.py* converts the movies.csv file into a sqlite database. The *app.py* file contains 3 different routes: "/", which produces the landing page, "/loading" which produces the loading page, and "/result" which produces the result and summary pages. 

In the "/" route, if the user accesses the route through POST, so just accessing the site, we return the landing html page, with no error message. If the user accesses through GET, meaning they have (hopefully) uploaded a file and pressed the submit button, we iterate through the csv file and insert into a letterboxd table in the sql database, and redirect to the loading page. The "/loading" route renders the loading.html page. The "result" route creates two lists and two counters, one for the messages to be displayed in the results and the other for messages in the summary page. The two lists are created to be empty, then we fill in the message if it applies to the user. When we display them, we don't display the empty list items.For each of our 23 pre-determined insults, we use a sql query to get the corresponding list of movies, and write a corresponding message and summary message if applicable. Then, if the route is reached through GET, meaning the user was redirected to the page, we render the result.html page with the messages generated. If the route is reached through POST, meaning the user has clicked the "get summary" button, it renders the summary.html page with the summary messages generated.

The *database.py* file takes the movies.csv file included in the folder, and imports the entries into the movies database.

## HTML
In our templates folder, there are five html pages. *layout.html* is the basic page that the other four pages build off of. The page implements bootstrap, the navbar with the logo and page name, and the footer with our names. It also includes jinja for block title and block main for the other pages to add content. 

*landing.html* includes a header and get started button that redirects the user to the instructions portion of the page. The instructions are listed and a form for the user to upload their file, and a submit button. Then we also have an about section about us two creators. 

*loading.html* has a loading animation with a little caption.

*result.html* lists the messages (as long as they're not empty) and has a button for the user to access the summary page.

*summary.html* lists the summary messages, a thank you, and some sharing features for users to share the site (it currently shares a non-existent website urmovietastesux.com)


## CSS
Our css file contains styling for our elements. We have a color palette that we primarily used in choosing text and element colors. We also primarily used two fonts, fira sans and source code pro for consistency and a retro look.

## SQLite3

