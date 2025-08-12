# This file is intended to be scanned by the TruffleHog action in the CI/CD pipeline.
# It contains a hardcoded secret that should be detected.

import boto3

def get_secret_from_aws():
    # This is a fake AWS access key ID, but it has the right format to be
    # detected by secret scanners.
    aws_access_key_id = "AKIAIOSFODNN7EXAMPLE"

    # In a real scenario, this would be a real secret.
    # The TruffleHog scanner in the GitHub Actions workflow should find this
    # and fail the build, preventing this secret from being merged.

    client = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    )

    print("Attempting to connect to AWS with hardcoded keys...")
    # ... rest of the function
    pass

print("This script contains a hardcoded secret.")
