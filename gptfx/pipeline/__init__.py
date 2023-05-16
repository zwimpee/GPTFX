import configs
import pipeline


# noinspection PyProtectedMember
def create_pipeline(
    pipeline_name: str = configs._PIPELINE_NAME,
    pipeline_root: str = configs._PIPELINE_ROOT,
    data_root: str = configs._DATA_ROOT,
    metadata_root: str = configs._METADATA_ROOT,
    config: configs.Config = configs.Config()
):

    return pipeline._create_pipeline(
        pipeline_name=pipeline_name,
        pipeline_root=pipeline_root,
        data_root=data_root,
        metadata_root=metadata_root,
        config=config,
    )