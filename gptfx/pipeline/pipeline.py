import os

import tfx.v1 as tfx

import gptfx.pipeline as pipeline
import gptfx.pipeline.containers as components


def create_pipeline(config: pipeline.configs.Config, **kwargs) -> tfx.dsl.Pipeline:
    """

    Returns:
        tfx.dsl.Pipeline:
    """
    pipeline_name = kwargs.get('pipeline_name', None) or config.pipeline_name
    pipeline_root = kwargs.get('pipeline_root', None) or config.pipeline_root
    data_root = kwargs.get('data_root', None) or config.data_root
    metadata_root = kwargs.get('metadata_root', None) or config.metadata_root
    log_root = kwargs.get('log_root', None) or config.log_root
    module_file = kwargs.get('module_file', None) or config.module_file

    pipeline_root = os.path.join(pipeline_root, pipeline_name)
    data_root = os.path.join(data_root, pipeline_name)
    metadata_root = os.path.join(metadata_root, pipeline_name)

    os.makedirs(pipeline_root, exist_ok=True)
    os.makedirs(data_root, exist_ok=True)
    os.makedirs(metadata_root, exist_ok=True)

    pipeline_component_instances = components.create_pipeline_component_instances(
        pipeline_name=pipeline_name,
        pipeline_root=pipeline_root,
        data_root=data_root,
        metadata_root=metadata_root,
        log_root=log_root,
        module_file=module_file,
    )

    return tfx.dsl.Pipeline(
        pipeline_name=pipeline_name,
        pipeline_root=pipeline_root,
        metadata_connection_config=tfx.orchestration.metadata.sqlite_metadata_connection_config(
            os.path.join(metadata_root, 'metadata.db')
        ),
        components=pipeline_component_instances,
        enable_cache=True,
        module_file=module_file,
        # beam_pipeline_args=['--direct_num_workers=0'],
        # execution_mode=kwargs.get('execution_mode', tfx.dsl.ExecutionMode.SYNC),
        # inputs=kwargs.get('inputs', None),
        # outputs=kwargs.get('outputs', None),
        # **kwargs
    )
