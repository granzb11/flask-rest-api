import sqlite3 as sql

connection = sql.connect("data.db")
cursor = connection.cursor()

# using INTEGER in this create statement so that the db auto-increments the ID for us
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price real)"
cursor.execute(create_table)

# cursor.execute("INSERT INTO items VALUES(NULL, 'test', 10.99)")

connection.commit()
connection.close()
