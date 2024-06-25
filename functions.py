"""Functions used in Personal Music Collection project,
Myriah Hodgson, 06/22/2024"""

# Import SQL
import sqlite3

# Connect to the database
conn = sqlite3.connect('music_collection.db')
cursor = conn.cursor()


""" // TABLE CREATION FUNCTION // """

def create_tables():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Artists (
               id INTEGER PRIMARY KEY,
               name TEXT UNIQUE NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Albums (
               id INTEGER PRIMARY KEY,
               title TEXT UNIQUE NOT NULL,
               artist_id INTEGER NOT NULL,
               year INTEGER,
               FOREIGN KEY (artist_id) REFERENCES Artists(id),
               UNIQUE (title, artist_id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Formats (
               id INTEGER PRIMARY KEY,
               format_name TEXT UNIQUE NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS FormattedAlbums (
               album_id INTEGER NOT NULL,
               format_id INTEGER NOT NULL,
               FOREIGN KEY (album_id) REFERENCES Albums(id),
               FOREIGN KEY (format_id) REFERENCES Formats(id),
               PRIMARY KEY (album_id, format_id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Genres (
               id INTEGER PRIMARY KEY,
               genre_name TEXT UNIQUE NOT NULL
        )""")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS AlbumGenres (
               album_id INTEGER,
               genre_id INTEGER,
               PRIMARY KEY (album_id, genre_id)
               FOREIGN KEY (album_id) REFERENCES Albums(id),
               FOREIGN KEY (genre_id) REFERENCES Genres(id)

        )""")
    return



""" // INSERTION & ID FINDING FUNCTIONS // """

def insert_artist(name):
    """This function inserts a new artist into our Artists table."""
    cursor.execute("""INSERT OR IGNORE INTO Artists (name) VALUES (?)""", (name,))
    conn.commit()
    return cursor.lastrowid

def find_artist_id(name):
    """This function finds the id associated with an artist."""
    cursor.execute("""SELECT id FROM Artists WHERE name = ?""", (name,))
    result = cursor.fetchone()
    if result:
        return result[0]
    return None

def insert_album(title, artist_name, year):
    """This function inserts an album into our Albums table if it doesn't already exist."""
    artist_id = find_artist_id(artist_name)
    if not artist_id:
        artist_id = insert_artist(artist_name) # if for some reason the artist is not in our Artists table, add it.
    
    # Check if the album already exists
    cursor.execute("""SELECT id FROM Albums WHERE title = ? AND artist_id = ?""", (title, artist_id))
    result = cursor.fetchone()
    if result:
        print(f"Album '{title}' by '{artist_name}' already exists in the database.")
        return result[0]
    else:
        cursor.execute("""INSERT INTO Albums (title, artist_id, year) VALUES (?, ?, ?)""", (title, artist_id, year))
        conn.commit()
        return cursor.lastrowid

def find_album_id(title):
    """This function finds the id associated with an album."""
    cursor.execute("""SELECT id FROM Albums WHERE title = ?""", (title,))
    result = cursor.fetchone()
    if result:
        return result[0]
    return None

def load_format(format):
    """Insert any new possible format types of our media."""
    cursor.execute("""INSERT INTO Formats (format_name) VALUES (?)""", (format,))
    conn.commit()
    return cursor.lastrowid

def find_format_id(format):
    """We also need the id associated with each format type."""
    cursor.execute("""SELECT id from Formats WHERE format_name = ?""", (format,))
    format_id = cursor.fetchone()[0]
    return format_id

def insert_formatted_album(album_title, format_title):
    """Finally, we will use the above functions in order to insert an album also with its media type."""
    album_id = find_album_id(album_title)
    format_id = find_format_id(format_title)
    cursor.execute("""INSERT OR IGNORE INTO FormattedAlbums (album_id, format_id) VALUES (?, ?)""", (album_id, format_id))
    conn.commit()
    return cursor.lastrowid

def insert_genre(genre_name):
    """Insert a new genre into Genres table, if it doesn't already exist."""
    cursor.execute("""INSERT OR IGNORE INTO Genres (genre_name) VALUES (?)""", (genre_name,))
    conn.commit()
    return cursor.lastrowid

def find_genre_id(genre_name):
    """Retrieve the id of a genre by its name."""
    cursor.execute("""SELECT id FROM Genres WHERE genre_name = ?""", (genre_name,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None
    


""" // BASIC QUERYING FUNCTIONS // """

def query_artists():
    """Query all artists."""
    cursor.execute("SELECT * FROM Artists")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def query_albums():
    """Query all albums."""
    cursor.execute("SELECT * FROM Albums")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def query_formats():
    """Query all formats."""
    cursor.execute("SELECT * FROM Formats")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def query_genres():
    """Query all genres."""
    cursor.execute("SELECT * FROM Genres")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def query_formatted_albums():
    """Query all formatted albums."""
    cursor.execute("""
    SELECT Albums.title, Artists.name, Albums.year, Formats.format_name
    FROM FormattedAlbums
    JOIN Albums ON FormattedAlbums.album_id = Albums.id
    JOIN Artists ON Albums.artist_id = Artists.id
    JOIN Formats ON FormattedAlbums.format_id = Formats.id
    """)
    rows = cursor.fetchall()
    for row in rows:
        print(row)



""" // 'GET' FUNCTIONS  (^ BUT RETURN INSTEAD OF PRINT) // """

def get_artists():
    """Query all artists."""
    cursor.execute("SELECT * FROM Artists")
    rows = cursor.fetchall()
    return rows

def get_albums():
    """Query all albums."""
    cursor.execute("SELECT * FROM Albums")
    rows = cursor.fetchall()
    return rows

def get_formats():
    """Query all formats."""
    cursor.execute("SELECT * FROM Formats")
    rows = cursor.fetchall()
    return rows

def get_formatted_albums():
    """Query all formatted albums."""
    cursor.execute("""
    SELECT Albums.title, Artists.name, Albums.year, Formats.format_name
    FROM FormattedAlbums
    JOIN Albums ON FormattedAlbums.album_id = Albums.id
    JOIN Artists ON Albums.artist_id = Artists.id
    JOIN Formats ON FormattedAlbums.format_id = Formats.id
    """)
    rows = cursor.fetchall()
    return rows

def get_albums_by_media(media_type):
    """Retrieve albums that belong to a specific media type."""
    cursor.execute("""
        SELECT Albums.title, Artists.name, Albums.year, Formats.format_name
        FROM Albums
        JOIN Artists ON Albums.artist_id = Artists.id
        JOIN FormattedAlbums ON Albums.id = FormattedAlbums.album_id
        JOIN Formats ON FormattedAlbums.format_id = Formats.id
        WHERE Formats.format_name = ?
    """, (media_type,))
    albums = cursor.fetchall()
    return albums

def get_albums_by_artist(artist_name):
    """Retrieve albums that belong to a specific artist."""
    cursor.execute("""
        SELECT Albums.title, Artists.name, Albums.year, Formats.format_name
        FROM Albums
        JOIN Artists ON Albums.artist_id = Artists.id
        JOIN FormattedAlbums ON Albums.id = FormattedAlbums.album_id
        JOIN Formats ON FormattedAlbums.format_id = Formats.id
        WHERE Artists.name = ?
    """, (artist_name,))
    albums = cursor.fetchall()
    return albums



""" // DELETE FORMATTED ALBUM FUNCTION // """

def delete_formatted_album(album_name, format_name):
    """Delete a formatted album from FormattedAlbums."""
    album_id = find_album_id(album_name)
    format_id = find_format_id(format_name)
    cursor.execute("""DELETE FROM FormattedAlbums WHERE album_id = ? AND format_id = ?""", (album_id, format_id))



""" // QUERYING BASED ON TIME PERIOD //"""

def formatted_album_between_years(start_year, end_year):
    """Query formatted albums which were released between the specified start and end years."""
    cursor.execute(
        """SELECT Albums.title, Artists.name, Albums.year, Formats.format_name
            FROM FormattedAlbums
            JOIN Albums ON FormattedAlbums.album_id = Albums.id
            JOIN Artists ON Albums.artist_id = Artists.id
            JOIN Formats ON FormattedAlbums.format_id = Formats.id
            WHERE Albums.year BETWEEN ? AND ?""",
            (start_year, end_year) )
    between_albums = cursor.fetchall()
    return between_albums



""" // ARTIST POPULARITY FUNCTIONS // """

def descending_count_albums_by_artist():
    """This function returns the number of albums I have in my posession by each artist, then sorts by popularity in descending order."""
    cursor.execute("""
        SELECT Artists.name, COUNT(Albums.id) as album_count
        FROM Albums
        JOIN Artists on Albums.artist_id = Artists.id
        GROUP BY Artists.name
        ORDER BY album_count DESC
        """)
    descending_count_query = cursor.fetchall()
    return descending_count_query

def artist_album_count(artist_name):
    """How many albums do I posess from this specific artist?"""
    cursor.execute("""
        SELECT COUNT(Albums.id)
        FROM Albums
        JOIN Artists on Albums.artist_id = Artists.id
        WHERE Artists.name = ?""", (artist_name,))
    count = cursor.fetchone()[0]
    return count



""" // SOME GENRE-RELATED FUNCTIONS // """
import random as rand

def associate_album_with_genres(album_title, genre_names):
    """Associate an album with one or more genres."""
    album_id = find_album_id(album_title)
    for genre_name in genre_names:
        genre_id = find_genre_id(genre_name)
        if genre_id is None:
            genre_id = insert_genre(genre_name)
        try:
            cursor.execute("""INSERT INTO AlbumGenres (album_id, genre_id) VALUES (?, ?)""", (album_id, genre_id))
        except sqlite3.IntegrityError:
            # Handle the case where the association already exists
            print(f"Album '{album_title}' is already associated with genre '{genre_name}'.")
    conn.commit()

def get_albums_by_genre(genre_name):
    """Retrieve albums that belong to a specific genre."""
    cursor.execute("""
        SELECT Albums.title, Artists.name, Albums.year, Formats.format_name
        FROM Albums
        JOIN Artists ON Albums.artist_id = Artists.id
        JOIN AlbumGenres ON Albums.id = AlbumGenres.album_id
        JOIN FormattedAlbums ON Albums.id = FormattedAlbums.album_id
        JOIN Formats ON FormattedAlbums.format_id = Formats.id
        JOIN Genres ON AlbumGenres.genre_id = Genres.id
        WHERE Genres.genre_name = ?
    """, (genre_name,))
    albums = cursor.fetchall()
    return albums

def get_genres_for_album(album_title):
    """Retrieve genres associated with a specific album."""
    cursor.execute("""
        SELECT Genres.genre_name
        FROM Albums
        JOIN AlbumGenres ON Albums.id = AlbumGenres.album_id
        JOIN Genres ON AlbumGenres.genre_id = Genres.id
        WHERE Albums.title = ?
    """, (album_title,))
    genres = cursor.fetchall()
    return [genre[0] for genre in genres]

def remove_genre_from_album(album_title, genre_name):
    """Remove a genre association from a specific album."""
    album_id = find_album_id(album_title)
    genre_id = find_genre_id(genre_name)
    cursor.execute("""
        DELETE FROM AlbumGenres
        WHERE album_id = ? AND genre_id = ?
    """, (album_id, genre_id))
    conn.commit()



""" // FUNCTIONS FOR REFACTORING MAIN SCRIPT // """

def add_music(media_list, media_type):
    for media in media_list:
        insert_album(media[0], media[1], media[2])
        insert_formatted_album(media[0], media_type)
        associate_album_with_genres(media[0], media[3])

def random_album_suggestion():
    type = input("Would you like to select an album based on (1) time of release or (2) genre? (Choose '1' or '2')\n").strip()
    if type == '1':
        select_album_by_time()
    elif type == '2':
        select_album_by_genre()
    else:
        print("Invalid selection. Please restart the program and choose a valid option.")

def select_album_by_time():
    beginning = int(input("What is the oldest year you would like to listen to? (Enter a year, ie, '1960')\n"))
    ending = int(input("What is the most recent year you would like to listen to? (Enter a year >= your last selection)\n"))
    possibilities = formatted_album_between_years(beginning, ending)
    media = input('What media type are you listening on?\n').strip()
    new_possibilities = [i for i in possibilities if i[3] == media]
    if new_possibilities:
        quantity = int(input(f"How many suggestions would you like? ({len(new_possibilities)} maximum)\n"))
        if quantity <= len(new_possibilities):
            suggest_albums(new_possibilities, quantity)
        else:
            print(f"You don't have quite that many options to choose from...\n But here's what you have:\n")
            suggest_albums(new_possibilities, len(new_possibilities))
    else:
        print(f"No albums found for the given criteria.")

def select_album_by_genre():
    print(f'Here are the possible genres to listen to:')
    query_genres()
    genre = input("Which genre would you like to listen to? (Enter name of genre)\n").strip()
    possibilities = get_albums_by_genre(genre)
    media = input('What media type are you listening on?\n').strip()
    new_possibilities = [i for i in possibilities if i[3] == media]
    if new_possibilities:
        quantity = int(input(f"How many suggestions would you like? ({len(new_possibilities)} maximum) \n"))
        if quantity <= len(new_possibilities):
            suggest_albums(new_possibilities, quantity)
        else:
            print(f"You don't have quite that many options to choose from... \nBut here's what you have:\n")
            suggest_albums(new_possibilities, len(new_possibilities))           
    else:
        print(f"No albums found for the given criteria.")

def suggest_albums(possibilities, quantity):
    if quantity == 1:
        choice = rand.choice(possibilities)
        print(f"Here is our selection: {choice}. Happy listening!")
    elif quantity > 1:
        choices = rand.sample(possibilities, quantity)
        print(f"Here are some options...\n")
        for choice in choices:
            print(f"{choice}\n")
        print(f"Enjoy!")
    else:
        print("Invalid quantity. Please restart the program and choose a valid option.")

def search_albums():
    way = input(f"How would you like to search for albums?\n(1) Time Period\n(2) Artist\n(3) Media Type\n(4) Genre\nChoose '1', '2', '3' or '4':\n").strip()
    if way == '1':
        search_by_time_period()
    elif way == '2':
        search_by_artist()
    elif way == '3':
        search_by_media_type()
    elif way == '4':
        search_by_genre()
    else:
        print("Invalid selection. Please restart the program and choose a valid option.")

def search_by_time_period():
    beginning = int(input("What is the earliest year you would like to browse? (Enter a year, ie, '1960')\n"))
    ending = int(input("What is the most recent year you would like to browse? (Enter a year >= your last selection)\n"))
    possibilities = formatted_album_between_years(beginning, ending)
    print(f"Here are your albums between the years {beginning} and {ending}:\n")
    for line in possibilities:
        print(f"{line}\n")

def search_by_artist():
    artist = input('What artist would you like to search for?\n').strip()
    number = artist_album_count(artist)
    print(f"You own {number} albums by {artist}. Here they are:\n")
    possibilities = get_albums_by_artist(artist)
    for line in possibilities:
        print(f"{line}\n")

def search_by_media_type():
    print(f"Here are your possible media types:")
    print(f"{query_formats()}")
    format = input("Which media type would you like to see? (Enter name of media type)\n").strip()
    possibilities = get_albums_by_media(format)
    print(f"Here are all of your {format} albums:\n")
    for line in possibilities:
        print(f"{line}\n")

def search_by_genre():
    print(f'Here are the possible genres to listen to:')
    query_genres()
    genre = input("Which genre would you like to listen to? (Enter name of genre)\n").strip()
    possibilities = get_albums_by_genre(genre)
    print(f"Here are all of your {genre} albums:\n")
    for line in possibilities:
        print(f"{line}\n")

def add_new_music():
    while True:
        album_name = input("What is the name of the album?\n").strip()
        artist_name = input("Who is the artist of that album?\n").strip()
        
        while True:
            year = input("What year was this album released?\n").strip()
            if year.isdigit() and len(year) == 4:  # Basic check for valid year
                break
            else:
                print("Please enter a valid year (e.g., 2020).")
        
        insert_album(album_name, artist_name, year)
        
        while True:
            format = input("What format is this album? (e.g., CD, vinyl, cassette)\n").strip()
            if format in ['CD', 'vinyl', 'cassette']:
                break
            else:
                print("Please enter a valid format (CD, Vinyl, Cassette).")
        
        insert_formatted_album(album_name, format)
        
        genres = input("Enter the genres for this album, separated by commas (e.g., Rock, Pop):\n").strip()
        genre_list = [genre.strip() for genre in genres.split(',')]
        associate_album_with_genres(album_name, genre_list)
        
        cont = input("Added. Do you have another album to add? ('Yes' or 'No')\n").strip().lower()
        if cont == 'no':
            print("Thank you for starting or growing your collection. Cheers!")
            break
