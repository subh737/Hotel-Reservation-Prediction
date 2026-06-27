# Use a lightweight Python image
FROM python:slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies required by LightGBM
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the application code (this will include the model files Jenkins creates!)
COPY . .

# Install the package in editable mode
RUN pip install --no-cache-dir -e .

EXPOSE 5000

# Just start the app!
CMD ["python", "application.py"]