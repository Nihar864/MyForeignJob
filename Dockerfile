# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set working directory
WORKDIR /myforeignjob

# Install system dependencies
RUN apt-get update && apt-get install -y gcc

# Copy requirements file
COPY requirements.txt .

# Upgrade pip
RUN pip install --upgrade pip

# Install Python dependencies
RUN pip install --upgrade pip              
RUN pip install -r requirements.txt

# Copy the project files
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8000

# Run the application
CMD ["python", "main.py"]



