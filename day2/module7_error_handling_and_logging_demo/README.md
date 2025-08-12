# Insecure Error Handling & Logging Demo

This directory contains a simple Flask application that demonstrates the dangers of **information leakage through verbose error messages**, a common and critical vulnerability.

## Real-World Scenario: From Error to Shell

An attacker is probing a website and discovers that when they submit invalid input, the site returns a detailed error page. This page, intended for developers, was accidentally left enabled in production.

1.  **Information Gathering:** The error page leaks the full file path of the application (`/var/www/app/main.py`), the web framework being used (e.g., Flask 1.1), and snippets of the source code. The attacker now knows the exact technology stack and file structure.
2.  **Finding Other Vulnerabilities:** The leaked source code reveals how the application connects to its database, including the structure of a SQL query. The attacker identifies a potential SQL injection vulnerability from this snippet.
3.  **Exploitation:** The attacker uses the information they've gathered to craft a successful SQL injection payload.
4.  **Privilege Escalation:** In some frameworks, debug modes can even expose an **interactive web-based shell**. If this is enabled, the attacker can directly execute commands on the server, leading to a full system compromise.

A single misconfigured error page can give an attacker the entire roadmap they need to take over a server.

## The Flaw: Debug Mode in Production

The key vulnerability is that the application is run with `debug=True`.

The vulnerable code is in the final lines of `app.py`:
```python
if __name__ == '__main__':
    # VULNERABLE: Running with debug=True in a production environment
    # exposes a powerful debugger and leaks sensitive information.
    app.run(debug=True, port=5003)
```

### Anatomy of a Leaky Error

When a Flask application (or many other web frameworks) runs in debug mode, it provides detailed error pages for unhandled exceptions. These are a goldmine for an attacker, leaking:
*   **Source Code:** The exact line of code that failed, along with surrounding lines.
*   **Configuration & Secrets:** The values of all active configuration settings, which can include secret keys, database connection strings, and API credentials.
*   **Environment Details:** Full file paths, library versions, and operating system information.

## How to Exploit

1.  Install Flask: `pip install Flask`
2.  Run the application: `python app.py`
3.  Open your browser to `http://127.0.0.1:5003/`.

4.  Click the link to `/divide?a=10&b=0`. This triggers a `ZeroDivisionError`.
5.  Because the app is in debug mode, you will see the detailed Werkzeug debugger page. **Explore it.** You will see the source code, the value of `app.config['SECRET_KEY']`, and the full stack trace. This is the information leak.

## The Fix: Fail Securely

The fix involves a two-pronged approach: disable debugging in production and implement robust, generic error handling.

### 1. Disable Debug Mode

This is the most critical step. Your production startup script should **never** have `debug=True`.
```python
# SAFE for production
app.run(debug=False)
```
This is typically managed through environment variables or configuration files, not hardcoded.

### 2. Implement Custom, Generic Error Pages

You must show users a generic error page that gives them no useful information for an attack, while logging the full details for your development team.

In Flask, you can use the `@app.errorhandler()` decorator:
```python
@app.errorhandler(500)
def internal_server_error(e):
    # 1. Log the full, detailed error for the development team.
    # The `exc_info=True` part is crucial to include the stack trace.
    app.logger.error(f"Server Error: {e}", exc_info=True)

    # 2. Show the user a generic, unhelpful (to an attacker) error page.
    return "<h1>500 - Internal Server Error</h1><p>Something went wrong on our end. We are looking into it.</p>", 500
```

### 3. Secure Logging Practices

*   **Log to a Secure Location:** Ensure log files are stored with proper permissions so they are not world-readable.
*   **Don't Log Sensitive Data:** Be careful not to log sensitive user data like passwords, credit card numbers, or session tokens unless absolutely necessary and properly secured.
*   **Prevent Log Injection:** Sanitize any user input that is written to logs to prevent an attacker from forging log entries or injecting malicious characters.
