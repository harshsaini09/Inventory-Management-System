import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

# Sample data
clinic_id = 1
item_name = "Gloves"
quantity = 30
expiry_date = "2028-03-32"
supplier = "Ramesh"
# SQL command to insert data
insert_user = "INSERT INTO Inventory (clinic_id, item_name, quantity, expiry_date, supplier) VALUES (?, ?, ?, ?, ?)"
cursor.execute(insert_user, (clinic_id, item_name, quantity, expiry_date, supplier))

# Commit the changes
conn.commit()
print("User inserted successfully!")
