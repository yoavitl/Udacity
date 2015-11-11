Movie Trailer Website v1.0.2
----------------------------

This python program generates a Webpage that contains movie Tile
with six movies. Hoovering over a movie should display the movie story line.
Cliking on a movie would open a window that shows the movie trailer.

The repository conatins.
------------------------

1 - media.py
    This python file conatins the class defintion for the movie information
    and also the show trailer function.

2 - fresh_tomatoes.py
    This python file gets the information about the movies and generates
    the web page with the movie tiles according to the information it's
    recieving from the movielist.py

3 - movielist.py
    This python file contains the information of each movie, built in a class
    formation. Then this file calls the fresh_tomatoes module and generates
    the web page.

How to run the application.
---------------------------

You need to have python 2.7 installed on the computer.

1 - Open the terminal in the folder where the files are located.
2 - Run "$ python movielist.py"

This will generate a web page that contains six movie tiles with their
information. clicking on a desiered movie will open it's trailer.

Copyright:  Yoavi
Auther:     Yoav T. Levi
Date:       11.11.15
