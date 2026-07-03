import hashlib
import bcrypt
from flask import Flask, render_template, request

app = Flask(__name__)

def weak_hash_password(password):
    """
    Hashes a password using a weak algorithm (MD5) without a salt.
    This is NOT secure and should never be used.
    """
    return hashlib.md5(password.encode()).hexdigest()

def strong_hash_password(password):
    """
    Hashes a password using a strong, modern algorithm (bcrypt) with a salt.
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        password = request.form['password']
        hashed_weak = weak_hash_password(password)
        hashed_strong = strong_hash_password(password)
        return render_template('index.html', password=password, hashed_weak=hashed_weak, hashed_strong=hashed_strong)

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, port=5000)