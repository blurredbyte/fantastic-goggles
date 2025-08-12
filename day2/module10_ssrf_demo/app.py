from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# --- Template ---

SSRF_TEMPLATE = """
<h1>Image Fetcher</h1>
<p>Enter the URL of an image to display it.</p>
<form method="get" action="/fetch">
    <input type="text" name="url" size="100" value="https://images.unsplash.com/photo-1518791841217-8f162f1e1131?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=800&q=60">
    <input type="submit" value="Fetch Image">
</form>

<hr>

{% if error %}
    <h2 style="color:red;">Error</h2>
    <p>{{ error }}</p>
{% endif %}

{% if content %}
    <h2>Fetched Content</h2>
    <!-- This is a naive way to display content. It might not render an image
         if the URL points to something else, but it will display the text. -->
    <pre>{{ content }}</pre>
{% endif %}

<h2>Attack Ideas</h2>
<p>Try fetching these URLs:</p>
<ul>
    <li>To access a local file: <code>file:///etc/passwd</code></li>
    <li>To access the internal admin panel (running on port 8001): <code>http://127.0.0.1:8001/admin</code></li>
    <li>To access cloud metadata (on AWS): <code>http://169.254.169.254/latest/meta-data/</code></li>
</ul>
"""

# --- Routes ---

@app.route('/')
def index():
    return render_template_string(SSRF_TEMPLATE)

@app.route('/fetch')
def fetch():
    url = request.args.get('url')
    if not url:
        return render_template_string(SSRF_TEMPLATE, error="URL parameter is missing.")

    # THE VULNERABILITY:
    # The application takes a URL from the user and makes a request to it
    # without any validation. An attacker can provide URLs that point to
    # internal services, local files, or cloud metadata endpoints.
    try:
        response = requests.get(url, timeout=3)
        content = response.text
    except requests.exceptions.RequestException as e:
        return render_template_string(SSRF_TEMPLATE, error=f"Could not fetch URL: {e}")

    return render_template_string(SSRF_TEMPLATE, content=content)


if __name__ == '__main__':
    # This is the main, public-facing application
    app.run(debug=True, port=5005)
