# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies (only run this step if necessary)
RUN apt-get update && \
    apt-get install -y --no-install-recommends make curl sudo && \
    curl -fsSL https://jprq.io/install.sh | sudo bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Expose port 1298
EXPOSE 1298

# Run the startup script
CMD ["bash", "start.sh"]