from flask import Flask, render_template, request

app = Flask(__name__)

# Sample user data
users = {
    "user1": {"isAdmin": False},
    "user2": {"isAdmin": True}
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    username = request.args.get('user')
    if not username or username not in users:
        return "User not found", 404

    user = users[username]

    # This is a client-side check, which is an insecure design.
    # A user can simply view the source and see the admin content.
    return render_template('dashboard.html', user=user, username=username)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
