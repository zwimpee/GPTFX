import tfx.v1 as tfx

import gptfx.pipeline.configs as configs
import gptfx.pipeline.pipeline as pipeline


def create_pipeline(
    pipeline_name: str = None,
    pipeline_root: str = None,
    data_root: str = None,
    metadata_root: str = None,
    log_root: str = None,
    module_file: str = None,
) -> tfx.dsl.Pipeline:
    config = configs.get_config(
        **dict(
            pipeline_name=pipeline_name,
            pipeline_root=pipeline_root,
            data_root=data_root,
            metadata_root=metadata_root,
            log_root=log_root,
            module_file=module_file,
        )
    )

    return pipeline.create_pipeline(config=config)
