from flask import Flask, render_template_string, request

app = Flask(__name__)

# Sample user data
users = {
    "user1": {"isAdmin": False},
    "user2": {"isAdmin": True}
}

@app.route('/')
def index():
    return '<h1>Insecure Design Demo</h1><p>Try to access the <a href="/dashboard?user=user1">dashboard</a> as user1 (not an admin) and <a href="/dashboard?user=user2">dashboard</a> as user2 (an admin).</p>'

@app.route('/dashboard')
def dashboard():
    username = request.args.get('user')
    if not username or username not in users:
        return "User not found", 404

    user = users[username]

    # This is a client-side check, which is an insecure design.
    # A user can simply view the source and see the admin content.
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Dashboard</title>
            <script>
                function checkAccess() {
                    var isAdmin = {{ user.isAdmin|tojson }};
                    if (isAdmin) {
                        document.getElementById('admin-content').style.display = 'block';
                    } else {
                        document.getElementById('user-content').style.display = 'block';
                    }
                }
            </script>
        </head>
        <body onload="checkAccess()">
            <h1>Dashboard</h1>
            <div id="user-content" style="display:none;">
                <p>Welcome, {{ username }}! You are a regular user.</p>
            </div>
            <div id="admin-content" style="display:none;">
                <p>Welcome, {{ username }}! You are an admin.</p>
                <p><strong>Admin Secret:</strong> The treasure is buried under the big 'W'.</p>
            </div>
        </body>
        </html>
    ''', user=user, username=username)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
