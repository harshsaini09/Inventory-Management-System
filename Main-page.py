import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Import ttk for Treeview
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()


# Hexa to RBG
def rgb_to_hex(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"
# Dashboard class (Assuming it's defined as provided previously)
class Dashboard:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title("Dashboard - Inventory Management System")
        self.root.geometry("700x500")
        self.root.configure(bg=rgb_to_hex(240, 244, 247))  # Light background color

        # Header Section
        header_frame = tk.Frame(root, bg=rgb_to_hex(59, 89, 152), height=60)
        header_frame.pack(fill="x")

        header_label = tk.Label(
            header_frame,
            text="Inventory Management Dashboard",
            font=("Helvetica", 18, "bold"),
            bg=rgb_to_hex(59, 89, 152),
            fg="white"
        )
        header_label.pack(pady=10)

        # Button Section
        button_frame = tk.Frame(root, bg=rgb_to_hex(240, 244, 247), pady=20)
        button_frame.pack(expand=True)

        button_style = {"font": ("Helvetica", 12, "bold"), "width": 25, "height": 2, "borderwidth": 2}

        view_button = tk.Button(
            button_frame,
            text="View Current Stock",
            command=self.view_current_stock,
            bg=rgb_to_hex(255, 131, 131),
            fg="black",
            **button_style
        )
        view_button.pack(pady=10)

        add_button = tk.Button(
            button_frame,
            text="Add New Stock",
            command=self.add_stock,
            bg=rgb_to_hex(255, 231, 131),
            fg="black",
            **button_style
        )
        add_button.pack(pady=10)

        edit_button = tk.Button(
            button_frame,
            text="Edit Stock",
            command=self.edit_stock,
            bg=rgb_to_hex(131, 255, 157),
            fg="black",
            **button_style
        )
        edit_button.pack(pady=10)

        account_button = tk.Button(
            button_frame,
            text="User Account Settings",
            command=self.user_account_settings,
            bg=rgb_to_hex(131, 212, 255),
            fg="black",
            **button_style
        )
        account_button.pack(pady=10)

        logout_button = tk.Button(
            button_frame,
            text="Logout",
            command=self.logout,
            bg=rgb_to_hex(255, 131, 131),
            fg="black",
            **button_style
        )
        logout_button.pack(pady=10)
    
    def view_current_stock(self):
         # View current stock window with Treeview
        stock_window = tk.Toplevel(self.root)
        stock_window.title("Current Stock")
        stock_window.geometry("800x500")
        stock_window.configure(bg=rgb_to_hex(240, 244, 247))

        tk.Label(
            stock_window, text="View Current Stock", font=("Helvetica", 16), bg=rgb_to_hex(240, 244, 247)
        ).pack(pady=10)

        cursor.execute("SELECT clinic_id, clinic_name FROM Clinics")
        clinics = cursor.fetchall()

        tk.Label(stock_window, text="Select Clinic:", font=("Helvetica", 12), bg=rgb_to_hex(240, 244, 247)).pack(pady=5)
        clinic_combobox = ttk.Combobox(stock_window, values=[clinic[1] for clinic in clinics], state="readonly")
        clinic_combobox.pack(pady=5)

        # Fetch clinic data for the dropdown (combobox)
        cursor.execute("SELECT clinic_id, clinic_name FROM Clinics")
        clinics = cursor.fetchall()

        # Create a combobox to select a clinic
        # tk.Label(stock_window, text="Select Clinic").pack(pady=5)
        # clinic_combobox = ttk.Combobox(stock_window, values=[clinic[1] for clinic in clinics])
        # clinic_combobox.pack(pady=5)

        # Function to update the stock data based on selected clinic
        def update_stock():
            selected_clinic_name = clinic_combobox.get()
            cursor.execute("SELECT clinic_id FROM Clinics WHERE clinic_name = ?", (selected_clinic_name,))
            selected_clinic_id = cursor.fetchone()[0]

            cursor.execute("SELECT * FROM Inventory WHERE clinic_id = ?", (selected_clinic_id,))
            rows = cursor.fetchall()

            for item in tree.get_children():
                tree.delete(item)
            for row in rows:
                tree.insert("", "end", values=row)
    
        tk.Button(stock_window, text="Load Stock", command=update_stock, bg=rgb_to_hex(15, 50, 170), fg="white", font=("Helvetica", 10, "bold"),).pack(pady=5)
        tree = ttk.Treeview(
            stock_window,
            columns=("Item ID", "Clinic ID", "Name", "Quantity", "Expiry Date", "Supplier"),
            show="headings",
        )
        tree.heading("Item ID", text="Item ID")
        tree.heading("Clinic ID", text="Clinic ID")
        tree.heading("Name", text="Name")
        tree.heading("Quantity", text="Quantity")
        tree.heading("Expiry Date", text="Expiry Date")
        tree.heading("Supplier", text="Supplier")

        tree.column("Item ID", width=70)
        tree.column("Clinic ID", width=70)
        tree.column("Name", width=150)
        tree.column("Quantity", width=80)
        tree.column("Expiry Date", width=120)
        tree.column("Supplier", width=150)

        tree.pack(fill="both", expand=True, pady=10)

        scrollbar = ttk.Scrollbar(stock_window, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        if clinics:
            clinic_combobox.set(clinics[0][1])
            update_stock()


    def add_stock(self):
        # Add stock window with organized layout
        add_stock_window = tk.Toplevel(self.root)
        add_stock_window.title("Add New Stock")
        add_stock_window.geometry("500x600")  # Increased window height for better visibility of the submit button
        add_stock_window.configure(bg=rgb_to_hex(240, 244, 247))

        # Centralized frame with padding for content
        frame = tk.Frame(add_stock_window, bg=rgb_to_hex(240, 244, 247), padx=20, pady=20)
        frame.pack(expand=True, fill="both")

        # Title Label
        tk.Label(
            frame,
            text="Add New Stock",
            font=("Helvetica", 16, "bold"),
            bg=rgb_to_hex(240, 244, 247),
            fg="#4CAF50"
        ).pack(pady=20)

        # Fields and entries for stock details
        fields = [("Clinic ID", None), ("Item Name", None), ("Quantity", None), 
                ("Expiry Date (YYYY-MM-DD)", None), ("Supplier", None)]
        entries = {}

        for label, _ in fields:
            tk.Label(
                frame,
                text=label,
                font=("Helvetica", 12),
                bg=rgb_to_hex(240, 244, 247)
            ).pack(pady=5)
            entry = tk.Entry(frame, font=("Helvetica", 12), width=30)
            entry.pack(pady=5)
            entries[label] = entry

        # Submit button to insert stock into database
        def submit_stock():
            values = {field: entry.get() for field, entry in entries.items()}
            if not all(values.values()):
                messagebox.showerror("Input Error", "Please fill all fields.")
                return

            try:
                quantity = int(values["Quantity"])
            except ValueError:
                messagebox.showerror("Input Error", "Quantity must be a number.")
                return

            cursor.execute(
                """
                INSERT INTO Inventory (clinic_id, item_name, quantity, expiry_date, supplier)
                VALUES (?, ?, ?, ?, ?)
                """,
                (values["Clinic ID"], values["Item Name"], quantity, values["Expiry Date (YYYY-MM-DD)"], values["Supplier"]),
            )
            conn.commit()
            messagebox.showinfo("Success", "New stock added successfully!")
            add_stock_window.destroy()

        # Submit Button
        tk.Button(
            frame,
            text="Submit",
            command=submit_stock,
            bg=rgb_to_hex(76, 175, 80),
            fg="white",
            font=("Helvetica", 16, "bold"),
            relief="raised",
            width=15
        ).pack(pady=30)

        # Footer
        tk.Label(
            add_stock_window,
            text="© 2024 Inventory System",
            font=("Helvetica", 10),
            bg=rgb_to_hex(240, 244, 247),
            fg="gray"
        ).pack(side="bottom", pady=10)





    def edit_stock(self):
        # Create a new window for editing stock
        edit_stock_window = tk.Toplevel(self.root)
        edit_stock_window.title("Edit Stock")
        edit_stock_window.geometry("500x500")
        edit_stock_window.configure(bg=rgb_to_hex(240, 244, 247))

        tk.Label(edit_stock_window, text="Edit Stock Details", font=("Helvetica", 16, "bold"), bg=rgb_to_hex(240, 244, 247)).pack(pady=10)

        # Fetch all items (or stock entries) to populate the dropdown
        cursor.execute("SELECT item_id, item_name FROM Inventory")
        items = cursor.fetchall()

        # Combobox to select the stock item
        tk.Label(edit_stock_window, text="Select Item", font=("Helvetica", 12), bg=rgb_to_hex(240, 244, 247)).pack(pady=5)
        item_combobox = ttk.Combobox(edit_stock_window, values=[item[1] for item in items], state="readonly")
        item_combobox.pack(pady=5)

        # Entry fields for stock details
        entries = {}
        fields = ["Item Name", "Quantity", "Expiry Date (YYYY-MM-DD)", "Supplier"]
        for field in fields:
            tk.Label(edit_stock_window, text=field, font=("Helvetica", 12), bg=rgb_to_hex(240, 244, 247)).pack(pady=5)
            entry = tk.Entry(edit_stock_window, width=40)
            entry.pack(pady=5)
            entries[field] = entry

        # Function to populate fields based on selected item
        def load_item_details():
            selected_item_name = item_combobox.get()
            cursor.execute("SELECT * FROM Inventory WHERE item_name = ?", (selected_item_name,))
            item = cursor.fetchone()
            if item:
                entries["Item Name"].delete(0, tk.END)
                entries["Item Name"].insert(0, item[2])
                entries["Quantity"].delete(0, tk.END)
                entries["Quantity"].insert(0, item[3])
                entries["Expiry Date (YYYY-MM-DD)"].delete(0, tk.END)
                entries["Expiry Date (YYYY-MM-DD)"].insert(0, item[4])
                entries["Supplier"].delete(0, tk.END)
                entries["Supplier"].insert(0, item[5])
            else:
                messagebox.showerror("Error", "Item not found!")

        tk.Button(edit_stock_window, text="Load Item Details", command=load_item_details, bg=rgb_to_hex(37, 84, 243), fg="white", font=("Helvetica", 14, "bold"), width=20).pack(pady=8)

        # Submit changes function
        def submit_changes():
            new_values = {field: entries[field].get() for field in fields}
            if any(not value for value in new_values.values()):
                messagebox.showerror("Input Error", "Please fill all fields.")
                return
            try:
                new_values["Quantity"] = int(new_values["Quantity"])
            except ValueError:
                messagebox.showerror("Input Error", "Quantity must be a number.")
                return
            cursor.execute("""
                UPDATE Inventory 
                SET item_name = ?, quantity = ?, expiry_date = ?, supplier = ?
                WHERE item_name = ?
            """, (new_values["Item Name"], new_values["Quantity"], new_values["Expiry Date (YYYY-MM-DD)"], new_values["Supplier"], item_combobox.get()))
            conn.commit()
            messagebox.showinfo("Success", "Stock details updated successfully!")
            edit_stock_window.destroy()

        tk.Button(edit_stock_window, text="Submit Changes", command=submit_changes, bg=rgb_to_hex(76, 175, 80), fg="white", font=("Helvetica", 14, "bold"), width=20).pack(pady=20)



    
    def user_account_settings(self):
        # Create a new window for account settings
        account_window = tk.Toplevel(self.root)
        account_window.title("User Account Settings")
        account_window.geometry("400x400")
        account_window.configure(bg=rgb_to_hex(247, 249, 252))

        tk.Label(account_window, text="User Account Settings", font=("Helvetica", 16, "bold"), bg=rgb_to_hex(247, 249, 252)).pack(pady=10)

        # Fetch current user's details
        cursor.execute("SELECT password, contact_info FROM Users WHERE username = ?", (self.username,))
        user_data = cursor.fetchone() or ("", "")

        entries = {}
        fields = {"Old Password": user_data[0], "New Password": "", "Contact Information": user_data[1]}
        for field, value in fields.items():
            tk.Label(account_window, text=field, font=("Helvetica", 12), bg=rgb_to_hex(247, 249, 252)).pack(pady=5)
            entry = tk.Entry(account_window, width=40, show="*" if "Password" in field else None)
            entry.insert(0, value)
            entry.pack(pady=5)
            entries[field] = entry

        def submit_changes():
            new_password = entries["New Password"].get()
            contact_info = entries["Contact Information"].get()

            if not new_password or not contact_info:
                messagebox.showerror("Input Error", "Please fill all fields.")
                return

            cursor.execute("""
                UPDATE Users 
                SET password = ?, contact_info = ?
                WHERE username = ?
            """, (new_password, contact_info, self.username))
            conn.commit()
            messagebox.showinfo("Success", "Account information updated successfully!")
            account_window.destroy()

        tk.Button(account_window, text="Submit Changes", command=submit_changes, bg=rgb_to_hex(76, 175, 80), fg="white", font=("Helvetica", 12, "bold"), width=15).pack(pady=20)



    def logout(self):
        self.root.destroy()
        messagebox.showinfo("Logout", "Logged out successfully!")

# Function to handle login
# Login Function
def login():
    username = username_entry.get()
    password = password_entry.get()

    # Verify username and password
    cursor.execute("SELECT * FROM Users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()

    if user:
        messagebox.showinfo("Login Successful", "Welcome to the Inventory Management System!")
        login_window.destroy()  # Close the login window
        
        # Pass the username to the Dashboard instance
        dashboard_window = tk.Tk()
        app = Dashboard(dashboard_window, username)  # Pass username here
        dashboard_window.mainloop()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password. Please try again.")

# Login GUI
login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("500x400")  # Increased window size
login_window.configure(bg=rgb_to_hex(240, 244, 247))

# Styling
font_title = ("Helvetica", 18, "bold")
font_label = ("Helvetica", 14)
font_entry = ("Helvetica", 14)
font_button = ("Helvetica", 14, "bold")

# Frame for centralizing content and adding outer margins
frame = tk.Frame(login_window, bg=rgb_to_hex(240, 244, 247), padx=20, pady=20)
frame.pack(expand=True)

# Title Label
tk.Label(
    frame, 
    text="Inventory Management Login", 
    font=font_title, 
    bg=rgb_to_hex(240, 244, 247), 
    fg="#4CAF50"
).pack(pady=20)

# Username Label and Entry
tk.Label(
    frame, 
    text="Username", 
    font=font_label, 
    bg=rgb_to_hex(240, 244, 247)
).pack(pady=5)
username_entry = tk.Entry(frame, font=font_entry, width=30)
username_entry.pack(pady=5)

# Password Label and Entry
tk.Label(
    frame, 
    text="Password", 
    font=font_label, 
    # bg=rgb_to_hex(240, 244, 247)
).pack(pady=5)
password_entry = tk.Entry(frame, show="*", font=font_entry, width=30)
password_entry.pack(pady=5)

# Login Button
login_button = tk.Button(
    frame, 
    text="Login", 
    command=login, 
    font=font_button, 
    bg=rgb_to_hex(76, 175, 80), 
    fg="white", 
    relief="raised",
    width=20
)
login_button.pack(pady=30)

# Footer
tk.Label(
    login_window, 
    text="© 2024 Inventory System", 
    font=("Helvetica", 10), 
    bg=rgb_to_hex(240, 244, 247), 
    fg="gray"
).pack(side="bottom", pady=10)

login_window.mainloop()

# Close the database connection when the application exits
conn.close()