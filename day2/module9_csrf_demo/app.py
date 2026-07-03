from flask import Flask, request, render_template_string, session, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect, CSRFError
import os

app = Flask(__name__)
# In a real app, use a long, random, secret key
app.config['SECRET_KEY'] = os.urandom(24)
# Set the WTF_CSRF_SECRET_KEY as well for Flask-WTF
app.config['WTF_CSRF_SECRET_KEY'] = os.urandom(24)

# Initialize CSRF protection
csrf = CSRFProtect(app)

# --- In-memory user data ---
users = {
    "user1": {"email": "user1@example.com", "password": "password"}
}
# In-memory session data
sessions = {}

# --- Routes ---

@app.before_request
def check_session():
    # Simple session management for the demo
    session_id = request.cookies.get('session_id')
    if session_id and session_id in sessions:
        session.update(sessions[session_id])
    else:
        session.clear()

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            session_id = os.urandom(16).hex()
            sessions[session_id] = {'username': username}
            resp = redirect(url_for('index'))
            resp.set_cookie('session_id', session_id)
            return resp
        else:
            flash("Invalid credentials")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session_id = request.cookies.get('session_id')
    if session_id in sessions:
        del sessions[session_id]
    resp = redirect(url_for('login'))
    resp.delete_cookie('session_id')
    return resp

# --- Vulnerable Endpoint ---
@app.route('/vulnerable-settings')
def vulnerable_settings():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('vulnerable_settings.html', users=users, session=session)

@app.route('/change-email-vulnerable', methods=['POST'])
def change_email_vulnerable():
    if 'username' not in session:
        return "Not logged in", 403

    new_email = request.form.get('email')
    if new_email:
        users[session['username']]['email'] = new_email
        flash(f"VULNERABLE: Email changed to {new_email}")
    return redirect(url_for('vulnerable_settings'))

# --- Secure Endpoint ---
@app.route('/secure-settings')
def secure_settings():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('secure_settings.html', users=users, session=session)

@app.route('/change-email-secure', methods=['POST'])
def change_email_secure():
    if 'username' not in session:
        return "Not logged in", 403

    new_email = request.form.get('email')
    if new_email:
        users[session['username']]['email'] = new_email
        flash(f"SECURE: Email changed to {new_email}")
    return redirect(url_for('secure_settings'))

# --- Attacker's Site ---
@app.route('/malicious-site')
def malicious_site():
    return render_template('malicious_site.html')

# --- Error Handling for CSRF ---
@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return f"CSRF Error: {e.description}", 400

if __name__ == '__main__':
    app.run(debug=True, port=5004)
