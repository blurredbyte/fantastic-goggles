# Broken Access Control (IDOR) Demo

This directory contains a simple Flask application that is vulnerable to Insecure Direct Object Reference (IDOR), a common type of broken access control.

## The Flaw

The application allows a user to view their profile by visiting a URL like `/profile/<user_id>`. For this demo, we simulate being logged in as user `1` (Alice).

The vulnerability lies in the `/profile/<user_id>` endpoint. The code in `app.py` checks if a profile with the given `user_id` exists, but it **fails to check if the currently logged-in user is authorized to view that profile.**

The vulnerable code is:
```python
@app.route('/profile/<user_id>')
def profile(user_id):
    # It only checks if the profile exists...
    if user_id not in PROFILES:
        abort(404)
    # ...but not if the logged-in user is the owner of the profile.
    profile_data = PROFILES[user_id]
    return render_template_string(...)
```

This means that any authenticated user (like Alice) can view the profile and secrets of any other user (like Bob or Charlie) simply by changing the `user_id` in the URL.

## How to Exploit

1.  Install Flask:
    ```bash
    pip install Flask
    ```

2.  Run the application:
    ```bash
    python app.py
    ```

3.  Open your browser and navigate to `http://127.0.0.1:5002/`.

4.  You are "logged in" as Alice (user ID 1). Click the link to view your profile, which goes to `/profile/1`.

5.  Now, manually change the URL in your browser to `http://127.0.0.1:5002/profile/2`.

6.  You will see Bob's profile, including his secret, even though you are not Bob. This is a successful IDOR attack.

## The Fix

To prevent this vulnerability, the application must verify not only that the object exists, but also that the current user has permission to access it.

The `app.py` file includes a corrected, secure endpoint `/secure_profile/<user_id>` for comparison.

The fixed code includes a crucial authorization check:
```python
@app.route('/secure_profile/<user_id>')
def secure_profile(user_id):
    # THE FIX: Check if the requested user_id matches the logged-in user's ID.
    if user_id != LOGGED_IN_USER_ID:
        abort(403) # Return a 403 Forbidden error

    if user_id not in PROFILES:
        abort(404)

    profile_data = PROFILES[user_id]
    return render_template_string(...)
```

This ensures that users can only access their own profiles. If you try to navigate to `http://127.0.0.1:5002/secure_profile/2`, the application will correctly return a "403 Forbidden" error.
