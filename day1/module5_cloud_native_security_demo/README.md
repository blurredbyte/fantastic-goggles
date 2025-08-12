# Cloud-Native Security Demo: Insecure Dockerfile

This directory contains an example of an insecure `Dockerfile` that highlights several common security misconfigurations.

## The Insecure Dockerfile

The `Dockerfile` in this directory has the following vulnerabilities:

1.  **Using a vague and outdated base image (`FROM python:3.8`)**:
    *   **Problem**: Using a vague tag like `:3.8` instead of a specific version like `:3.8.12-slim-buster` can lead to inconsistent builds. More importantly, this base image may contain unpatched vulnerabilities. The full (non-slim) version also includes many unnecessary tools and libraries, increasing the attack surface.
    *   **Fix**: Use a specific, minimal base image (like `slim` or `alpine`) and regularly update it to patch vulnerabilities.

2.  **Hardcoding secrets (`ENV DB_PASSWORD="..."`)**:
    *   **Problem**: Secrets like passwords and API keys should never be hardcoded in a `Dockerfile`. They become part of the image layer, can be seen with `docker history`, and are easily exposed.
    *   **Fix**: Use build-time arguments with a `.dockerignore` file for build-time secrets, or use a secrets management tool (like Docker secrets, Kubernetes secrets, or HashiCorp Vault) to inject secrets at runtime.

3.  **Insecure package installation**:
    *   **Problem**: The `pip install` command doesn't pin package versions. This can lead to unpredictable behavior if a dependency releases a breaking change.
    *   **Fix**: Use a `requirements.txt` file with pinned versions (e.g., `Flask==2.0.1`) to ensure reproducible builds.

4.  **Running as the `root` user (the default)**:
    *   **Problem**: This is one of the most critical container security issues. If an attacker compromises the application running in the container, they gain `root` access inside the container, which gives them extensive capabilities.
    *   **Fix**: Create a non-root user and switch to it in the `Dockerfile`.
        ```Dockerfile
        RUN addgroup -S appgroup && adduser -S appuser -G appgroup
        USER appuser
        ```

5.  **Exposing unnecessary ports (`EXPOSE 8080`)**:
    *   **Problem**: This might not seem like a vulnerability, but exposing ports that are not needed increases the attack surface.
    *   **Fix**: Only `EXPOSE` the ports that your application actually listens on.

## How to Analyze

You can use static analysis tools like `hadolint` to automatically check your `Dockerfile` for common security issues and bad practices.

```bash
# Install hadolint (e.g., on macOS)
brew install hadolint

# Run hadolint on the Dockerfile
hadolint Dockerfile
```

This will produce a report detailing the issues found in the file.
