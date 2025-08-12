from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Internal Service</h1><p>This service is not supposed to be public.</p>"

@app.route('/admin')
def admin():
    return "<h1>PRIVATE ADMIN PANEL</h1><p>This page contains sensitive information.</p><p>Admin API Key: adm_sk_1234567890abcdef</p>"

if __name__ == '__main__':
    # This service runs on a different port and should only be accessible
    # from the local machine (or the internal network).
    print("Starting internal service on port 8001...")
    app.run(port=8001)
