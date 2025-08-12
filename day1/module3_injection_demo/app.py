import sqlite3
from flask import Flask, request, render_template_string

app = Flask(__name__)
DB_FILE = "users.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS users")
        cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
        cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'password123')")
        cursor.execute("INSERT INTO users (username, password) VALUES ('user', 'password')")
        conn.commit()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # This is the vulnerable part of the code
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            # The query is executed here. A malicious user can inject SQL commands.
            # For example, using a username like: ' OR 1=1 --
            try:
                cursor.execute(query)
                user = cursor.fetchone()
            except sqlite3.Error as e:
                return f"An error occurred: {e}"


        if user:
            return f'<h1>Welcome, {user[1]}!</h1><p>Login successful.</p>'
        else:
            return '<h1>Login Failed</h1><p>Invalid username or password.</p>'

    return '''
        <h1>Login</h1>
        <form method="post">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username"><br><br>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password"><br><br>
            <input type="submit" value="Login">
        </form>
        <p>Try to log in with username: <code>' OR 1=1 --</code> and any password.</p>
    '''

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5001)
