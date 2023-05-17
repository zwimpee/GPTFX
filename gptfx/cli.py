# ./gptfx/cli.py
import os

import click

PIPELINE_NAME = os.environ.get("PIPELINE_NAME", "gptfx-pipeline")
PIPELINE_ROOT = os.environ.get("PIPELINE_ROOT", os.path.join(os.getcwd(), "pipelines", PIPELINE_NAME))
DATA_ROOT = os.environ.get("DATA_ROOT", os.path.join(os.getcwd(), "data"))
METADATA_ROOT = os.environ.get("METADATA_ROOT", os.path.join(DATA_ROOT, "metadata"))
LOG_ROOT = os.environ.get("LOG_ROOT", os.path.join(DATA_ROOT, "logs"))
MODULE_FILE = os.environ.get("MODULE_FILE", None)


@click.command()
@click.option(
    "--pipeline_name",
    default=PIPELINE_NAME,
    help="Name of the pipeline.",
    type=str,
)
@click.option(
    "--pipeline_root",
    default=PIPELINE_ROOT,
    help="Root directory of the pipeline.",
    type=str,
)
@click.option(
    "--data_root",
    default=DATA_ROOT,
    help="Root directory of the data.",
    type=str,
)
@click.option(
    "--metadata_root",
    default=METADATA_ROOT,
    help="Root directory of the metadata.",
    type=str,
)
@click.option(
    "--log_root",
    default=LOG_ROOT,
    help="Root directory of the logs.",
    type=str,
)
@click.option(
    "--module_file",
    default=MODULE_FILE,
    help="Module file containing pre/post processing logic.",
    type=str,
)
@click.pass_context
def main(
    ctx: click.Context,
    pipeline_name: str = None,
    pipeline_root: str = None,
    data_root: str = None,
    metadata_root: str = None,
    log_root: str = None,
    module_file: str = None,
) -> None:
    """
    Welcome to GPTFX, an experimental extension of Auto-GPT utilizing the TensorFlow Extended (TFX) framework to
    manage Agents and Pipelines.
    """
    # Put imports inside function to avoid importing everything when starting the CLI
    from gptfx.commands import run_pipeline

    run_pipeline.run_pipeline(
        ctx=ctx,
        pipeline_name=pipeline_name,
        pipeline_root=pipeline_root,
        data_root=data_root,
        metadata_root=metadata_root,
        log_root=log_root,
        module_file=module_file,
    )


if __name__ == "__main__":
    main()
