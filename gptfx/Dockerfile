# AutoGPT base
FROM zwimpee/auto-gpt:latest as autogpt-base

# GPTFX base with Python 3.8
FROM python:3.8-slim as gptfx_base

WORKDIR /app

# Copy the entire content from AutoGPT base
COPY --from=autogpt-base . ./autogpt

# Copy the requirements.txt file into the image
COPY requirements.txt .

# Set environment variables
ENV PIP_NO_CACHE_DIR=yes \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="$PATH:/root/.local/bin"

# Update and install build tools
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    --no-install-recommends \
 && rm -rf /var/lib/apt/lists/*

# Update pip and install the required python packages globally
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the app folder into the image
COPY . .


# Container components
FROM gptfx_base as container_component_base

WORKDIR /app

COPY /usr/local/lib/python3.8/site-packages/ /usr/local/lib/python3.8/site-packages/

WORKDIR /app/gptfx/components/container_components

# Config generator component
FROM container_component_base as config_generator_component
COPY container_components/config_generator.py .
ENTRYPOINT ["python", "config_generator.py"]

# Output processing component
FROM container_component_base as output_processing_component
COPY container_components/output_processing_component.py .
ENTRYPOINT ["python", "output_processing_component.py"]

# Dev build - include everything
FROM gptfx_base as gptfx-dev
ONBUILD COPY . ./app

# Release build - include bare minimum
FROM gptfx_base as gptfx-release

# Remove unneeded items from requirements and install
RUN sed -i '/Items below this point will not be included in the Docker Image/,$d' requirements.txt && \
	pip install --no-cache-dir -r requirements.txt

# Copy needed directories
ONBUILD COPY gptfx/ ./app/gptfx
ONBUILD COPY scripts/ ./app/scripts
ONBUILD COPY plugins/ ./app/plugins

# Final image
FROM gptfx-${BUILD_TYPE} AS gptfx
WORKDIR /app
