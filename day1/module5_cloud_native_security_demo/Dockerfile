# This Dockerfile is intentionally insecure for demonstration purposes.

# 1. Using a vague and potentially outdated base image
FROM python:3.8

# 2. Hardcoding secrets directly in the Dockerfile
ENV DB_PASSWORD="supersecretpassword123"

WORKDIR /app

COPY . /app

# 3. Installing packages with --no-cache which can hide issues, and not pinning versions
RUN pip install --no-cache-dir -r requirements.txt

# 4. Running the container as the root user (default)
# This is a major security risk. If an attacker gains control of the
# application, they will have root privileges inside the container.

# 5. Exposing an unnecessary port
EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
