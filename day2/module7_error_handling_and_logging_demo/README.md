# Insecure Error Handling & Logging Demo

This directory contains a simple Flask application that demonstrates the dangers of improper error handling, specifically leaking sensitive information through debug error pages.

## The Flaw

The application `app.py` is a simple web server that has a route for dividing two numbers. The key vulnerability is that the application is run with `debug=True`.

The vulnerable code is in the final lines of `app.py`:
```python
if __name__ == '__main__':
    # NEVER run with debug=True in production!
    app.run(debug=True, port=5003)
```

When a Flask application (or many other web frameworks) is run in debug mode, it provides detailed error pages for unhandled exceptions. These pages are incredibly useful for developers during development, but they are a massive security risk if exposed to users in a production environment.

These debug pages can leak:
*   **Source code:** Snippets of the code that caused the error.
*   **Configuration values:** Sensitive information like secret keys, database credentials, etc.
*   **Environment details:** Full file paths, library versions, and other system information.
*   **Interactive Debugger:** Some frameworks provide an interactive console that allows executing arbitrary code on the server.

## How to Exploit

1.  Install Flask:
    ```bash
    pip install Flask
    ```

2.  Run the application:
    ```bash
    python app.py
    ```

3.  Open your browser and navigate to `http://127.0.0.1:5003/`.

4.  Click the link to `/divide?a=10&b=0` or navigate there directly. This will cause the application to attempt to divide by zero, which raises a `ZeroDivisionError`.

5.  Because the app is in debug mode, you will see a detailed Werkzeug debugger page. Explore this page. You will be able to see the full source code, the values of local variables, and other sensitive information. This information is a goldmine for an attacker.

## The Fix

The fix is multi-layered:

1.  **Disable Debug Mode in Production:** The most important step is to **never** run a production application with `debug=True`. Set it to `False`.

2.  **Implement Custom Error Pages:** Instead of relying on the server's default error pages, create your own generic error pages that do not reveal any internal details. In Flask, you can use the `@app.errorhandler()` decorator:
    ```python
    @app.errorhandler(500)
    def internal_server_error(e):
        # Log the detailed error for developers to see
        app.logger.error(f"Server Error: {e}", exc_info=True)
        # Show a generic error page to the user
        return "<h1>500 - Internal Server Error</h1><p>Something went wrong. We're looking into it.</p>", 500
    ```

3.  **Secure Logging:** As shown in the custom error handler above, detailed error information (like the stack trace) should be logged securely on the server-side where only authorized personnel can access it. It should never be sent to the user's browser. Logs should also be sanitized to prevent log injection attacks.
