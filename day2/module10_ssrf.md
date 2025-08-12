# Module 10: Server-Side Request Forgery (SSRF)

*   Understand and mitigate SSRF attacks.
*   Implement strong defenses against SSRF in modern architectures.

## Practical Demo: Shielding Cloud and Web Apps from SSRF

This module includes a practical demonstration of a Server-Side Request Forgery (SSRF) vulnerability. The code for this demo can be found in the `module10_ssrf_demo` directory. The demo showcases a web application that fetches an image from a URL provided by the user. This functionality is vulnerable to SSRF, allowing an attacker to make the server send requests to internal, private services.
