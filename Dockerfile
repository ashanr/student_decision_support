FROM python:3.9-slim

WORKDIR /app

# Install build dependencies for numpy and pandas
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create directory structure
RUN mkdir -p data

# Copy application files
COPY *.py /app/
COPY *.md /app/

# Copy data directory if it exists
COPY data/ /app/data/

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Make port 5000 available
EXPOSE 5000

# Add health check for dependencies
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python check_dependencies.py || exit 1

# Run the application
CMD ["python", "app.py"]
