from flask import Flask, request, render_template
import requests

app = Flask(__name__)

# --- Routes ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch')
def fetch():
    url = request.args.get('url')
    if not url:
        return render_template('index.html', error="URL parameter is missing.")

    # THE VULNERABILITY:
    # The application takes a URL from the user and makes a request to it
    # without any validation. An attacker can provide URLs that point to
    # internal services, local files, or cloud metadata endpoints.
    try:
        response = requests.get(url, timeout=3)
        content = response.text
    except requests.exceptions.RequestException as e:
        return render_template('index.html', error=f"Could not fetch URL: {e}")

    return render_template('index.html', content=content)


if __name__ == '__main__':
    # This is the main, public-facing application
    app.run(debug=True, port=5005)
