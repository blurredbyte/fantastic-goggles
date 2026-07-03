import os
from flask import Flask, render_template

app = Flask(__name__)

# This is a VULNERABLE practice.
# Hardcoding secrets directly in the source code is a major security risk.
API_KEY = "ak_live_a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6" # Example hardcoded API key
DATABASE_PASSWORD = "Password123!" # Example hardcoded password

def connect_to_external_api():
    output = []
    output.append("Connecting to external API...")
    output.append(f"Using API Key: {API_KEY}")
    output.append("Connection successful (simulated).")
    return output

def connect_to_database():
    output = []
    output.append("Connecting to database...")
    output.append(f"Using Password: {DATABASE_PASSWORD}")
    output.append("Connection successful (simulated).")
    return output

def connect_securely():
    output = []

    # Load secrets from environment variables
    api_key_from_env = os.getenv("API_KEY")
    db_password_from_env = os.getenv("DB_PASSWORD")

    if not api_key_from_env or not db_password_from_env:
        output.append("Error: API_KEY and DB_PASSWORD environment variables must be set.")
        return output

    output.append("Connecting securely...")
    output.append("Using API Key from environment.")
    output.append("Using Password from environment.")
    output.append("Connection successful (simulated).")
    return output

@app.route('/')
def index():
    insecure_output = connect_to_external_api() + [""] + connect_to_database()
    secure_output = connect_securely()

    return render_template('index.html', insecure_output=insecure_output, secure_output=secure_output)

if __name__ == "__main__":
    app.run(debug=True, port=5000)