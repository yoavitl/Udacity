Item Catalog website Project v1.0
---------------------------

This web application goal is to create the English Premier League Database.
this web application demonstrate the use of CRUD in web development, the league
is the catalog, each team is a category and each player is item in the catalog.
In this application you can view wall the league teams, and for each team you
can see its players. If you are not logged in you have view only permissions.
You can log in into the application and then you can create new players for each
team, if you created a player you can edit him or delete him if necessary, but
you can't edit or delete a player you didn't created.
The application have XML and JSON endpoints.

The repository contains.
------------------------

1 - league.py
    This is the main file, it is the web application. this file contains all the
    functions that responsible to the web site functioning.

2 - database_setup.py
    This python file will create the necessary database creation module.

3 - AllTeams.py & Allplayers.py
    This file populates the DB with the teams and players for each team in the
    English Premier league

4 - client_secrets.JSON
    This file allows the web app to communicate with google, allowing users to
    login to the site using google authentication.

5- Templates folder
   This folder contains all the html pages availble in the application, written
   is a format that allawos the app to render the pages with content

6 - static\ style.css
    This is the style formatter for the website.

7 - Puppies folder
    This folder was created as an extra assignment in the full stack course



How to run the application.
---------------------------

You need to have python 2.7 installed on the computer.
and flask python module installed.
You Need a computer with sqlite3 installed,
a web browser and google account.

1 - open the terminal and run this command -
    $ python database_setup.py

2 - Fill the database using the AllTeams and Allplayers scripts-
    $ python Allteams.py
    $ python Allplayers.py

3 - run the main module -
    $ python leauge.py

4 - Open a Browser and enter this address-
    http://localhost:5000/

5 - the application is up and running, you can now view the teams, login and
    create additional players in the team.

Date:       
Copyright:  Yoavi
Auther:     Yoav T. Levi
