# GPTFX (GPT-Extended)

GPTFX is a framework that provides a scalable and extensible structure for incorporating Large Language Model (LLM) agents into TFX pipelines. GPTFX enables the generation of container-based TFX components that house the LLM agent and other custom components, such as configuration generators and output data processors.

## Project Structure

```markdown
GPTFX
├── gptfx
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── commands
│   │   ├── __init__.py
│   │   ├── run_pipeline.py
│   ├── components
│   │   ├── __init__.py
│   │   ├── container_components
│   │   │   ├── __init__.py
│   │   │   ├── config_generator.py
│   │   │   └── output_processing.py
│   │   └── transform_components
│   │       ├── __init__.py
│   │       └── autogpt_utils.py
│   └── pipeline
│       ├── __init__.py
│       ├── configs.py
│       └── pipeline.py
├── .env
├── docker-compose.yml
├── Dockerfile
├── README.md
├── environment.yml
└── requirements.txt
```

# Technologies Used
GPTFX utilizes a range of technologies and frameworks, including:

- **Python**: The primary language for development, offering flexibility and a rich ecosystem of libraries.
- **Conda**: The package and environment manager for Python, enabling the creation of isolated environments with specific dependencies.
- **Docker**: The containerization platform for building and deploying container images, ensuring consistent and reproducible execution environments.
- **Tensorflow** and **TFX**: Core frameworks for building and running machine learning pipelines, offering data processing, model training, and model serving capabilities.

Getting Started
To get started with GPTFX, follow these steps:

1. Clone the GPTFX repository: Begin by cloning the GPTFX repository to your local machine:
    ```git clone https://github.com/zwimpee/GPTFX.git.```

2. cd into the GPTFX directory: Navigate to the project directory:
    ```cd GPTFX```

3. Install dependencies: Install the necessary dependencies and libraries required for the project:
    ```conda env create -f environment.yml```

4. Create the Conda environment: Create the Conda environment with the necessary dependencies:
    ```conda activate gptfx```

5. Using conda-build, install the application into the conda environment:
    ```conda develop .```

6. Compile images that will be used to run the application:
   - **Auto-GPT**:  

Install dependencies: Navigate to the project directory and use pip to install the necessary dependencies and libraries required for the project by running pip install -r requirements.txt.

Create the Conda environment: Use conda env create -f environment.yml to create the Conda environment with the necessary dependencies.

Build and deploy Docker containers: Build the Docker image with docker build -t gptfx . and then start the container with docker run -p 8000:8000 gptfx.

Define TFX pipeline and components: Define the TFX pipeline and the corresponding components, including the container-based components, configuration generators, and output data processors.

Run the pipeline: Execute the TFX pipeline and monitor its execution and outputs.

Current Progress
Currently, the project is in the proof of concept stage. The development efforts are focused on creating container-based TFX components, a configuration generator component, and an output data processor component. These components aim to seamlessly integrate the LLM agent into the TFX pipeline, enabling the generation of a prompt for the agent, the execution of the agent pipeline, and the processing of the agent’s output.

Contribution Guidelines
Contributions to GPTFX are welcome! If you have any ideas, bug fixes, or new features to propose, please open an issue or submit a pull request in the repository. The project follows industry-standard practices for contributing, and detailed guidelines can be found in the CONTRIBUTING