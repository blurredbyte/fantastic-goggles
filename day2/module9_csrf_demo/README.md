# Cross-Site Request Forgery (CSRF) Demo

This directory contains a simple Flask application that demonstrates a Cross-Site Request Forgery (CSRF) vulnerability and how to prevent it using CSRF tokens.

## The Flaw

CSRF is an attack that tricks a user into submitting a malicious request. It inherits the identity and privileges of the victim to perform an undesired function on their behalf. For most sites, browser requests automatically include any credentials associated with the site, such as session cookies. If the user is authenticated to the site, the site cannot distinguish between a forged request and a legitimate one.

The demo application (`app.py`) has two versions of a settings page where a logged-in user can change their email address:
1.  `/vulnerable-settings`: This endpoint is **vulnerable** to CSRF.
2.  `/secure-settings`: This endpoint is **protected** against CSRF.

The vulnerable endpoint `/change-email-vulnerable` does not perform any checks to ensure that the request originated from the application's own form. It only checks if the user is logged in (via the session cookie).

## How to Exploit

1.  **Install Dependencies:**
    This demo uses Flask and Flask-WTF for CSRF protection.
    ```bash
    pip install Flask Flask-WTF
    ```

2.  **Run the Application:**
    ```bash
    python app.py
    ```

3.  **Simulate the Attack:**
    a. Open your browser and go to `http://127.0.0.1:5004/`.
    b. Log in using the default credentials (`user1`, `password`). You are now on the main application.
    c. In a **new tab**, open the "attacker's website" by navigating to `http://127.0.0.1:5004/malicious-site`.
    d. Click the "Claim Prize" button on the attacker's site. This button submits a hidden form that targets the vulnerable endpoint (`/change-email-vulnerable`) of the main application.
    e. Go back to your first tab (the main application) and refresh the page or navigate to the vulnerable settings page. You will see that your email has been changed to `hacker@example.com` without your knowledge or consent. The attack was successful because the browser automatically included your session cookie with the request sent from the malicious page.

## The Fix: CSRF Tokens

The standard way to prevent CSRF is to use a unique, unpredictable token for each request. This is often called a "synchronizer token" or "CSRF token".

1.  When a user visits a page with a form, the server generates a unique token and embeds it as a hidden field in the form.
2.  When the user submits the form, the token is sent back to the server.
3.  The server validates that the token from the form matches the token it expects for that user's session.

If the tokens don't match, the server rejects the request. An attacker cannot guess the correct token, so any forged request from a malicious site will be missing the valid token and will be blocked.

The demo application uses the `Flask-WTF` library to implement this protection.

*   The `/secure-settings` page includes a hidden input with the token:
    ```html
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
    ```
*   The Flask application is configured with `CSRFProtect(app)`, which automatically handles the generation and validation of these tokens for all POST requests.

If you try to point the malicious form's `action` to `/change-email-secure`, the request will fail with a "400 Bad Request (CSRF token missing or invalid)" error, because the attacker's site cannot provide the correct token.
