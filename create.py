import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('user_data.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Create a table to store user data

# command = """CREATE TABLE IF NOT EXISTS users(name TEXT, password TEXT)"""

# cursor.execute(command)
cursor.execute("INSERT INTO users VALUES ('John','1234567890')")
cursor.execute("INSERT INTO users VALUES ('Joshua','password-josh')")
cursor.execute("INSERT INTO users VALUES ('John','password-james')")

conn.commit()

# Close the database connection when done
conn.close()
