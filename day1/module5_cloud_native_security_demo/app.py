from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    # This is just an example. In a real app, you would use this password
    # to connect to a database.
    db_password = os.environ.get('DB_PASSWORD')
    return f"Hello, World! The DB password is (supposedly a secret): {db_password}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
