import hashlib
import bcrypt
import os

def weak_hash_password(password):
    """
    Hashes a password using a weak algorithm (MD5) without a salt.
    This is NOT secure and should never be used.
    """
    return hashlib.md5(password.encode()).hexdigest()

def strong_hash_password(password):
    """
    Hashes a password using a strong, modern algorithm (bcrypt) with a salt.
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)

def check_password_strong(password, hashed_password):
    """
    Checks a password against a hash created with bcrypt.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)

if __name__ == "__main__":
    password = "mySuperSecretPassword123"

    print("--- Weak Hashing (MD5 without salt) ---")
    hashed_weak = weak_hash_password(password)
    print(f"Password: {password}")
    print(f"Weakly hashed: {hashed_weak}")
    # With MD5, the same password always produces the same hash.
    # This makes it vulnerable to rainbow table attacks.
    print(f"Hashing the same password again: {weak_hash_password(password)}")
    print("\n")

    print("--- Strong Hashing (bcrypt with salt) ---")
    hashed_strong = strong_hash_password(password)
    print(f"Password: {password}")
    print(f"Strongly hashed: {hashed_strong}")
    # With bcrypt, the salt is included in the hash, and it's different every time.
    print(f"Hashing the same password again: {strong_hash_password(password)}")

    # Checking the password
    is_correct = check_password_strong(password, hashed_strong)
    print(f"\nIs '{password}' the correct password? {is_correct}")

    is_correct = check_password_strong("wrongPassword", hashed_strong)
    print(f"Is 'wrongPassword' the correct password? {is_correct}")
