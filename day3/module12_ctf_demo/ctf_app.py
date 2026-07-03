import sqlite3
from flask import Flask, request, render_template, abort

app = Flask(__name__)
DB_FILE = "ctf.db"

# This is a hardcoded secret! Vulnerability #1
SHIPPING_API_KEY = "shp_live_abcdef1234567890"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS products")
        cursor.execute("DROP TABLE IF EXISTS invoices")
        cursor.execute("CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, description TEXT)")
        cursor.execute("CREATE TABLE invoices (id INTEGER PRIMARY KEY, user_id INTEGER, amount REAL, details TEXT)")
        cursor.execute("INSERT INTO products (name, description) VALUES ('Laptop', 'A powerful laptop')")
        cursor.execute("INSERT INTO products (name, description) VALUES ('Mouse', 'A wireless mouse')")
        cursor.execute("INSERT INTO invoices (user_id, amount, details) VALUES (1, 1200.50, 'Invoice for Laptop')")
        cursor.execute("INSERT INTO invoices (user_id, amount, details) VALUES (2, 25.00, 'Invoice for Mouse')")
        conn.commit()

# --- Routes ---

@app.route('/')
def index():
    # For the CTF, we'll simulate being logged in as user 1.
    return render_template('index.html')

# This search is vulnerable to SQL Injection. Vulnerability #2
@app.route('/search')
def search():
    query = request.args.get('q', '')
    products = []
    if query:
        # Unsafe query construction
        sql_query = f"SELECT * FROM products WHERE name LIKE '%{query}%'"
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            # An attacker can inject SQL here. e.g., q=a' UNION SELECT 1,2,3--
            cursor.execute(sql_query)
            products = cursor.fetchall()

    return render_template('search.html', products=products)

# This endpoint is vulnerable to IDOR. Vulnerability #3
@app.route('/invoice/<invoice_id>')
def invoice(invoice_id):
    # The application does not check if the logged-in user (user 1) is
    # authorized to view the requested invoice.
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM invoices WHERE id = ?", (invoice_id,))
        invoice_data = cursor.fetchone()

    if not invoice_data:
        abort(404)

    return render_template('invoice.html', invoice=invoice_data)


if __name__ == '__main__':
    init_db()
    print(f"CTF App running on port 5006. Good luck!")
    app.run(debug=True, port=5006)
