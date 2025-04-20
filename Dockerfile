# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies and both jprq & ngrok
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl sudo gnupg make && \
    \
    # Install jprq
    curl -fsSL https://jprq.io/install.sh | sudo bash && \
    \
    # Install ngrok
    curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
        | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && \
    echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
        | sudo tee /etc/apt/sources.list.d/ngrok.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends ngrok && \
    \
    # Clean up
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Expose port 8000
EXPOSE 8000

# Run the startup script
CMD ["bash", "start.sh"]