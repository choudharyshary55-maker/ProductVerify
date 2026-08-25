import sqlite3
import uuid
import qrcode

# Product details
brand = input("Enter Brand Name: ")
product_name = input("Enter Product Name: ")
batch_number = input("Enter Batch Number: ")

# Automatic Product Code
product_code = "PV-" + str(uuid.uuid4())[:8].upper()

# Database
connection = sqlite3.connect("products.db")
cursor = connection.cursor()

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

# ProductVerify frontend URL
verification_url = (
    f"http://172.20.10.3:5500/index.html?code={product_code}"
)

# Generate QR Code
qr = qrcode.make(verification_url)

qr_file = f"{product_code}.png"
qr.save(qr_file)

print("\n========== PRODUCT ADDED ==========")
print("Product Code:", product_code)
print("Brand:", brand)
print("Product:", product_name)
print("Batch:", batch_number)
print("Status: VERIFIED")
print("Verification URL:", verification_url)
print("QR Code:", qr_file)
print("===================================")