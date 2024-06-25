# Personal Music Collection
This project uses SQL and Python in order to put my personal music collection (physical media like CDs and vinyl) into a database. Once in the database, I am able
to query in order to find music based on certain features (media type, year of release, artist, etc.). I developed this project further, too, by writing an additional Python script
which prompts the user in order to interact with the database. The user can randomly generate a musical suggestion, or investigate the media they have based on certain features. Users are
also able to add music to the database via this program.

To more closely follow my workflow in this project:
- *music_collection_functions.ipynb* is a JupyterNotebooks file which explains my initial development of most SQL functions used in the project (ie, Table creation, querying, etc)
- *Myriahs_music.ipynb* is a JupyterNotebooks file which includes my initial usage of the functions I developed, with all of my own media
- *user_music.py* is a script which depends on user input to reccommend an album, search for albums, add albums, etc. *user_music.py* interacts with *functions.py*,
  which contains all of the functions I developed in the above JupyterNotebooks, as well as a few additional functions for re-factoring any redundant code.
  It also interacts with *my_music.py*, which is just a file that contains record of all of my physical media.

Happy exploring!
