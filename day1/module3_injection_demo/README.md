# SQL Injection Demo

This directory contains a simple Flask application that is vulnerable to SQL injection.

## The Flaw

The application has a login form that takes a username and password. The server-side code in `app.py` constructs a SQL query by embedding the user input directly into the query string using an f-string. This is a classic SQL injection vulnerability.

The vulnerable code is:
```python
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
cursor.execute(query)
```

Because the input is not sanitized or parameterized, a malicious user can provide specially crafted input to manipulate the SQL query.

## How to Exploit

1.  Install Flask:
    ```bash
    pip install Flask
    ```

2.  Run the application:
    ```bash
    python app.py
    ```

3.  Open your browser and navigate to `http://127.0.0.1:5001/`.

4.  In the login form, enter the following as the username:
    ```
    ' OR 1=1 --
    ```
    You can leave the password field empty or type anything.

5.  Click "Login".

## Why it Works

The input `' OR 1=1 --` modifies the SQL query to become:
```sql
SELECT * FROM users WHERE username = '' OR 1=1 --' AND password = '...'
```

Here's a breakdown of the injected query:
*   `''`: The empty string closes the single quote for the `username`.
*   `OR 1=1`: This is a condition that is always true. The `WHERE` clause becomes `WHERE username = '' OR 1=1`, which will always be true and will match all rows.
*   `--`: This is a comment in SQL. It causes the rest of the original query (the password check) to be ignored.

As a result, the query returns the first user from the `users` table (in this case, the admin), and the application logs you in without a valid password.

## The Fix

To prevent SQL injection, you should always use parameterized queries (also known as prepared statements). In Python's `sqlite3` library, you would do this:

```python
query = "SELECT * FROM users WHERE username = ? AND password = ?"
cursor.execute(query, (username, password))
```

This way, the user input is treated as data, not as part of the SQL command, and the injection attack is prevented.
