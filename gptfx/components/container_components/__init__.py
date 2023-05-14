from tfx.dsl.component.experimental.container_component import create_container_component
from tfx.dsl.component.experimental.placeholders import InputUriPlaceholder, OutputUriPlaceholder, InputValuePlaceholder
import tfx.types as types

import autogpt.config
import gptfx.pipeline.configs

config_generator_component = create_container_component(
    name='config_gen_component',
    image='config_generator_component:latest',
    command=[
        'python',
        'gptfx',
        'config_gen',
        '--pipeline_name', InputValuePlaceholder('pipeline_name'),
        '--pipeline_root', InputValuePlaceholder('pipeline_root'),
        '--data_root', InputValuePlaceholder('data_root'),
        '--log_root', InputValuePlaceholder('log_root'),
        '--metadata_root', InputValuePlaceholder('metadata_root'),
        '--pipeline_config_uri', OutputUriPlaceholder('pipeline_config'),
    ],
    inputs={
        'autogpt_config': autogpt.config.Config,
        'ai_config': autogpt.config.AIConfig,
    },
    outputs={
        'pipeline_config': gptfx.pipeline.configs.Config,
    },
    parameters={
        'pipeline_name': str,
        'pipeline_root': str,
        'data_root': str,
        'log_root': str,
        'metadata_root': str,
    },
)

autogpt_component = create_container_component(
    name='autogpt_component',
    image='zwimpee/auto-gpt:latest',
    command=[
        'python',
        '-m',
        'autogpt',
    ],
    inputs={
        'pipeline_config': gptfx.pipeline.configs.Config,
    },
    outputs={
        'data': types.artifact.json_utils.JsonableType,
    },
    parameters={}
)

output_processing_component = create_container_component(
    name='output_processing_component',
    image='output_processing_component:latest',
    command=[
        'python',
        'gptfx',
        'post_processing',
        '–data_uri', InputUriPlaceholder('data'),
        '--output_uri', OutputUriPlaceholder('output'),
    ],
    inputs={
        'data': types.artifact.json_utils.JsonableType,
    },
    outputs={
        'output': types.artifact.json_utils.JsonableType,
    },
    parameters={
        'module_file': str,
    }
)


def create_pipeline_component_instances(
    pipeline_name,
    pipeline_root,
    data_root,
    metadata_root,

):
    """Creates a list of component instances for the pipeline."""

    config_gen_task = config_generator_component(
        pipeline_name=pipeline_name,
        pipeline_root=pipeline_root,
        data_root=data_root,
        metadata_root=metadata_root,
    )

    autogpt_task = autogpt_component(
        pipeline_config=config_gen_task.outputs['pipeline_config'],
    )

    post_processing_task = output_processing_component(
        inputs=autogpt_task.outputs['data'],
    )

    component_instances = [
        config_gen_task,
        autogpt_task,
        post_processing_task
    ]

    return component_instances
