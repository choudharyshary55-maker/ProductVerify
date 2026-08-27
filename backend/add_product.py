import os
import uuid
import qrcode
import psycopg2
from pathlib import Path

# ==========================================
# PATH
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

# ==========================================
# DATABASE
# ==========================================

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not set."
    )

# ==========================================
# PRODUCT DETAILS
# ==========================================

brand = input("Enter Brand Name: ").strip()
product_name = input("Enter Product Name: ").strip()
batch_number = input("Enter Batch Number: ").strip()

if not brand or not product_name or not batch_number:
    raise ValueError(
        "Brand, Product Name and Batch Number are required."
    )

# ==========================================
# AUTOMATIC PRODUCT CODE
# ==========================================

product_code = "PV-" + str(uuid.uuid4())[:8].upper()

# ==========================================
# DATABASE INSERT
# ==========================================

connection = psycopg2.connect(DATABASE_URL)
cursor = connection.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS products (
        id SERIAL PRIMARY KEY,
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
    VALUES (%s, %s, %s, %s, %s)
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

cursor.close()
connection.close()

# ==========================================
# LIVE PRODUCTVERIFY URL
# ==========================================

verification_url = (
    f"https://productverify.onrender.com/verify/{product_code}"
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