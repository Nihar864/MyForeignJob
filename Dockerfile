# Use an official Python runtime as the base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /myforeignjob

# Install system dependencies needed for your app
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libcairo2 \
        libpango-1.0-0 \
        libpangocairo-1.0-0 \
        libgdk-pixbuf2.0-0 \
        gir1.2-gtk-3.0 \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements to leverage Docker cache
COPY ./requirements.txt ./

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Create a non-root user and switch to it
RUN useradd --create-home appuser
USER appuser

# Expose the port your FastAPI app will run on
EXPOSE 8000

# Run the app using uvicorn for production
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
