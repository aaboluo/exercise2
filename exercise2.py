import sqlite3


# Reads the file stephen_king_adaptations.txt
with open("stephen_king_adaptations.txt") as f:
    contents = f.read().strip()

# Copies all the content from that file to a list called stephen_king_adaptations_list
content_list = [
    [i for i in content.split(",")]
    for content in contents.split("\n")
]

# Connect to the database
db_file = 'stephen_king_adaptations.db'
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Establishes a connection with a new SQLite database called
# stephen_king_adaptations.db
# Delete the table if it exists
cursor.execute('DROP TABLE IF EXISTS stephen_king_adaptations_table')

# Creates a table called stephen_kind_adaptations_table with the column names
# movieID, movieName, movieYear, imdbRating.
create_table_sql = """
CREATE TABLE IF NOT EXISTS stephen_king_adaptations_table (
    movieID TEXT PRIMARY KEY,
    movieName TEXT NOT NULL,
    movieYear TEXT,
    imdbRating TEXT
);
"""

cursor.execute(create_table_sql)

# Takes the content from stephen_king_adaptations_list and inserts it into the table stephen_king_adaptations_table
insert_sql = 'INSERT INTO stephen_king_adaptations_table (movieID, movieName, movieYear, imdbRating) VALUES (?, ?, ?, ?)'
cursor.executemany(insert_sql, content_list)

# Gives the user the option to search for movies in the database, based on the following parameters. This should be presented to the user on a loop, until the user picks the option to stop:
while 1:
    print("1. Movie name\n2. Movie year\n3. Movie rating\n4. STOP")
    number = input("Your Choice: ")
    if number == "4":
        print("EXIT")
        break
    if number == "1":
        movie_name = input("Movie Title: ")
        query = "SELECT * FROM stephen_king_adaptations_table WHERE movieName = ?"
        cursor.execute(query, (movie_name,))

        results = cursor.fetchall()
        if results:
            for row in results:
                print(f"\nmovieID: {row[0]}, movieName: {row[1]}, movieYear: {row[2]}, imdbRating: {row[3]}\n")
        else:
            print("\nNo such movie exists in our database.\n")
    elif number == "2":
        movie_year = input("Movie Year: ")
        query = "SELECT * FROM stephen_king_adaptations_table WHERE movieYear = ?"
        cursor.execute(query, (movie_year,))

        results = cursor.fetchall()
        print("\n")
        if results:
            for row in results:
                print(f"movieID: {row[0]}, movieName: {row[1]}, movieYear: {row[2]}, imdbRating: {row[3]}")
        else:
            print("No movies were found for that year in our database.")
        print("\n")
    elif number == "3":
        movie_rate = input("Movie Rating: ")
        query = "SELECT * FROM stephen_king_adaptations_table WHERE imdbRating > ?"
        cursor.execute(query, (float(movie_rate),))
        results = cursor.fetchall()
        print("\n")
        if results:
            for row in results:
                print(f"movieID: {row[0]}, movieName: {row[1]}, movieYear: {row[2]}, imdbRating: {row[3]}")
        else:
            print("No movies at or above that rating were found in the database.")
        print("\n")

conn.commit()
conn.close()
