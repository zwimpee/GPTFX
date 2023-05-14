# 'dev' or 'release' container build
ARG BUILD_TYPE=dev

FROM significantgravitas/auto-gpt:latest as autogpt-base

FROM autogpt-base as auto-gpt

WORKDIR /app

# Copy the requirements.txt file from the app folder into the image
COPY requirements.txt .

# Set environment variables
ENV PIP_NO_CACHE_DIR=yes \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Update pip and install the required python packages globally
ENV PATH="$PATH:/root/.local/bin"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir -e . \

# Container components
FROM gptfx_base as container_component_base

WORKDIR /app/gptfx/components/container_components

FROM container_component_base as config_generator_component

COPY container_components/config_generator_component.py .

ENTRYPOINT ["python", "config_generator.py"]

FROM container_component_base as output_processing_component

COPY container_components/output_processing_component.py .

ENTRYPOINT ["python", "output_processing_component.py"]



FROM tensorflow/tfx_base:latest as gptfx_base

WORKDIR /app

# Copy the requirements.txt file from the app folder into the image
COPY requirements.txt .

# Set environment variables
ENV PIP_NO_CACHE_DIR=yes \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Update pip and install the required python packages globally
ENV PATH="$PATH:/root/.local/bin"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt





# dev build -> include everything
FROM gptfx_base as gptfx-dev

WORKDIR /app

ONBUILD COPY . ./

# release build -> include bare minimum
FROM gptfx_base as gptfx-release
RUN sed -i '/Items below this point will not be included in the Docker Image/,$d' requirements.txt && \
	pip install --no-cache-dir -r requirements.txt
WORKDIR /app
ONBUILD COPY gptfx/ ./gptfx
ONBUILD COPY scripts/ ./scripts
ONBUILD COPY plugins/ ./plugins

WORKDIR /app
ONBUILD COPY gptfx/ ./gptfx
ONBUILD COPY scripts/ ./scripts
ONBUILD COPY plugins/ ./plugins

FROM gptfx-${BUILD_TYPE} AS gptfx
