# Broken Access Control Demo: Insecure Direct Object Reference (IDOR)

This directory contains a simple Flask application that is vulnerable to **Insecure Direct Object Reference (IDOR)**, one of the most common and impactful types of access control vulnerabilities.

## Real-World Impact

IDOR vulnerabilities are discovered in major applications all the time. They can lead to massive data breaches by allowing attackers to systematically access data they are not authorized to see.

*   **USPS Data Breach (2018):** A vulnerability in the USPS "Informed Visibility" API allowed any authenticated user to query for the account details of any other user simply by changing a user ID in the API request. This exposed the personal data of over 60 million users.
*   **Facebook/Instagram (2013-2019):** Numerous IDOR bugs have been found in Facebook and Instagram over the years, allowing researchers to view private photos, delete content belonging to other users, and access other sensitive information.

The business impact is severe:
*   **Confidentiality Breach:** Attackers can read sensitive data belonging to other users (e.g., messages, financial information, personal details).
*   **Integrity Breach:** In some cases, IDOR can be used to modify or delete other users' data.
*   **Full Account Takeover:** If an IDOR exposes password reset tokens or other sensitive session information, it can lead to full account takeover.

## The Flaw: Missing Authorization Checks

IDOR occurs when an application provides a **direct reference** to an internal object (like a database key or file path) in a URL or API request, and then **fails to verify that the current user is authorized** to access that specific object.

### Vulnerable Code Analysis

In our demo app, a user can view their profile by visiting `/profile/<user_id>`. The `user_id` is a direct reference to a key in our `PROFILES` dictionary.

The vulnerable code in `app.py` is in the `profile` function:
```python
@app.route('/profile/<user_id>')
def profile(user_id):
    # Step 1: The application checks if the profile exists (Authentication).
    if user_id not in PROFILES:
        abort(404)

    # MISSING STEP: The application FAILS to check if the logged-in user
    # is AUTHORIZED to view this specific profile_id.

    # Step 2: The data is fetched and returned to the user.
    profile_data = PROFILES[user_id]
    return render_template_string(...)
```
The code correctly checks if the requested object (`user_id`) is valid, but it completely skips the crucial step of checking if `LOGGED_IN_USER_ID` is the same as the requested `user_id`. This means Alice (user 1) can request Bob's profile (user 2), and the application will happily serve it.

## How to Exploit

1.  Install Flask: `pip install Flask`
2.  Run the application: `python app.py`
3.  Open your browser to `http://127.0.0.1:5002/`.

4.  You are "logged in" as Alice (user ID 1). Click the link to view your profile, which goes to `/profile/1`.
5.  Now, **become the attacker**. Manually change the `1` in the URL to a `2`: `http://127.0.0.1:5002/profile/2`.
6.  You will see Bob's profile, including his secret information. You have successfully performed an IDOR attack.

## The Fix: Centralized and Enforced Authorization

The fix is to **always** perform an authorization check after authenticating the user and before accessing the resource.

The `app.py` file includes a corrected, secure endpoint `/secure_profile/<user_id>` for comparison.

### Secure Code Example
```python
@app.route('/secure_profile/<user_id>')
def secure_profile(user_id):
    # THE FIX: Add an explicit authorization check.
    # Does the ID of the requested resource match the ID of the logged-in user?
    if user_id != LOGGED_IN_USER_ID:
        # If not, deny access with a 403 Forbidden error.
        abort(403)

    # This part remains the same.
    if user_id not in PROFILES:
        abort(404)

    profile_data = PROFILES[user_id]
    return render_template_string(...)
```
By adding this simple check, the vulnerability is eliminated. If you try to navigate to `/secure_profile/2`, the application will correctly return a "403 Forbidden" error.

In a real application, it's best to implement these checks in a centralized way, for example, using decorators or middleware, to ensure they are applied consistently across all relevant endpoints.
