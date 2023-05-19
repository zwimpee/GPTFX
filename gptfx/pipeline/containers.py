from typing import Any

from tfx.dsl.component.experimental.container_component import create_container_component
from tfx.dsl.component.experimental.placeholders import InputUriPlaceholder, OutputUriPlaceholder, InputValuePlaceholder
from tfx.v1.types import standard_artifacts

CONFIG_GENERATOR_IMAGE = 'config_generator:latest'
LLM_AGENT_IMAGE = 'llm_agent:latest'
OUTPUT_PROCESSING_IMAGE = 'output_processing:latest'

config_generator_component = create_container_component(
    name='config_generator',
    image=CONFIG_GENERATOR_IMAGE,
    command=[
        'python',
        'config_generator',
        '--pipeline_name', InputValuePlaceholder('pipeline_name'),
        '--pipeline_root', InputValuePlaceholder('pipeline_root'),
        '--data_root', InputValuePlaceholder('data_root'),
        '--metadata_root', InputValuePlaceholder('metadata_root'),
        '--log_root', InputValuePlaceholder('log_root'),
        '--module_file', InputValuePlaceholder('module_file'),
    ],
    inputs={},
    outputs={
        'pipeline_config': standard_artifacts.standard_artifacts.JsonValue,
    },
    parameters={
        'pipeline_name': str,
        'pipeline_root': str,
        'data_root': str,
        'metadata_root': str,
        'log_root': str,
        'module_file': Any
    },
)

llm_agent_component = create_container_component(
    name='llm_agent',
    image=LLM_AGENT_IMAGE,
    command=[
        'python',
        'llm_agent',
        '--pipeline_config_uri', InputUriPlaceholder('pipeline_config'),
        '--output_uri', OutputUriPlaceholder('data'),
        '--temperature', InputValuePlaceholder('temperature'),
        'log_root', InputValuePlaceholder('log_root'),

    ],
    inputs={
        'pipeline_config': standard_artifacts.standard_artifacts.JsonValue,
    },
    outputs={
        'data': standard_artifacts.standard_artifacts.ExternalArtifact,
    },
    parameters={
        'temperature': float,
        'log_root': str,
    }
)

output_processing_component = create_container_component(
    name='output_processing',
    image=OUTPUT_PROCESSING_IMAGE,
    command=[
        'python',
        'output_processing',
        '--data_uri', InputUriPlaceholder('data'),
        '--output_uri', OutputUriPlaceholder('output'),
        '--log_root', InputValuePlaceholder('log_root'),
        '--module_file', InputValuePlaceholder('module_file'),
    ],
    inputs={
        'data': standard_artifacts.standard_artifacts.ExternalArtifact,

    },
    outputs={
        'output': standard_artifacts.standard_artifacts.ExternalArtifact,
    },
    parameters={
        'log_root': str,
        'module_file': Any
    }
)


def create_pipeline_component_instances(
    pipeline_name,
    pipeline_root,
    data_root,
    metadata_root,
    log_root,
    module_file,
):
    """Creates a list of component instances for the pipeline."""

    config_gen_task = config_generator_component(
        pipeline_name=pipeline_name,
        pipeline_root=pipeline_root,
        data_root=data_root,
        metadata_root=metadata_root,
        log_root=log_root,
        module_file=module_file,
    )

    llm_task = llm_agent_component(
        pipeline_config=config_gen_task.outputs['pipeline_config'],
        temperature=0.5,
        log_root=log_root,
    )

    post_processing_task = output_processing_component(
        data=llm_task.outputs['data'],
        log_root=log_root,
        module_file=module_file,
    )

    component_instances = [
        config_gen_task,
        llm_task,
        post_processing_task
    ]
    return component_instances
