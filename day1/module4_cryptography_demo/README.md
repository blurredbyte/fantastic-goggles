# Cryptography Demo: Secure Password Hashing

This directory contains a Python script that demonstrates the critical difference between weak and strong password hashing techniques.

## Real-World Impact: The LinkedIn Breach

In 2012, LinkedIn suffered a major data breach where attackers stole the credentials of millions of users. The stolen password file was later leaked online. A critical finding from the post-mortem analysis was that the passwords were hashed using **SHA-1 without any salt**.

Because the hashes were unsalted, attackers could use pre-computed "rainbow tables" to instantly find the original password for any common hash. For the remaining hashes, the speed of SHA-1 allowed them to brute-force millions of password guesses per second. This resulted in a massive number of user accounts being compromised, not just on LinkedIn, but on any other site where users had reused the same password.

## The Flaw: Using the Wrong Tool for the Job

Hashing is a one-way function, which is great for passwords. However, not all hashing algorithms are suitable for password storage.

### Weak Hashing: Fast and Unsalted

The `hashing_demo.py` script demonstrates using **MD5**, a fast hashing algorithm.

*   **Problem 1: Speed.** Algorithms like MD5 and SHA-1 were designed to be fast. This is good for file integrity checks, but terrible for passwords. Modern GPUs can compute **billions** of MD5 hashes per second, making it trivial for an attacker to guess common passwords if they steal the hash file.
*   **Problem 2: No Salt.** A "salt" is a unique, random string that is combined with a password *before* hashing. Without a salt, every user with the same password (e.g., "Password123") will have the exact same hash in the database. This allows attackers to use rainbow tables to crack many passwords at once.

```python
# hashing_demo.py - WEAK
def weak_hash_password(password):
    # MD5 is too fast and produces the same output for the same input.
    return hashlib.md5(password.encode()).hexdigest()
```

### Strong Hashing: Slow, Salted, and Adaptive

The best practice is to use an algorithm specifically designed for password hashing. This demo uses **bcrypt**.

*   **Slow by Design:** bcrypt has a configurable "work factor" (or cost) that allows you to tune how slow it is. This makes brute-force attacks much more expensive and time-consuming for an attacker.
*   **Automatic Salting:** bcrypt automatically generates a unique salt for every password and stores it as part of the final hash string. You don't have to manage the salt yourself.
*   **Adaptive:** As computers get faster, you can increase the work factor to maintain the same level of security without changing the algorithm.

```python
# hashing_demo.py - STRONG
def strong_hash_password(password):
    # bcrypt handles salt generation automatically.
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)
```

## Understanding a bcrypt Hash

When you generate a hash with bcrypt, you get a string that looks like this:
`$2b$12$D9.o6BigeW4O4s.y2fThzO.3T9G2d3c.E4Z.E6f2g3h4i5j6k7l8m`

This string contains all the information needed to verify a password:
*   `$2b$`: The bcrypt algorithm version.
*   `$12$`: The "cost factor" (in this case, 2^12 rounds of hashing).
*   `D9.o6BigeW4O4s.y2fThzO`: This is the 22-character salt, stored right inside the hash.
*   `.3T9G2d3c.E4Z.E6f2g3h4i5j6k7l8m`: This is the actual hashed result of the password and salt.

When you use `bcrypt.checkpw(password, hash)`, the library automatically extracts the salt and cost factor from the hash string and uses them to correctly re-hash the provided password for comparison.

## How to Run the Demo

1.  Install the `bcrypt` library:
    ```bash
    pip install bcrypt
    ```

2.  Run the script:
    ```bash
    python hashing_demo.py
    ```

Observe the output. You'll see that the MD5 hash for the same password is always identical. The bcrypt hash, however, is different every time you run the script because a new random salt is generated for each hash. This is the power of proper password hashing.
