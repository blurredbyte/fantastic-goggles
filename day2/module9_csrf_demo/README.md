# Cross-Site Request Forgery (CSRF) Demo

This directory contains a simple Flask application that demonstrates a **Cross-Site Request Forgery (CSRF)** vulnerability. CSRF is a classic web vulnerability that tricks a logged-in user's browser into sending a malicious request to a trusted site.

## Real-World Scenario: The Unwanted Money Transfer

Imagine you are logged into your online banking website, `mybank.com`. In another browser tab, you open an email and click a link to a funny cat video. The link takes you to `evil-cat-videos.com`.

This malicious site has a hidden form that is automatically submitted by your browser the moment the page loads. The form is designed to look like the "Transfer Funds" form from `mybank.com`. It's pre-filled to transfer $1,000 from your account to the attacker's account.

When the form is submitted, your browser helpfully attaches your session cookie for `mybank.com` to the request. From the bank's perspective, the request looks completely legitimate. It came from your browser, with your session cookie, so it must be you, right? The bank processes the transfer, and you've just lost $1,000 without even knowing it.

This is the essence of CSRF: an attacker forges a request and tricks your browser into sending it with your credentials.

## The Flaw: The Confused Deputy

The "confused deputy" in a CSRF attack is the user's browser. It sees a request being made to `mybank.com` and, without knowing the context, helpfully attaches the cookies for that domain. It cannot distinguish between a request initiated by you on the bank's site and a request initiated by a malicious site in another tab.

Our demo application has a vulnerable endpoint, `/change-email-vulnerable`, that changes a user's email address. It relies solely on the session cookie for authentication and has no way of verifying that the request was intentionally submitted by the user from the application's own settings page.

## How to Exploit

1.  **Install Dependencies:** `pip install Flask Flask-WTF`
2.  **Run the Application:** `python app.py`

3.  **Simulate the Attack (Step-by-Step):**
    a. Open your browser and go to `http://127.0.0.1:5004/`.
    b. **Log in** using the default credentials (`user1`, `password`). You now have a valid session cookie stored in your browser for the `127.0.0.1:5004` domain.
    c. In a **new tab**, visit the attacker's website: `http://127.0.0.1:5004/malicious-site`.
    d. **Click the "Claim Prize" button.** This submits a hidden form on the malicious page. The form's `action` attribute points to the vulnerable endpoint on the main application: `http://127.0.0.1:5004/change-email-vulnerable`.
    e. Your browser sees the request going to `127.0.0.1:5004` and **automatically attaches your session cookie**.
    f. The server receives the request, sees the valid session cookie, and changes your email to `hacker@example.com`.
    g. Go back to your first tab and refresh the page. You'll see the email has been changed. The attack was successful.

## The Fix: The Synchronizer Token Pattern

The standard way to prevent CSRF is to use a **Synchronizer Token** (or CSRF Token). This is a unique, secret, and unpredictable value that the server generates and the client must include with every state-changing request.

Here's how it works:
1.  **Server Generates Token:** When the user visits the settings page, the server generates a random CSRF token, stores it in the user's session, and also embeds it as a hidden field in the form.
2.  **Client Submits Token:** When the user submits the form, the token is sent back to the server as part of the form data.
3.  **Server Verifies Token:** The server compares the token from the form with the token stored in the user's session.
    *   If they **match**, the request is valid and is processed.
    *   If they **do not match** (or the token is missing), the request is rejected.

An attacker on a malicious site cannot guess the correct token, so any forged request they send will be missing the valid token and will be blocked.

### Secure Code Example

The demo uses the `Flask-WTF` library, which automates this process.
*   The secure form includes the hidden token:
    ```html
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
    ```
*   The Flask app is initialized with `CSRFProtect(app)`, which handles the token validation for all POST requests automatically.

## Defense in Depth: SameSite Cookies

A powerful, modern defense against CSRF is the `SameSite` cookie attribute. It tells the browser whether to send cookies with cross-site requests. It has three values:
*   `Strict`: The browser will **never** send the cookie on a cross-site request. This is the most secure option but can break some legitimate functionality (e.g., links from other sites).
*   `Lax`: The browser will send the cookie on top-level navigations (e.g., clicking a link), but not on "unsafe" requests like POST from a form on another site. **This is the default in most modern browsers.**
*   `None`: The browser will always send the cookie. This is required for some cross-site API usage but must be paired with the `Secure` attribute (HTTPS only).

While `SameSite=Lax` provides good default protection, you should still implement CSRF tokens as your primary defense. Not all browsers may enforce `SameSite` policies strictly, and relying on it alone is not sufficient.
