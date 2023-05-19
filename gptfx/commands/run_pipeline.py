# ./gptfx/commands/run_pipeline.py
import absl
import click
from tfx.orchestration.local.local_dag_runner import LocalDagRunner

from gptfx import pipeline


def run_pipeline(
    ctx: click.Context,
    pipeline_name: str = None,
    pipeline_root: str = None,
    data_root: str = None,
    metadata_root: str = None,
    log_root: str = None,
    module_file: str = None,
):
    absl.logging.set_verbosity(absl.logging.INFO)
    run(
        pipeline_name=pipeline_name,
        pipeline_root=pipeline_root,
        data_root=data_root,
        metadata_root=metadata_root,
        log_root=log_root,
        module_file=module_file,
    )


def run(
    pipeline_name: str = None,
    pipeline_root: str = None,
    data_root: str = None,
    metadata_root: str = None,
    log_root: str = None,
    module_file: str = None,
) -> None:
    absl.logging.set_verbosity(absl.logging.INFO)
    _pipeline = pipeline.create_pipeline(
        pipeline_name=pipeline_name,
        pipeline_root=pipeline_root,
        data_root=data_root,
        metadata_root=metadata_root,
        log_root=log_root,
        module_file=module_file,
    )
    LocalDagRunner(
        # tfx.proto.CustomConfig()
    ).run(
        pipeline=_pipeline
    )


if __name__ == '__main__':
    absl.logging.set_verbosity(absl.logging.INFO)
    run_pipeline()
