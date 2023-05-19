# ./gptfx/components/agents/langchain/config_generator/config_generator.py
import json
import os

import click
import tensorflow as tf

import gptfx.pipeline.configs


@click.command()
@click.option('--pipeline-name', type=str, required=True)
@click.option('--pipeline-root', type=str, required=True)
@click.option('--data-root', type=str, required=True)
@click.option('--log-root', type=str, required=True)
@click.option('--metadata-root', type=str, required=True)
def generate_config(pipeline_name, pipeline_root, data_root, log_root, metadata_root):
    config = gptfx.pipeline.configs.get_config(
        pipeline_name=pipeline_name,
        pipeline_root=pipeline_root,
        data_root=data_root,
        metadata_root=metadata_root,
        log_root=log_root
    )

    with tf.io.gfile.GFile(os.path.join(pipeline_root, '.config.json'), 'wb+') as f:
        tf.io.write_file(f, json.dumps(config.to_json_dict()))


if __name__ == '__main__':
    generate_config()
