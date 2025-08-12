# Server-Side Request Forgery (SSRF) Demo

This directory contains a Flask application that is vulnerable to Server-Side Request Forgery (SSRF).

## The Flaw

SSRF is a vulnerability that allows an attacker to induce the server-side application to make HTTP requests to an arbitrary domain of the attacker's choosing. In modern applications, this is especially dangerous as it can be used to pivot into the internal cloud infrastructure.

The demo consists of two applications:
1.  `app.py`: The main, public-facing application that is vulnerable. It runs on port 5005.
2.  `internal_service.py`: A simulated private admin panel that should only be accessible from the server itself. It runs on port 8001.

The vulnerability exists in the `/fetch` endpoint of `app.py`. This endpoint takes a `url` parameter from the user and makes a `GET` request to that URL to fetch its content.

The vulnerable code is:
```python
@app.route('/fetch')
def fetch():
    url = request.args.get('url')
    # ...
    try:
        # The application blindly trusts and requests the user-provided URL.
        response = requests.get(url, timeout=3)
        content = response.text
    # ...
```
There is no validation to ensure that the URL is a safe, public address. An attacker can abuse this to make the server send requests to internal resources.

## How to Exploit

1.  **Install Dependencies:**
    ```bash
    pip install Flask requests
    ```

2.  **Run the Applications:**
    You need to run both the main app and the internal service.

    *   In one terminal, start the internal service:
        ```bash
        python internal_service.py
        ```
    *   In a **second terminal**, start the main, vulnerable application:
        ```bash
        python app.py
        ```

3.  **Simulate the Attack:**
    a. Open your browser and go to the main application at `http://127.0.0.1:5005/`.
    b. The page has a form to fetch an image. You can try it with a legitimate image URL to see how it's supposed to work.
    c. Now, use the form to perform an SSRF attack. Enter the following URL into the input box and click "Fetch Image":
        ```
        http://127.0.0.1:8001/admin
        ```
    d. The server will make a request to its own local `internal_service` on port 8001. The response from the private admin panel, including the "sensitive" API key, will be displayed in your browser. The attacker has successfully accessed an internal service by using the public-facing application as a proxy.

## Mitigation Strategies

Fixing SSRF requires a combination of techniques, primarily centered around strict validation of user-provided URLs.

1.  **Use an Allow-List:**
    *   The most effective defense is to maintain an allow-list of trusted domains, IP addresses, and ports that the application is allowed to connect to. If the user-provided URL does not match an entry in the allow-list, the request should be rejected.

2.  **Validate URL Scheme:**
    *   Only allow safe schemes like `http` and `https`. Block dangerous schemes like `file://`, `ftp://`, `gopher://`, `dict://`, etc.

3.  **Validate IP Address:**
    *   After resolving the hostname to an IP address, check if the IP is a private, reserved, or loopback address (e.g., `127.0.0.1`, `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`). If it is, block the request.
    *   Be careful of DNS rebinding attacks. The application should resolve the domain to an IP and check it, and then use that *same IP address* for the actual request, not the original domain name.

4.  **Disable Redirects:**
    *   When making the request, disable redirects. An attacker could otherwise point to a safe domain that redirects to a malicious or internal one. In Python's `requests` library, this is done with `allow_redirects=False`.

5.  **Network-Level Controls:**
    *   Use firewall rules to prevent the server from initiating connections to internal services that it doesn't need to access. This is a crucial defense-in-depth measure, especially in cloud environments.
