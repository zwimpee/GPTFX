
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
def main(
    pipeline_name,
    pipeline_root: str,
    continuous: bool,
    continuous_limit: int,
    ai_settings_file: str,
    skip_reprompt: bool,
    speak: bool,
    debug: bool,
    gpt3only: bool,
    gpt4only: bool,
    memory_type: str,
    browser_name: str,
    allow_downloads: bool,
    skip_news: bool
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