import os
from typing import Any

import tfx.v1 as tfx

import autogpt
from autogpt import configurator
from autogpt import config as autogpt_config
from autogpt.config import check_openai_api_key
import gptfx.pipeline as pipeline
import gptfx.components as components


def _create_pipeline(config: pipeline.configs.Config, **kwargs) -> tfx.dsl.Pipeline:
    pipeline_name = kwargs.get('pipeline_name', None) or config.pipeline_name
    pipeline_root = kwargs.get('pipeline_root', None) or config.pipeline_root
    data_root = kwargs.get('data_root', None) or config.data_root
    metadata_root = kwargs.get('metadata_root', None) or config.metadata_root

    cfg = autogpt_config.Config()
    check_openai_api_key()
    configurator.create_config(
        continuous=kwargs.get('continuous', None) or cfg.continuous_mode,
        continuous_limit=kwargs.get('continuous_limit', None) or cfg.continuous_limit,
        ai_settings_file=kwargs.get('ai_settings_file', None) or cfg.ai_settings_file,
        skip_reprompt=kwargs.get('skip_reprompt', None) or cfg.skip_reprompt,
        speak=kwargs.get('speak', None) or cfg.speak_mode,
        debug=kwargs.get('debug', None) or cfg.debug_mode,
        gpt3only=kwargs.get('gpt3only', None) or cfg.fast_llm_model,
        gpt4only=kwargs.get('gpt4only', None) or cfg.fast_llm_model,
        memory_type=kwargs.get('memory_type', None) or cfg.memory_backend,
        browser_name=kwargs.get('browser_name', None) or cfg.selenium_web_browser,
        allow_downloads=kwargs.get('allow_downloads', None) or cfg.allow_downloads,
        skip_news=kwargs.get('skip_news', None) or cfg.skip_news,
    )

    pipeline_root = os.path.join(pipeline_root, pipeline_name)
    data_root = os.path.join(data_root, pipeline_name)
    metadata_root = os.path.join(metadata_root, pipeline_name)

    os.makedirs(pipeline_root, exist_ok=True)
    os.makedirs(data_root, exist_ok=True)
    os.makedirs(metadata_root, exist_ok=True)

    pipeline_component_instances = components.container_components.create_pipeline_component_instances(
        pipeline_name=pipeline_name,
        pipeline_root=pipeline_root,
        data_root=data_root,
        metadata_root=metadata_root,
    )

    return tfx.dsl.Pipeline(
        pipeline_name=pipeline_name,
        pipeline_root=pipeline_root,
        metadata_connection_config=tfx.orchestration.metadata.sqlite_metadata_connection_config(
            os.path.join(metadata_root, 'metadata.db')
        ),
        components=pipeline_component_instances,
        enable_cache=True,
        # beam_pipeline_args=['--direct_num_workers=0'],
        # execution_mode=kwargs.get('execution_mode', tfx.dsl.ExecutionMode.SYNC),
        # inputs=kwargs.get('inputs', None),
        # outputs=kwargs.get('outputs', None),
        # **kwargs
    )
