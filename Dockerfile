# Use official Python image
FROM python:3.9-slim

# Set environment vars
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install required packages
RUN pip install --upgrade pip

# Copy files
WORKDIR /app
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Entry point
CMD ["python", "docker_cpu_monitor.py"]
