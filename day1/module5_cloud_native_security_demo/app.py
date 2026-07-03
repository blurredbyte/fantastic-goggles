from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def hello():
    # This is just an example. In a real app, you would use this password
    # to connect to a database.
    db_password = os.environ.get('DB_PASSWORD', 'Not set')
    return render_template('index.html', db_password=db_password)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
