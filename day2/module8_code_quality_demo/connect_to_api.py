import os

# This is a VULNERABLE practice.
# Hardcoding secrets directly in the source code is a major security risk.
# If this code is checked into a version control system like Git, the secret
# will be part of the commit history, even if it's removed later.
# Anyone with access to the repository can find it.

API_KEY = "ak_live_a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6" # Example hardcoded API key
DATABASE_PASSWORD = "Password123!" # Example hardcoded password


def connect_to_external_api():
    print("Connecting to external API...")
    print(f"Using API Key: {API_KEY}")
    # In a real application, you would use this key to make an API request.
    print("Connection successful (simulated).")

def connect_to_database():
    print("\nConnecting to database...")
    print(f"Using Password: {DATABASE_PASSWORD}")
    # In a real application, you would use this password to connect to a database.
    print("Connection successful (simulated).")


# --- A BETTER WAY ---
# Secrets should be loaded from the environment or a secure secrets management system.

def connect_securely():
    print("\n--- Secure Connection Method ---")

    # Load secrets from environment variables
    api_key_from_env = os.getenv("API_KEY")
    db_password_from_env = os.getenv("DB_PASSWORD")

    if not api_key_from_env or not db_password_from_env:
        print("Error: API_KEY and DB_PASSWORD environment variables must be set.")
        return

    print("Connecting securely...")
    print("Using API Key from environment.")
    print("Using Password from environment.")
    print("Connection successful (simulated).")


if __name__ == "__main__":
    print("--- Insecure Connection Method ---")
    connect_to_external_api()
    connect_to_database()

    connect_securely()
