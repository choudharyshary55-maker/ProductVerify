import sqlite3

product_code = input("Enter Product Code: ")

connection = sqlite3.connect("products.db")
cursor = connection.cursor()

cursor.execute(
    "SELECT brand, product_name, batch_number, status FROM products WHERE product_code = ?",
    (product_code,)
)

product = cursor.fetchone()

connection.close()

if product:
    brand, product_name, batch_number, status = product

    print("\n========== PRODUCT VERIFICATION ==========")
    print("Brand:", brand)
    print("Product:", product_name)
    print("Batch:", batch_number)
    print("Status:", status)
    print("==========================================")
else:
    print("\n❌ PRODUCT NOT FOUND")