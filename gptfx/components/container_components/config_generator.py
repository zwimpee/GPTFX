
import os

import click
from absl import logging
import tensorflow as tf

from autogpt import configurator


@click.command()
@click.option('--pipeline_name', type=str, required=True)
@click.option('--pipeline_root', type=str, required=True)
@click.option('--data_root', type=str, required=True)
@click.option('--metadata_root', type=str, required=True)
@click.option('--continuous', type=bool, required=False)
@click.option('--ai_settings_file', type=str, required=False)
@click.option('--skip_reprompt', type=bool, required=False)
@click.option('--speak', type=bool, required=False)
@click.option('--debug', type=bool, required=False)
@click.option('--gpt3only', type=bool, required=False)
@click.option('--gpt4only', type=bool, required=False)
@click.option('--memory_type', type=str, required=False)
@click.option('--browser_name', type=str, required=False)
@click.option('--allow_downloads', type=bool, required=False)
@click.option('--skip_news', type=bool, required=False)
@click.pass_context
def main(
    ctx: click.Context = None,
    pipeline_name = None,
    pipeline_root: str = None,
    continuous: bool = None,
    continuous_limit: int = None,
    ai_settings_file: str = None,
    skip_reprompt: bool = None,
    speak: bool = None,
    debug: bool = None,
    gpt3only: bool = None,
    gpt4only: bool = None,
    memory_type: str = None,
    browser_name: str = None,
    allow_downloads: bool = None,
    skip_news: bool = None
) -> None:
    logging.basicConfig(level=logging.INFO)
    logging.info('Generating pipeline config for %s', pipeline_name)

    cfg = configurator.Config()
    configurator.create_config(
        continuous=continuous,
        continuous_limit=continuous_limit,
        ai_settings_file=ai_settings_file,
        skip_reprompt=skip_reprompt,
        speak=speak,
        debug=debug,
        gpt3only=gpt3only,
        gpt4only=gpt4only,
        memory_type=memory_type,
        browser_name=browser_name,
        allow_downloads=allow_downloads,
        skip_news=skip_news
    )

    logging.info('Done generating pipeline config for %s', pipeline_name)

    with tf.io.gfile.GFile(os.path.join(pipeline_root, 'config.json'), 'w') as f:
        tf.io.write_file(f, cfg)


if __name__ == '__main__':
    main()