import sqlite3
from flask import Flask, request, render_template_string, abort

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

# --- Templates ---

SEARCH_TEMPLATE = """
<h1>Product Search</h1>
<form method="get" action="/search">
    <input type="text" name="q" size="50">
    <input type="submit" value="Search">
</form>
<hr>
{% if products %}
    <h2>Search Results</h2>
    <ul>
    {% for product in products %}
        <li>{{ product[1] }}: {{ product[2] }}</li>
    {% endfor %}
    </ul>
{% endif %}
"""

INVOICE_TEMPLATE = """
<h1>Invoice Details</h1>
<p><strong>Invoice ID:</strong> {{ invoice[0] }}</p>
<p><strong>User ID:</strong> {{ invoice[1] }}</p>
<p><strong>Amount:</strong> ${{ invoice[2] }}</p>
<p><strong>Details:</strong> {{ invoice[3] }}</p>
"""

# --- Routes ---

@app.route('/')
def index():
    # For the CTF, we'll simulate being logged in as user 1.
    return '<h1>CTF Challenge App</h1><p>You are logged in as user 1.</p><ul><li><a href="/search">Product Search</a></li><li><a href="/invoice/1">View Your Invoice (ID 1)</a></li><li>Try to find the other user\'s invoice!</li></ul>'

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

    return render_template_string(SEARCH_TEMPLATE, products=products)

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

    return render_template_string(INVOICE_TEMPLATE, invoice=invoice_data)


if __name__ == '__main__':
    init_db()
    print(f"CTF App running on port 5006. Good luck!")
    app.run(debug=True, port=5006)
