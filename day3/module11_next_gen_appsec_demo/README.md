# Next-Gen AppSec Demo: CI/CD Security

This directory contains an example of a GitHub Actions workflow that integrates an automated security scanner into a Continuous Integration (CI) pipeline. This is a fundamental practice in DevSecOps, often referred to as "shifting left" – finding and fixing security issues early in the development lifecycle.

## The Demo

The demo consists of two parts:
1.  A GitHub Actions workflow file located at `.github/workflows/security-scan.yml`.
2.  A sample source code file, `sample_code_with_secret.py`, that contains a hardcoded secret.

### The GitHub Actions Workflow

The `security-scan.yml` file defines a CI job that is triggered every time code is pushed to any branch in the repository. The job performs the following steps:

1.  **Checks out the code:** It downloads the latest version of the code in the repository.
2.  **Runs TruffleHog:** It uses the official `trufflesecurity/trufflehog` GitHub Action to scan the entire repository for secrets.
3.  **Fails the build:** The action is configured with `--fail`, which means that if TruffleHog finds any potential secrets, the CI job will fail. This can be used to block pull requests from being merged if they contain hardcoded credentials.

### How It Works

By placing this workflow in your repository, you automate the process of secret scanning. Developers get instant feedback if they accidentally try to commit a password, API key, or private key. This prevents secrets from ever entering the Git history, which is a major security improvement.

This is a simple example of DevSecOps. The same principle can be applied to many other security tools:
*   **SAST (Static Application Security Testing):** Tools like `CodeQL`, `Snyk`, or `Semgrep` can be run to find vulnerabilities in the source code.
*   **SCA (Software Composition Analysis):** Tools like `OWASP Dependency-Check` or `npm audit` can be run to find known vulnerabilities in third-party libraries.
*   **IaC Scanning:** Tools like `tfsec` or `checkov` can scan Infrastructure as Code files (Terraform, CloudFormation) for security misconfigurations.
*   **Container Scanning:** Tools like `Trivy` or `Grype` can scan Docker images for vulnerabilities.

## How to Use This Demo

1.  **Create a GitHub Repository:** To see this in action, you would create a new repository on GitHub.
2.  **Add the Files:** Add the `.github/workflows/security-scan.yml` file and the `sample_code_with_secret.py` file to your repository.
3.  **Push the Code:**
    ```bash
    git add .
    git commit -m "Add security workflow and sample code"
    git push
    ```
4.  **Observe the Action:** Go to the "Actions" tab in your GitHub repository. You will see the "Security Scan" workflow running. It will fail because `sample_code_with_secret.py` contains a hardcoded secret, and TruffleHog will detect it. You can click on the failed job to see the output from the scanner.
