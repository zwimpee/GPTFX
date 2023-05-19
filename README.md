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
│   │   ├── agents
│   │   │   ├── __init__.py
│   │   │   ├── autogpt
│   │   │   ├── langchain
│   │   │   └── openai
│   │   ├── configs
│   │   │   ├── __init__.py
│   │   │   └── config.py
│   │   └── models
│   │       ├── __init__.py
│   │       ├── model.py
│   │       └── train.py
│   ├── pipeline
│   │   ├── __init__.py
│   │   ├── configs.py
│   │   └── pipeline.py
│   └── utils
│       ├── __init__.py
│       ├── autogpt_utils.py
│       ├── openai_utils.py
│       └── tfx_utils.py
├── logs
├── scripts
│   ├── conda_cleanup.ps1
│   └── project_file_tree.ps1
├── docker-compose.yml
├── Dockerfile
├── README.md
├── environment.yml
├── requirements.txt
└── setup.py

```

# Technologies Used
GPTFX utilizes a range of technologies and frameworks, including:

- **Python**: The primary language for development, offering flexibility and a rich ecosystem of libraries.
- **Conda**: The package and environment manager for Python, enabling the creation of isolated environments with specific dependencies.
- **Docker**: The containerization platform for building and deploying container images, ensuring consistent and reproducible execution environments.
- **Tensorflow** and **TFX**: Core frameworks for building and running machine learning pipelines, offering data processing, model training, and model serving capabilities.

# Getting Started
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
    - **Pipeline Components**:
        - **Configuration generation**:
          ```docker build -t <name of image> <path to Dockerfile>```
        - **LLM Agent**:
          ```docker build -t <name of image> <path to Dockerfile>```
        - **Output data processing**:
          ```docker build -t <name of image> <path to Dockerfile>```

7. Run the application: Run the application using the following command:
   ```python -m gptfx <command> <arguments>```
   where:
    - **command**: The command to execute. If left blank, the application will default to the run_pipeline command (via
      the __main__.py/cli.py/run_pipeline.py files).
    - **arguments**: The arguments to pass to the command. If left blank, the application will use default arguments.

# Current Progress

- General project progress:
    - [X] Define the project structure
    - [X] Determine the MVP for the first iteration of the project
    - [X] Create the initial project files
    - [X] Create the initial Dockerfile
    - [X] Create the initial environment.yml file
    - [X] Create the initial requirements.txt file
    - [X] Create the initial setup.py file
    - [X] Create the initial README.md file

- MVP progress:
    - [X] Create the initial pipeline components
    - [X] Create the initial pipeline
    - [X] Create the initial CLI
    - [X] Create the initial Dockerfile
    - [X] Create the initial environment.yml file
    - [X] Create the initial requirements.txt file
    - [X] Create the initial setup.py file
    - [X] Create the initial README.md file
    - [ ] Run the pipeline and explore the outputs

# Contribution Guidelines
Contributions to GPTFX are welcome! If you have any ideas, bug fixes, or new features to propose, please open an issue or submit a pull request in the repository. The project follows industry-standard practices for contributing, and detailed guidelines can be found in the CONTRIBUTING