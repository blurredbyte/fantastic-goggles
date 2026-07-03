from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Internal Service</h1><p>This service is not supposed to be public.</p>"

@app.route('/admin')
def admin():
    return render_template('admin.html', api_key="adm_sk_1234567890abcdef")

if __name__ == '__main__':
    # This service runs on a different port and should only be accessible
    # from the local machine (or the internal network).
    print("Starting internal service on port 8001...")
    app.run(port=8001)
