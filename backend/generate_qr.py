import qrcode
import uuid

product_code = "PV-" + str(uuid.uuid4())[:8].upper()

verification_url = f"http://172.20.10.3:8000/verify/{product_code}"

qr = qrcode.make(verification_url)

qr.save(f"{product_code}.png")

print("Product Code:", product_code)
print("QR Code created:", f"{product_code}.png")