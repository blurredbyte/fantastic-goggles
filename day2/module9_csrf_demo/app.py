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

# --- Templates ---

LOGIN_TEMPLATE = """
<h1>Login</h1>
<form method="post" action="/login">
    <label>Username:</label><input type="text" name="username" value="user1"><br>
    <label>Password:</label><input type="password" name="password" value="password"><br>
    <input type="submit" value="Login">
</form>
"""

# This settings form is VULNERABLE to CSRF
VULNERABLE_SETTINGS_TEMPLATE = """
<h1>Vulnerable Settings Page</h1>
<p>Welcome, {{ session['username'] }}!</p>
<p>Your current email is: {{ users[session['username']]['email'] }}</p>
<form method="post" action="/change-email-vulnerable">
    <label>New Email:</label><input type="email" name="email"><br>
    <input type="submit" value="Change Email">
</form>
<p><a href="/logout">Logout</a></p>
"""

# This settings form is SECURE against CSRF
SECURE_SETTINGS_TEMPLATE = """
<h1>Secure Settings Page</h1>
<p>Welcome, {{ session['username'] }}!</p>
<p>Your current email is: {{ users[session['username']]['email'] }}</p>
<form method="post" action="/change-email-secure">
    <!-- This hidden input adds the CSRF token to the form -->
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
    <label>New Email:</label><input type="email" name="email"><br>
    <input type="submit" value="Change Email">
</form>
<p><a href="/logout">Logout</a></p>
"""

MALICIOUS_PAGE_TEMPLATE = """
<h1>You've Won a Prize!</h1>
<p>Click the button below to claim your prize!</p>
<!-- This form is hosted on an attacker's website. It silently submits a request
     to the vulnerable application. If the user is logged in, their email will be changed. -->
<form id="csrf-form" method="post" action="http://127.0.0.1:5004/change-email-vulnerable">
    <input type="hidden" name="email" value="hacker@example.com">
</form>
<button onclick="document.getElementById('csrf-form').submit();">Claim Prize</button>
<script>
    // In a real attack, this could be submitted automatically without user interaction.
    // For demonstration, we use a button.
    // Example of automatic submission:
    // window.onload = () => { document.getElementById('csrf-form').submit(); };
</script>
"""

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
        return f"""
            <h1>CSRF Demo</h1>
            <p>Welcome, {session['username']}!</p>
            <p><a href="/vulnerable-settings">Go to VULNERABLE Settings Page</a></p>
            <p><a href="/secure-settings">Go to SECURE Settings Page</a></p>
            <p><a href="/malicious-site" target="_blank">Visit the Attacker's Website (open in new tab)</a></p>
        """
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
    return render_template_string(LOGIN_TEMPLATE)

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
    return render_template_string(VULNERABLE_SETTINGS_TEMPLATE, users=users, session=session)

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
    return render_template_string(SECURE_SETTINGS_TEMPLATE, users=users, session=session)

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
    return render_template_string(MALICIOUS_PAGE_TEMPLATE)

# --- Error Handling for CSRF ---
@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return f"CSRF Error: {e.description}", 400

if __name__ == '__main__':
    app.run(debug=True, port=5004)
