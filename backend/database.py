import sqlite3

connection = sqlite3.connect("products.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_code TEXT UNIQUE NOT NULL,
    brand TEXT NOT NULL,
    product_name TEXT NOT NULL,
    batch_number TEXT NOT NULL,
    status TEXT NOT NULL
)
""")

connection.commit()
connection.close()

print("Database ready!")