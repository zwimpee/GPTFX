

# Use a Python 3.8 slim image as the base image
FROM python:3.8-slim as gptfx-base

# Install browsers
RUN apt-get update && apt-get install -y \
    chromium-driver firefox-esr \
    ca-certificates

# Install utilities
RUN apt-get install -y curl jq wget git

# Install gcc and build-essential
RUN apt-get install -y gcc build-essential

# Set environment variables
ENV PIP_NO_CACHE_DIR=yes \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set the Python path to include packages installed by pip
ENV PATH="$PATH:/root/.local/bin"

# Copy the requirements.txt file to the Docker image
COPY requirements.txt .

# Install the required python packages globally
RUN pip install --no-cache-dir -r requirements.txt

# Use the base image to create a new build stage called gptfx-dev
FROM gptfx-base as gptfx-dev

# Set the working directory to /app
WORKDIR /app

# Copy the entire contents of the current directory to the Docker image
COPY . .

# Install the gptfx package
RUN pip install .

# Use the gptfx-dev build stage to create the final Docker image
FROM gptfx-dev AS gptfx

# Set the entrypoint
ENTRYPOINT ["python", "-m", "gptfx"]

