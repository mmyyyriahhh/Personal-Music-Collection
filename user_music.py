"""Script for user input for Personal Music Collection project,
Myriah Hodgson 06/22/2024"""

import sqlite3
import functions
import my_music
import random as rand

def main():

    # Greet the user... hehe
    print(f"Hello, welcome to the Music Selector!")
    print(f"Let's get grooving!")

    # My music, or someone else's? (Develop a more generalized way to connect to a different database, eventually...)
    myriah = input("Will you be using Myriah's music today? ('Yes' or 'No')\n").strip().lower()

    if myriah == 'yes':
        # Connect to the database/create it, if not yet created
        conn = sqlite3.connect('music_collection.db')
        cursor = conn.cursor()
        functions.create_tables() # Create the tables needed, if necessary
        functions.add_music(my_music.cds, 'CD')
        functions.add_music(my_music.cassettes, 'cassette')
        functions.add_music(my_music.vinyl, 'vinyl')
    else:
        print(f"Apologies, but outside collections are not yet supported. Sorry!")
        return

    print(f"\nGreat! Now that we have your music, what would you like to do?")
    print(f"We can:")
    print(f"(1) Randomly choose and suggest an album(s)")
    print(f"(2) Search for a specific albums(s)")
    print(f"(3) Add music to your database")

    use = input("Choose '1', '2', or '3':\n").strip()

    if use == '1': # RANDOMIZED ALBUM SUGGESTION
        functions.random_album_suggestion()
    elif use == '2': # QUERYING
        functions.search_albums()
    elif use == '3': # ADDING MUSIC
        functions.add_new_music()
    else:
        print("Invalid selection. Please restart the program and choose a valid option.")
    
    # Close the database connection
    conn.close()
    return

if __name__ == "__main__":
    main()

