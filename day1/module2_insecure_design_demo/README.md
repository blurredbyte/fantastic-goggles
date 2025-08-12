# Insecure Design Demo

This directory contains a simple Flask application that demonstrates an insecure design flaw.

## The Flaw

The application has a dashboard that is supposed to show different content to admin and non-admin users. However, the access control check is performed on the client-side (in JavaScript) rather than on the server-side. This is a common insecure design flaw.

The `app.py` file passes the user's admin status directly to the template:
```python
return render_template_string('''...''', user=user, username=username)
```
The JavaScript in the template then uses this status to decide what to show:
```javascript
var isAdmin = {{ user.isAdmin|tojson }};
if (isAdmin) {
    document.getElementById('admin-content').style.display = 'block';
} else {
    document.getElementById('user-content').style.display = 'block';
}
```
All the content, including the "admin secret," is sent to the browser, regardless of the user's privileges. A malicious user can simply view the page source or use browser developer tools to inspect the DOM and find the hidden admin content.

## How to Run

1.  Install Flask:
    ```bash
    pip install Flask
    ```

2.  Run the application:
    ```bash
    python app.py
    ```

3.  Open your browser and navigate to:
    *   `http://127.0.0.1:5000/dashboard?user=user1` (non-admin)
    *   `http://127.0.0.1:5000/dashboard?user=user2` (admin)

    Even when you are logged in as `user1`, you can see the admin content by viewing the page source.
