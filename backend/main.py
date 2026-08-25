from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pathlib import Path
import sqlite3
import html


app = FastAPI()


# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# DATABASE PATH
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "products.db"


# ==========================================
# DATABASE INITIALIZATION
# ==========================================

def initialize_database():

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

    connection.commit()
    connection.close()


# Initialize database when application starts
initialize_database()


# ==========================================
# HOME
# ==========================================

@app.get("/")
def home():

    return {
        "message": "ProductVerify API is running!",
        "database": "connected"
    }


# ==========================================
# VERIFY PRODUCT
# ==========================================

@app.get(
    "/verify/{product_code}",
    response_class=HTMLResponse
)
def verify_product(product_code: str):

    product_code = product_code.strip()

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            brand,
            product_name,
            batch_number,
            status
        FROM products
        WHERE product_code = ?
        """,
        (product_code,)
    )

    product = cursor.fetchone()

    connection.close()


    # ======================================
    # PRODUCT FOUND
    # ======================================

    if product:

        brand, product_name, batch_number, status = product

        # Prevent HTML injection
        brand = html.escape(str(brand))
        product_name = html.escape(str(product_name))
        batch_number = html.escape(str(batch_number))
        status = html.escape(str(status))
        product_code = html.escape(product_code)

        return f"""
        <div class="backend-card">

            <div class="success-icon">
                ✓
            </div>

            <div class="verified-badge">
                AUTHENTIC PRODUCT
            </div>

            <h2 class="verified">
                PRODUCT VERIFIED
            </h2>

            <h3 class="product-name">
                {brand}
            </h3>

            <div class="details">

                <div class="detail-row">
                    <span>Product</span>
                    <strong>{product_name}</strong>
                </div>

                <div class="detail-row">
                    <span>Batch Number</span>
                    <strong>{batch_number}</strong>
                </div>

                <div class="detail-row">
                    <span>Status</span>
                    <strong class="status">
                        {status}
                    </strong>
                </div>

                <div class="detail-row">
                    <span>Product Code</span>
                    <strong>{product_code}</strong>
                </div>

            </div>

            <div class="verification-message">
                ✓ This product has been successfully verified
                by ProductVerify.
            </div>

        </div>
        """


    # ======================================
    # PRODUCT NOT FOUND
    # ======================================

    product_code = html.escape(product_code)

    return f"""
    <div class="backend-error">

        <div class="error-icon">
            !
        </div>

        <h2 class="not-found">
            PRODUCT NOT VERIFIED
        </h2>

        <p class="error-message">
            This product code could not be found in the
            ProductVerify database.
        </p>

        <div class="code-box">
            Product Code:
            <strong>{product_code}</strong>
        </div>

        <p class="warning">
            Please contact the brand or seller if you
            believe this product is genuine.
        </p>

    </div>
    """