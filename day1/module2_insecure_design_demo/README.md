# Insecure Design Demo: Client-Side Access Control

This directory contains a simple Flask application that demonstrates a critical **insecure design flaw**: performing access control checks on the client-side instead of the server-side.

## Real-World Scenario

Imagine an online store where pricing is determined by user type. Regular users see the standard price, while "premium" members see a discounted price. The developers, in a rush to implement this feature, decide to send both prices to the browser and use JavaScript to show the correct one based on a `isPremium` flag.

A savvy but dishonest user could simply inspect the webpage's source code, find the hidden premium price, and manipulate the checkout process to pay the lower price. This is not a "hack" in the traditional sense; it's an exploitation of a fundamental design flaw. The system was **designed** insecurely by trusting the client's browser to enforce a business rule.

## The Flaw: Trusting the Client

The core issue is that **the client (the user's browser) cannot be trusted to enforce security rules.** Any data sent to the client (HTML, CSS, JavaScript) is fully under the user's control. They can view, modify, and manipulate it at will.

In this demo application, we have a dashboard that is supposed to show sensitive admin-only information.

### Code Analysis

The `app.py` file sends the user's `isAdmin` status directly to the browser as a JavaScript variable:

```python
# app.py
@app.route('/dashboard')
def dashboard():
    # ...
    # The user object, including the isAdmin flag, is sent to the template.
    return render_template_string('''...''', user=user, username=username)
```

The template then uses this JavaScript variable to decide what to display:

```html
<!-- The template receives the user data -->
<script>
    function checkAccess() {
        // The isAdmin flag is now a JavaScript variable, controllable by the user.
        var isAdmin = {{ user.isAdmin|tojson }};
        if (isAdmin) {
            document.getElementById('admin-content').style.display = 'block';
        } else {
            document.getElementById('user-content').style.display = 'block';
        }
    }
</script>

<!-- Both regular content and admin content are sent to the browser.
     The admin content is just hidden with CSS. -->
<div id="user-content" style="display:none;">...</div>
<div id="admin-content" style="display:none;">
    <p>Welcome, {{ username }}! You are an admin.</p>
    <p><strong>Admin Secret:</strong> The treasure is buried under the big 'W'.</p>
</div>
```

All the "secret" admin data is sent to every user, and it's simply hidden using CSS. An attacker doesn't need any special tools to find it; they can just right-click and "View Page Source".

## Business Impact

*   **Data Breach:** Sensitive information intended for a privileged group (admins, premium users) is exposed to everyone.
*   **Financial Loss:** As in the e-commerce example, this can lead to direct financial loss.
*   **Reputational Damage:** Users will lose trust in an application that cannot properly protect their data or enforce its own business rules.

## How to Run the Demo

1.  Install Flask:
    ```bash
    pip install Flask
    ```

2.  Run the application:
    ```bash
    python app.py
    ```

3.  Open your browser and navigate to `http://127.0.0.1:5000/dashboard?user=user1` (the non-admin user).

4.  Right-click on the page and select "View Page Source" or "Inspect". You will be able to see the hidden `admin-content` div containing the secret message, even though you are not an admin.

## The Fix: Server-Side Enforcement

The only secure way to implement access control is to **enforce it on the server.** The server should decide what data to send to the client, and the client should only receive the data it is authorized to see.

A secure implementation would look like this:

```python
# A secure version of the dashboard endpoint
@app.route('/secure_dashboard')
def secure_dashboard():
    username = request.args.get('user')
    # ...
    user = users[username]

    # The access control logic is on the SERVER.
    if user['isAdmin']:
        # Only send the admin template to admin users.
        return render_template_string('<h1>Admin Dashboard</h1><p>Secret admin data...</p>')
    else:
        # Send the regular user template to non-admin users.
        return render_template_string('<h1>User Dashboard</h1><p>Welcome, regular user.</p>')
```

In this fixed version, the non-admin user's browser **never receives the admin data.** There is nothing to uncover because the server never sent it in the first place. This is a secure design.
