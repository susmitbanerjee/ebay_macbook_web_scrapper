import sqlite3


class Listing:
    def __init__(self, title, price, category):
        self.title = title
        self.price = price
        self.category = category

    def print_all_details(self):
        print("Title: "+self.title+" Price: "+self.price+" Category: "+self.category)

    def save_to_database(self):
        conn = sqlite3.connect('ebay_macbooks.db')
        c = conn.cursor()

        # Create table if not exists
        c.execute('''CREATE TABLE IF NOT EXISTS products
                     (title TEXT, price REAL, category TEXT)''')

        # Insert data into the table
        c.execute("INSERT INTO products (title, price, category) VALUES (?, ?, ?)",
                  (self.title, self.price, self.category))

        # Commit changes and close connection
        conn.commit()
        conn.close()
