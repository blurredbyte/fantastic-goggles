# Server-Side Request Forgery (SSRF) Demo

This directory contains a Flask application that is vulnerable to **Server-Side Request Forgery (SSRF)**. This is a highly dangerous vulnerability that allows an attacker to force a server to make requests on their behalf, often to internal, privileged resources.

## Real-World Impact: The Capital One Breach (2019)

One of the most famous examples of SSRF is the 2019 Capital One data breach, which affected over 100 million customers. The attacker was able to exploit an SSRF vulnerability in a Web Application Firewall (WAF) to send requests from the WAF server to the internal AWS metadata service.

The AWS metadata service is a special endpoint (`169.254.169.254`) that is only accessible from within an EC2 instance. It provides information about the instance, including temporary security credentials for the IAM role attached to it.

By exploiting the SSRF, the attacker was able to query the metadata service, steal the temporary credentials, and use them to access and exfiltrate massive amounts of customer data from Capital One's S3 buckets. This demonstrates the catastrophic potential of SSRF in a cloud environment.

## The Flaw: Abusing the Server's Trust and Position

The vulnerability exists when an application takes a user-supplied URL and makes a request to it without proper validation. The server, which is often located inside a private network with special privileges, becomes a proxy for the attacker.

### Vulnerable Code Analysis

The demo consists of two applications:
1.  `app.py`: The main, public-facing application that is vulnerable.
2.  `internal_service.py`: A simulated private admin panel that should only be accessible from the server itself.

The vulnerability is in the `/fetch` endpoint of `app.py`:
```python
# app.py
@app.route('/fetch')
def fetch():
    url = request.args.get('url')
    # ...
    try:
        # VULNERABLE: The application blindly trusts and requests the user-provided URL.
        response = requests.get(url, timeout=3)
        content = response.text
    # ...
```
The code takes the `url` parameter and immediately tries to fetch it. There is no validation to check *what* the URL is pointing to. An attacker can abuse this to make the server connect to itself (`localhost`), other servers on the internal network, or special cloud metadata endpoints.

## How to Exploit

1.  **Install Dependencies:** `pip install Flask requests`
2.  **Run the Applications:**
    *   In one terminal, start the internal service: `python internal_service.py`
    *   In a second terminal, start the main application: `python app.py`

3.  **Simulate the Attack:**
    a. Open your browser to the main application at `http://127.0.0.1:5005/`.
    b. In the input box, enter the URL for the **internal admin panel**:
        ```
        http://127.0.0.1:8001/admin
        ```
    c. Click "Fetch Image".
    d. The public-facing server at port 5005 will make a request to the internal service at port 8001. The response from the private admin panel, including the fake API key, will be displayed in your browser. You have successfully used the public server as a proxy to access a protected, internal resource.

## Mitigation Strategies: A Layered Approach

Fixing SSRF requires a multi-layered defense, as simple blocklists are often easy to bypass.

### 1. Primary Defense: Strict Allow-List

*   **What:** The most effective defense is to **only allow connections to a list of known, safe, and required domains.**
*   **Why:** Instead of trying to guess all the "bad" places a user could point to (a blocklist), you define the small set of "good" places the server is allowed to talk to. All other URLs are rejected.
*   **Example:** If your application only needs to fetch images from `images.example.com`, your code should check if the hostname of the user's URL is exactly `images.example.com`.

### 2. Secondary Defense: Validate URL and IP Address

If an allow-list is not feasible, you must perform strict validation:
*   **URL Scheme:** Only allow `http` and `https`. Block all others (`file://`, `dict://`, `gopher://`, etc.).
*   **IP Address Resolution:**
    1.  Resolve the user-provided hostname to an IP address.
    2.  Check if that IP address is a public IP. Reject it if it's a private, loopback, or otherwise reserved IP address (e.g., `127.0.0.1`, `10.x.x.x`, `192.168.x.x`, `169.254.x.x`).
    3.  **Crucially**, make the final request to the *resolved IP address*, not the original hostname. This helps prevent DNS-based bypasses like DNS rebinding.

### 3. Defense in Depth: Network Controls

*   **Egress Firewalling:** Configure firewall rules on the server itself (or the network it's in) to prevent it from making outbound connections to unauthorized locations. For example, a web server should probably never be making connections to the database server of another microservice. You should explicitly block access to cloud metadata endpoints (`169.254.169.254`) unless the server absolutely needs it.
*   **Disable Redirects:** When making the request in your code, disable redirects. An attacker could otherwise provide a URL to a safe, whitelisted domain that then redirects to an internal, malicious one. In Python's `requests` library, this is done with `allow_redirects=False`.
