import sqlite3

# Connect to SQLite and create the database file if it doesn't exist
conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()
print("Database 'inventory.db' created and connected successfully!")

# SQL statements to create tables
create_users_table = """
CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    contact_info TEXT
);
"""

create_clinics_table = """
CREATE TABLE IF NOT EXISTS Clinics (
    clinic_id INTEGER PRIMARY KEY AUTOINCREMENT,
    clinic_name TEXT NOT NULL,
    location TEXT
);
"""

create_inventory_table = """
CREATE TABLE IF NOT EXISTS Inventory (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    clinic_id INTEGER,
    item_name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    expiry_date DATE,
    supplier TEXT,
    FOREIGN KEY (clinic_id) REFERENCES Clinics(clinic_id)
);
"""

create_stock_history_table = """
CREATE TABLE IF NOT EXISTS StockHistory (
    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER,
    change_type TEXT NOT NULL,
    change_quantity INTEGER,
    change_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES Inventory(item_id)
);
"""

# Execute the SQL commands
cursor.execute(create_users_table)
cursor.execute(create_clinics_table)
cursor.execute(create_inventory_table)
cursor.execute(create_stock_history_table)

# Commit the changes and close the connection
conn.commit()
cursor.close()
conn.close()
print("Tables created successfully in 'inventory.db'.")
