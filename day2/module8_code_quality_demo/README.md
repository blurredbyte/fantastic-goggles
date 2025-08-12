# Code Quality Demo: Hardcoded Secrets in Source Code

This directory contains a Python script that demonstrates one of the most common and easily preventable security vulnerabilities: **hardcoding secrets** (like API keys, passwords, and tokens) directly in source code.

## Real-World Scenario: The Public GitHub Repo

A developer at a startup is working on a new feature that integrates with a third-party API. To get the code working quickly on their local machine, they hardcode the company's master API key directly into the script. Later, they push the code to a public GitHub repository, forgetting the key is there.

Within minutes, automated scanners run by attackers find the key. The attackers use the key to access the company's account on the third-party service, steal all the customer data stored there, and then delete it. The startup only finds out when their service stops working and customers start complaining. The damage is done, and it all started with one hardcoded secret.

This scenario happens thousands of times every day.

## The Flaw: Secrets as Code

The script `connect_to_api.py` contains the following lines:

```python
# VULNERABLE: Hardcoded secrets
API_KEY = "ak_live_a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6"
DATABASE_PASSWORD = "Password123!"
```

This is a critical flaw for several reasons:

*   **Permanent Git History:** Once a secret is committed to Git, it is in the repository's history **forever**. Even if you "delete" it in a later commit, it's still present in the previous commits. The only way to truly remove it is to rewrite the entire Git history, which is a complex and destructive process.
*   **Overly Broad Access:** Source code is often shared widely within a company, and sometimes publicly. Secrets, however, should only be accessible to the specific people and services that absolutely need them. Storing secrets in code breaks this principle.
*   **Difficult Rotation:** When a secret needs to be changed (a process called "rotation"), you have to find every place it's hardcoded, change the code, and redeploy the entire application. This is slow, error-prone, and discourages good security practices like regular key rotation.

## How to Detect Hardcoded Secrets

Manually reviewing code for secrets is unreliable. You should always use **automated secret scanning tools**. These tools can be run by developers locally before they commit, and they should also be integrated into your CI/CD pipeline to act as a safety net.

A popular open-source tool for this is **TruffleHog**.

### Using TruffleHog

1.  **Install TruffleHog:**
    ```bash
    pip install trufflehog
    ```

2.  **Scan a file:**
    ```bash
    trufflehog filesystem ./connect_to_api.py
    ```
    TruffleHog will scan the file and report the high-entropy strings and other patterns that look like secrets.

3.  **Scan a Git repository's entire history:**
    This is the most powerful feature. TruffleHog can scan every commit in a repository's history to find secrets that were added and later removed.
    ```bash
    # Example scanning a public repo known to have test keys
    trufflehog git https://github.com/trufflesecurity/test_keys.git
    ```

## The Fix: Separate Configuration from Code

The cardinal rule of secrets management is: **Secrets are configuration, not code.** They must be loaded by the application at runtime from a secure external source.

The `connect_to_api.py` script includes a `connect_securely` function that demonstrates this principle.

### Best Practices for Managing Secrets

The right solution depends on your environment, but here are the most common approaches, from simplest to most robust:

1.  **Environment Variables:**
    *   **How it works:** The application reads secrets from environment variables (e.g., `os.getenv("API_KEY")`). The secrets are set in the shell or by the container orchestration system (like Docker or Kubernetes) before the application starts.
    *   **Pros:** Simple, language-agnostic, and works well in many environments.
    *   **Cons:** Can be difficult to manage at scale; secrets can still be exposed in logs or system inspection tools.

2.  **Configuration Files (e.g., `.env` files):**
    *   **How it works:** Secrets are stored in a file (e.g., `prod.env`). This file is **NEVER** committed to Git (it must be listed in `.gitignore`). The application loads this file at startup.
    *   **Pros:** Easy for local development.
    *   **Cons:** Distributing the secret file to production servers securely can be a challenge.

3.  **Dedicated Secrets Management Systems:**
    *   **How it works:** Use a tool designed specifically for this purpose, like **HashiCorp Vault**, **AWS Secrets Manager**, **Google Secret Manager**, or **Azure Key Vault**. The application authenticates to the secrets manager at startup and fetches the secrets it needs.
    *   **Pros:** The most secure option. Provides centralized management, fine-grained access control, auditing, and dynamic secret rotation.
    *   **Cons:** Adds another piece of infrastructure to manage.
