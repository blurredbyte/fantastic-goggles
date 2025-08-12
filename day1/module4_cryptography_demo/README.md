# Cryptography Demo: Password Hashing

This directory contains a Python script that demonstrates the difference between weak and strong password hashing techniques.

## The Concept

Storing user passwords securely is a critical part of application security. You should never store passwords in plaintext. Hashing is the standard approach, but not all hashing methods are equal.

### Weak Hashing

*   **Algorithm:** Using an old, fast hashing algorithm like MD5 or SHA-1 is insecure for passwords. These algorithms were not designed for password hashing and are too fast, making them susceptible to brute-force attacks.
*   **No Salt:** A "salt" is a random string that is added to the password before hashing. Without a salt, the same password will always produce the same hash. This makes the system vulnerable to "rainbow table" attacks, where an attacker can pre-compute hashes for common passwords and quickly find matches.

The `hashing_demo.py` script shows an example of weak hashing using `MD5` without a salt.

### Strong Hashing

*   **Algorithm:** Use a modern, slow, and adaptive hashing algorithm designed specifically for passwords. Examples include `bcrypt`, `scrypt`, `Argon2`, and `PBKDF2`. These algorithms are computationally intensive, which slows down brute-force attacks.
*   **Salting:** A unique, random salt should be generated for each user and stored with their hashed password. This ensures that even if two users have the same password, their hashes will be different. Modern password hashing libraries like `bcrypt` handle salt generation automatically.

The `hashing_demo.py` script shows how to use the `bcrypt` library to hash passwords securely.

## How to Run

1.  Install the `bcrypt` library:
    ```bash
    pip install bcrypt
    ```

2.  Run the script:
    ```bash
    python hashing_demo.py
    ```

The script will output the results of both weak and strong hashing for the same password, highlighting the differences. You'll notice that the weak hash is always the same, while the strong `bcrypt` hash is different each time you run it (due to the random salt). However, the `check_password_strong` function will still correctly verify the password against any of the generated hashes for it.
