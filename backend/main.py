from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import os
import psycopg2
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
# DATABASE CONNECTION
# ==========================================

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL environment variable is not set")

    return psycopg2.connect(DATABASE_URL)


# ==========================================
# DATABASE INITIALIZATION
# ==========================================

def initialize_database():

    connection = get_connection()
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
        ON CONFLICT (product_code) DO NOTHING
        """,
        (
            "PV-000001",
            "XYZ Cosmetics",
            "Face Serum 30ml",
            "FS26001",
            "VERIFIED"
        )
    )

    connection.commit()
    cursor.close()
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
        "database": "PostgreSQL connected"
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

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            brand,
            product_name,
            batch_number,
            status
        FROM products
        WHERE product_code = %s
        """,
        (product_code,)
    )

    product = cursor.fetchone()

    cursor.close()
    connection.close()


    # ======================================
    # PRODUCT FOUND
    # ======================================

    if product:

        brand, product_name, batch_number, status = product

        brand = html.escape(str(brand))
        product_name = html.escape(str(product_name))
        batch_number = html.escape(str(batch_number))
        status = html.escape(str(status))
        product_code = html.escape(product_code)

        return f"""
        <div class="backend-card">

            <div class="success-icon">
                ?
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
                ? This product has been successfully verified
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
