# SQL Injection (SQLi) Demo

This directory contains a simple Flask application that is vulnerable to one of the oldest and most dangerous web security vulnerabilities: **SQL Injection**.

## Real-World Impact

SQL Injection vulnerabilities have been the cause of some of the most infamous data breaches in history. Attackers have used SQLi to steal credit card numbers, personal user information, and sensitive corporate data from major companies and governments.

*   **TalkTalk Breach (2015):** A major UK telecom company was breached using a simple SQL injection attack, resulting in the exposure of 157,000 customers' personal data and a fine of £400,000.
*   **Heartland Payment Systems (2008):** In one of the largest breaches ever, attackers used SQL injection to steal over 130 million credit card records.

The impact goes beyond data theft. An attacker can use SQLi to:
*   **Bypass Authentication:** As shown in this demo, they can log in as other users, including administrators.
*   **Modify Data:** Change or delete records in the database.
*   **Denial of Service (DoS):** Run queries that overload the database, crashing the application.
*   **Execute OS Commands:** In some cases, gain full control over the underlying server.

## The Flaw: Mixing Code and Data

The vulnerability occurs when an application takes untrusted user input and uses it to dynamically build a SQL query. By using simple string formatting (like Python's f-strings), the application mixes the **data** (the user's input) with the **code** (the SQL query).

### Vulnerable Code Analysis

In `app.py`, the login function takes the `username` and `password` directly from the form and inserts them into the query string:

```python
# app.py
username = request.form['username']
password = request.form['password']

# VULNERABLE: User input is directly embedded into the SQL query string.
# The database cannot distinguish between the intended query logic and the user's input.
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

cursor.execute(query)
```

## How to Exploit

1.  Install Flask: `pip install Flask`
2.  Run the application: `python app.py`
3.  Open your browser to `http://127.0.0.1:5001/`.

4.  In the username field, enter the classic SQLi payload:
    ```
    ' OR 1=1 --
    ```
    You can leave the password field empty. Click "Login".

### Why it Works

Let's break down how the database sees the final query when you submit the payload:

1.  **Original Query Structure:**
    `SELECT * FROM users WHERE username = '...' AND password = '...'`

2.  **Payload Injection:**
    The application injects the payload `' OR 1=1 --` into the `username` variable.

3.  **The Final, Malicious Query:**
    `SELECT * FROM users WHERE username = '' OR 1=1 --' AND password = ''`

Let's analyze the malicious query part by part:
*   `username = ''`: The first single quote from our payload closes the `username` string, leaving it empty.
*   `OR 1=1`: This is a universally true condition. The `WHERE` clause now effectively becomes `WHERE (username = '') OR (1=1)`. Since `1=1` is always true, the condition for the `WHERE` clause is met for **every single row** in the table.
*   `--`: This is the comment character in SQL. It tells the database to ignore everything that comes after it on the same line. This effectively **removes the password check** from the query.

The database executes this modified query, which asks it to "select all users where the username is empty OR true is true". It finds all users, returns the first one (the admin), and the application logs you in.

## The Fix: Parameterized Queries (Prepared Statements)

The only reliable way to prevent SQL injection is to **never build queries by hand**. Instead, use **parameterized queries**, also known as prepared statements.

With parameterized queries, you send the SQL query template to the database first, with placeholders for the user input. Then, you send the user input separately. The database engine then combines them safely, ensuring that the user input is always treated as data and never as executable code.

### Secure Code Example

In Python's `sqlite3` library, you use a `?` as a placeholder:

```python
# The SQL query is a template with placeholders.
query = "SELECT * FROM users WHERE username = ? AND password = ?"

# The user input is passed as a separate tuple to the execute function.
# The database driver handles quoting and escaping safely.
cursor.execute(query, (username, password))
```

This approach creates a fundamental separation between code and data, making SQL injection impossible for this query.

## Defense in Depth

While parameterized queries are the primary defense, other measures can add layers of security:
*   **Principle of Least Privilege:** The application's database user should only have the minimum permissions it needs. For example, a user that only needs to read data should not have `WRITE` or `DELETE` permissions.
*   **Web Application Firewall (WAF):** A WAF can be used to block common, obvious SQLi patterns, but it should not be relied upon as the only defense, as attackers can often find ways to bypass them.
