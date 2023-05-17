# Stage 1: Build the base image
FROM python:3.9-slim as gptfx-base

# Update the base image
RUN apt-get update && apt-get install -y \
    ca-certificates

# Install utilities
RUN apt-get install -y curl git

# Set the working directory to /app
WORKDIR /app

# Install Python dependencies from the requirements.txt file
COPY requirements.txt .
RUN pip install -r requirements.txt

# Stage 2: Build the gptfx image
FROM gptfx-base as gptfx

# Copy the entire contents of the current directory to the Docker image
COPY . .

# Install the app
RUN pip install .

# Set the entrypoint
ENTRYPOINT ["python", "-m", "gptfx"]
