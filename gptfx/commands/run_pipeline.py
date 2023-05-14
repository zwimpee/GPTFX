import absl
import click
import tfx.v1 as tfx
import gptfx.pipeline as pipeline


def run(config: pipeline.configs.Config = None) -> None:
    absl.logging.set_verbosity(absl.logging.INFO)
    tfx.orchestration.LocalDagRunner.run(pipeline.create_pipeline(config))


@click.command()
@click.option('--pipeline_name', default=None, help='Name of the pipeline.')
@click.option('--pipeline_root', default=None, help='Root directory of the pipeline.')
@click.option('--data_root', default=None, help='Root directory of the data.')
@click.option('--metadata_root', default=None, help='Root directory of the metadata.')
@click.option('--module_file', default=None, help='Module file containing pre/post processing logic.')
def run_pipeline(
    pipeline_name: str = None,
    pipeline_root: str = None,
    data_root: str = None,
    metadata_root: str = None,
    module_file: str = None,
):
    absl.logging.set_verbosity(absl.logging.INFO)
    run(
        config=pipeline.configs.Config(
            pipeline_name=pipeline_name,
            pipeline_root=pipeline_root,
            data_root=data_root,
            metadata_root=metadata_root,
            module_file=module_file,
        )
    )


if __name__ == '__main__':
    absl.logging.set_verbosity(absl.logging.INFO)
    run_pipeline()
