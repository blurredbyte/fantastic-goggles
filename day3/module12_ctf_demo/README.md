# CTF Challenge: Secure Code Review

Welcome to the final challenge! Your mission is to perform a secure code review of the included Flask application (`ctf_app.py`) and identify its security vulnerabilities.

## Objective

Find and document all the security flaws in the `ctf_app.py` application. For each vulnerability, you should provide:
1.  **Vulnerability Name:** What is the type of vulnerability? (e.g., SQL Injection, IDOR, etc.)
2.  **Location:** Which part of the code is vulnerable? (e.g., function name, line number).
3.  **Description:** Explain how the vulnerability works and what an attacker could do by exploiting it.
4.  **Recommendation:** How would you fix the vulnerability? Provide a brief description of the fix or a corrected code snippet.

## How to Run the Application

1.  **Install Dependencies:**
    ```bash
    pip install Flask
    ```

2.  **Run the App:**
    ```bash
    python ctf_app.py
    ```
    The application will be running at `http://127.0.0.1:5006/`.

## The Application

The application is a simple e-commerce backend with a few features:
*   A product search page.
*   An invoice viewing page.
*   It simulates being logged in as `user_id = 1`.

## The Challenge

There are **at least 3 major vulnerabilities** hidden in the code. Your job is to find them by reading the source code of `ctf_app.py`. You can also run the application and interact with it to help confirm your findings.

Good luck, and happy hacking!
