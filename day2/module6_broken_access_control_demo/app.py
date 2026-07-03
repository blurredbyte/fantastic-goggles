from flask import Flask, render_template, request, abort

app = Flask(__name__)

# In-memory database of user profiles
PROFILES = {
    '1': {'name': 'Alice', 'email': 'alice@example.com', 'secret': 'Alice\'s secret is safe.'},
    '2': {'name': 'Bob', 'email': 'bob@example.com', 'secret': 'Bob\'s secret is also safe.'},
    '3': {'name': 'Charlie', 'email': 'charlie@example.com', 'secret': 'Charlie\'s secret is... well, you get the idea.'}
}

# For the demo, we'll simulate a logged-in user. In a real app, this would come from a session.
LOGGED_IN_USER_ID = '1'

@app.route('/')
def index():
    return render_template('index.html', user_id=LOGGED_IN_USER_ID)

@app.route('/profile/<user_id>')
def profile(user_id):
    # THE VULNERABILITY:
    # The application checks if the profile exists, but it does NOT check
    # if the logged-in user is AUTHORIZED to view the requested profile.
    if user_id not in PROFILES:
        abort(404)

    profile_data = PROFILES[user_id]

    return render_template('profile.html', profile=profile_data, is_secure=False)

# A fixed version of the profile route for comparison
@app.route('/secure_profile/<user_id>')
def secure_profile(user_id):
    # THE FIX:
    # Check if the requested user_id is the same as the logged-in user's ID.
    if user_id != LOGGED_IN_USER_ID:
        abort(403) # 403 Forbidden

    if user_id not in PROFILES:
        abort(404)

    profile_data = PROFILES[user_id]

    return render_template('profile.html', profile=profile_data, is_secure=True)

if __name__ == '__main__':
    app.run(debug=True, port=5002)
