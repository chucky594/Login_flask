# Use a lightweight official Python image
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Install OS packages your app might need (optional)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first (leverages Docker layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your project
COPY . .

# Expose the service port (change if needed)
EXPOSE 5000

# Run your Flask app
CMD ["python3", "app.py"]

