import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("inventory.db")  # Replace "inventory.db" with your database name

# Create a cursor object to interact with the database
cursor = conn.cursor()

print("Connected to SQLite database successfully!")

# Sample data
clinic_name = "Dental Care" 
location = "RamBagh"
# SQL command to insert data
insert_user = "INSERT INTO Clinics (clinic_name, location) VALUES (?, ?)"
cursor.execute(insert_user, (clinic_name, location))

# Commit the changes
conn.commit()
print("User inserted successfully!")
