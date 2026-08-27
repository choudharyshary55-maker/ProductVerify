import sqlite3
import uuid
import qrcode
from pathlib import Path

# ==========================================
# DATABASE
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "products.db"

# ==========================================
# PRODUCT DETAILS
# ==========================================

brand = input("Enter Brand Name: ").strip()
product_name = input("Enter Product Name: ").strip()
batch_number = input("Enter Batch Number: ").strip()

# ==========================================
# AUTOMATIC PRODUCT CODE
# ==========================================

product_code = "PV-" + str(uuid.uuid4())[:8].upper()

# ==========================================
# DATABASE INSERT
# ==========================================

connection = sqlite3.connect(DATABASE_PATH)
cursor = connection.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_code TEXT UNIQUE NOT NULL,
        brand TEXT NOT NULL,
        product_name TEXT NOT NULL,
        batch_number TEXT NOT NULL,
        status TEXT NOT NULL
    )
    """
)

cursor.execute(
    """
    INSERT INTO products
    (product_code, brand, product_name, batch_number, status)
    VALUES (?, ?, ?, ?, ?)
    """,
    (
        product_code,
        brand,
        product_name,
        batch_number,
        "VERIFIED"
    )
)

connection.commit()
connection.close()

# ==========================================
# LIVE PRODUCTVERIFY URL
# ==========================================

verification_url = (
    f"https://productverify-7.onrender.com/?code={product_code}"
)

# ==========================================
# GENERATE QR CODE
# ==========================================

qr = qrcode.make(verification_url)

qr_file = BASE_DIR / f"{product_code}.png"
qr.save(qr_file)

# ==========================================
# RESULT
# ==========================================

print("\n========== PRODUCT ADDED ==========")
print("Product Code:", product_code)
print("Brand:", brand)
print("Product:", product_name)
print("Batch:", batch_number)
print("Status: VERIFIED")
print("Verification URL:", verification_url)
print("QR Code:", qr_file)
print("===================================")
