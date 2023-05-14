FROM significantgravitas/auto-gpt:latest as autogpt_base
FROM tensorflow/tfx_base:latest as tfx_base

# Path: Dockerfile
FROM tfx_base as gptfx_base

# Install the required python packages globally
ENV PATH="$PATH:/root/.local/bin"
ENV PIP_NO_CACHE_DIR=yes \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install the required python packages globally
ENV PATH="$PATH:/root/.local/bin"
COPY requirements.txt .

ENTRYPOINT ["python", "-m", "gptfx"]

# Container components
FROM gptfx_base as container_component_base

# Install the required python packages globally
ENV PATH="$PATH:/root/.local/bin"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app/gptfx/container_components

FROM container_component_base as config_generator_component

COPY container_components/config_generator_component.py .

ENTRYPOINT ["python", "config_generator.py"]

FROM autogpt_base as autogpt_component

FROM container_component_base as output_processing_component

COPY container_components/output_processing_component.py .

ENTRYPOINT ["python", "output_processing_component.py"]

# dev build -> include everything
FROM gptfx_base as gptfx-dev
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /app
ONBUILD COPY . ./











