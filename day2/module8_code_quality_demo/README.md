# Code Quality Demo: Hardcoded Secrets

This directory contains a Python script that demonstrates a common and critical security vulnerability: hardcoding secrets (like API keys and passwords) directly in the source code.

## The Flaw

The script `connect_to_api.py` contains the following lines:

```python
API_KEY = "ak_live_a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6"
DATABASE_PASSWORD = "Password123!"
```

This is a major security risk for several reasons:
*   **Version Control History:** If this code is committed to a version control system like Git, these secrets become part of the permanent history of the repository. Even if you "remove" them in a later commit, they are still accessible in the history.
*   **Improper Access:** Anyone who has read-access to the code repository (which may include many more people than those who need access to the secrets) can see the credentials in plain text.
*   **Difficult to Rotate:** When a secret needs to be changed (e.g., if it's compromised), you have to change it in the code, which requires a new code deployment. This is slow and error-prone.

## How to Detect Hardcoded Secrets

Manually reviewing code for secrets is difficult and unreliable. The best approach is to use automated tools to scan your code for hardcoded credentials. These tools can be integrated into your development workflow and CI/CD pipelines.

A popular open-source tool for this is **TruffleHog**.

### Using TruffleHog

1.  **Install TruffleHog:**
    ```bash
    pip install trufflehog
    ```

2.  **Scan a file:**
    To scan the `connect_to_api.py` file, you would run:
    ```bash
    trufflehog filesystem ./connect_to_api.py
    ```
    TruffleHog will scan the file and report the secrets it finds, identifying them by type (e.g., "High entropy string").

3.  **Scan a Git repository:**
    You can also scan a whole Git repository's history:
    ```bash
    trufflehog git https://github.com/trufflesecurity/test_keys.git
    ```

## The Fix

Secrets should never be stored in code. Instead, they should be loaded at runtime from a secure source. The `connect_to_api.py` script also includes a `connect_securely` function that demonstrates the correct approach.

**Best Practices for Managing Secrets:**

1.  **Environment Variables:** For many applications, especially in containerized environments, loading secrets from environment variables is a good practice.
    ```python
    import os
    api_key = os.getenv("API_KEY")
    ```
    You can then set these environment variables when you run the application.

2.  **Configuration Files:** Store secrets in configuration files (e.g., `.env`, `config.yaml`) that are **excluded** from version control (using `.gitignore`).

3.  **Secrets Management Systems:** For more complex or sensitive applications, use a dedicated secrets management tool like **HashiCorp Vault**, **AWS Secrets Manager**, or **Google Secret Manager**. These tools provide secure storage, fine-grained access control, auditing, and dynamic secret rotation.
