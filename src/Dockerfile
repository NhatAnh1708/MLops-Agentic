# Use an official Python image as the base
FROM python:3.11-slim

# Set environment variables to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install Playwright dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    gnupg \
    curl && \
    pip install playwright && \
    playwright install-deps && \
    playwright install && \
    rm -rf /var/lib/apt/lists/*
# Copy requirements.txt and install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the application files
COPY . /app

COPY ssl/ /etc/nginx/ssl/
# Set working directory
WORKDIR /app

EXPOSE 30000

# CMD ["uvicorn", "server:app", "--port", "30000", "--host", "0.0.0.0", "--ssl-keyfile", "/etc/nginx/ssl/tls.key", "--ssl-certfile", "/etc/nginx/ssl/tls.crt"]
CMD ["uvicorn", "server:app", "--port", "30000", "--host", "0.0.0.0"]