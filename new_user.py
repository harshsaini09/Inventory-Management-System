import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

# Sample data
username = "Harsh"
password = "password12"
contact_info = "Harsh@example.com"

# SQL command to insert data
insert_user = "INSERT INTO Users (username, password, contact_info) VALUES (?, ?, ?)"
cursor.execute(insert_user, (username, password, contact_info))

# Commit the changes
conn.commit()
print("User inserted successfully!")
