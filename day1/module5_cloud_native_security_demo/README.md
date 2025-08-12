# Cloud-Native Security Demo: Insecure Dockerfile

This directory contains an example of an insecure `Dockerfile` that highlights several common security misconfigurations. Container images are a foundational layer of modern cloud applications, and an insecure base can undermine the security of the entire system.

## Real-World Scenario: The Leaky Container

Imagine a startup deploys a new microservice using a container built from a `Dockerfile` similar to the one in this demo.
1.  An attacker discovers a vulnerability in the application code (e.g., Remote Code Execution).
2.  Because the container is running as the **root user**, the attacker gains root privileges inside the container after exploiting the bug.
3.  As root, they can access all files, including the application's source code. They find a **hardcoded AWS key** in an environment variable.
4.  The AWS key belongs to a user with overly broad permissions. The attacker uses this key to access the company's S3 buckets, steal customer data, and then launch a ransomware attack by encrypting the data and deleting the originals.

This entire disaster could have been mitigated or even prevented by building a more secure container image.

## Insecure Dockerfile Analysis

The `Dockerfile` in this directory has several vulnerabilities. We will analyze them one by one. A fixed version, `Dockerfile.fixed`, is included for comparison.

---

### 1. Vague and Outdated Base Image

*   **Vulnerability:** `FROM python:3.8`
*   **Risk:** Using a vague tag like `:3.8` means you could get a different version of the image every time you build, leading to inconsistent behavior. More importantly, the `python:3.8` image is a full OS installation with many tools (compilers, package managers, shells) that are not needed to run the application, increasing the attack surface. It may also contain unpatched OS-level vulnerabilities.
*   **Fix:** Use a specific, minimal base image like `python:3.8.13-slim-buster`. This reduces the image size, decreases the attack surface, and ensures reproducible builds.

---

### 2. Hardcoded Secrets

*   **Vulnerability:** `ENV DB_PASSWORD="supersecretpassword123"`
*   **Risk:** This is one of the most common and dangerous practices. The secret is embedded directly into the container image layer. Anyone who can pull the image (e.g., any developer, a CI/CD system) can inspect its layers and find the secret in plain text using `docker history` or `docker inspect`.
*   **Fix:** Never store secrets in the Dockerfile. Use a runtime injection mechanism like Kubernetes Secrets, Docker Secrets, or a dedicated secrets manager like HashiCorp Vault. These tools mount secrets into the container at runtime, either as files or environment variables, without ever baking them into the image.

---

### 3. Running as the Root User

*   **Vulnerability:** The `Dockerfile` does not specify a `USER`, so the container will run as `root` by default.
*   **Risk:** This is a critical security failure. If an attacker finds a vulnerability in your application (e.g., RCE, Path Traversal), they will gain `root` access inside the container. This gives them full control to install malware, attack other services on the network, and access any sensitive files mounted into the container.
*   **Fix:** Create a dedicated, non-root user in the Dockerfile and switch to it before running the application.
    ```Dockerfile
    RUN addgroup -S appgroup && adduser -S appuser -G appgroup
    USER appuser
    ```

---

### 4. Insecure Package Installation

*   **Vulnerability:** `RUN pip install --no-cache-dir flask`
*   **Risk:** The command does not pin the version of `flask`. This means a new build could pull in a newer version of the library with breaking changes or even a new vulnerability.
*   **Fix:** Use a `requirements.txt` file with fully pinned versions for all your dependencies (e.g., `Flask==2.0.1`). This ensures your builds are reproducible and that you are using known, vetted versions of your libraries.

## How to Analyze Automatically

Manually reviewing Dockerfiles is error-prone. You can use static analysis tools like **hadolint** to automatically check your `Dockerfile` for common security issues and bad practices.

```bash
# Install hadolint (e.g., on macOS via Homebrew)
brew install hadolint

# Run hadolint on the insecure Dockerfile
hadolint Dockerfile
```
This will produce a report detailing the issues found in the file, often with links to best practices.
