# This file is intended to be scanned by the TruffleHog action in the CI/CD pipeline.
# It contains a hardcoded secret that should be detected.

from flask import Flask, render_template

app = Flask(__name__)

def get_secret_from_aws():
    # This is a fake AWS access key ID, but it has the right format to be
    # detected by secret scanners.
    aws_access_key_id = "AKIAIOSFODNN7EXAMPLE"

    # In a real scenario, this would be a real secret.
    # The TruffleHog scanner in the GitHub Actions workflow should find this
    # and fail the build, preventing this secret from being merged.
    aws_secret_access_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

    return "Attempting to connect to AWS with hardcoded keys..."

@app.route('/')
def index():
    output = get_secret_from_aws()
    return render_template('index.html', output=output)

if __name__ == "__main__":
    app.run(debug=True, port=5000)