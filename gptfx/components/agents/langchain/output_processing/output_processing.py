import click
import ml_metadata.metadata_store.metadata_store
import tensorflow as tf
from absl import logging
from ml_metadata.proto import metadata_store_pb2


@click.command()
@click.option('--pipeline_name', type=str, required=True)
@click.option('--data_root', type=str, required=True)
@click.option('--metadata_root', type=str, required=True)
def main(
    pipeline_name,
    data_root: str,
    metadata_root: str,
) -> None:
    logging.basicConfig(level=logging.INFO)
    logging.info('Processing pipeline outputs for %s', pipeline_name)

    store = ml_metadata.metadata_store.metadata_store.MetadataStore(
        metadata_store_pb2.MetadataStoreClientConfig(
            database_file_path=metadata_root,
        )
    )

    context = store.get_context_by_type_and_name(
        'pipeline_run', pipeline_name
    )

    artifacts = store.get_artifacts_by_context(context.id)

    output_artifacts = [
        artifact for artifact in artifacts
        if artifact.type_id == 2
    ]

    for artifact in output_artifacts:
        with tf.io.gfile.GFile(tf.io.gfile.join(data_root, artifact.name, artifact.uri), 'wb+') as f:
            tf.io.write_file(f, artifact.get_string_custom_property('content'))


if __name__ == '__main__':
    main()