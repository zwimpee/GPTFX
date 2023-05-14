"""Main script for the autogpt package."""
from typing import Any, Dict

import click


@click.group(invoke_without_command=True)
@click.option(
    "--pipeline_name",
    default=None,
    help="Name of the pipeline.",
)
@click.option(
    "--pipeline_root",
    default=None,
    help="Root directory of the pipeline.",
)
@click.option(
    "--data_root",
    default=None,
    help="Root directory of the data.",
)
@click.option(
    "--metadata_root",
    default=None,
    help="Root directory of the metadata.",
)
@click.option(
    "--config",
    default=None,
    help="Config file to use.",
)

@click.pass_context
def main(
    ctx: click.Context = None,
    pipeline_name: str = None,
    pipeline_root: str = None,
    data_root: str = None,
    metadata_root: str = None,
    config: Any = None,
    **kwargs: Dict[str, Any]
) -> None:
    """
    Welcome to GPTFX, an experimental extension of Auto-GPT utilizing the TensorFlow Extended (TFX) framework to manage Agents and Pipelines.
    """
    # Put imports inside function to avoid importing everything when starting the CLI
    from gptfx.commands import run_pipeline

    if ctx.invoked_subcommand is None:
        run_pipeline.run_pipeline(
            pipeline_name,
            pipeline_root,
            data_root,
            metadata_root,
            config,
            **kwargs,
        )


if __name__ == "__main__":
    main()
