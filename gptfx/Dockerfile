# Use a Miniconda base image
FROM continuumio/miniconda3:latest as gptfx-base

# Update the base image
RUN apt-get update && apt-get install -y \
    chromium-driver firefox-esr \
    ca-certificates

# Install utilities
RUN apt-get install -y curl jq wget git

# Install gcc and build-essential
RUN apt-get install -y gcc build-essential


# Set the working directory to /app
WORKDIR /app

# Copy the entire contents of the current directory to the Docker image
COPY . .

# Use Conda to create a new environment from the environment.yml file
RUN conda env create -f environment.yml && conda activate gptfx

# Activate the new environment
# SHELL ["conda", "run", "-n", "gptfx", "/bin/bash", "-c"]

# Install the app into the Conda environment
RUN conda develop .

# Set the entrypoint
ENTRYPOINT ["python", "-m", "gptfx"]
