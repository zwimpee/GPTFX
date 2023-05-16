import os
from typing import Dict, Any

import tfx.v1 as tfx
import tensorflow as tf

_BASE_DIR = os.path.dirname(os.path.abspath(os.getcwd()))
_PIPELINE_NAME = 'gptfx_pipeline'
_PIPELINE_ROOT = os.path.join(_BASE_DIR, 'pipelines', _PIPELINE_NAME)
_DATA_ROOT = os.path.join(_PIPELINE_ROOT, 'data')
_METADATA_ROOT = os.path.join(_PIPELINE_ROOT, 'metadata')
_MODULE_FILE = os.path.join(_BASE_DIR, 'gptfx', 'components', 'transform_components', 'autogpt_utils.py')


class Config(tfx.utils.JsonableType):
    def __init__(
        self,
        pipeline_name: str = None,
        pipeline_root: str = None,
        data_root: str = None,
        metadata_root: str = None,
        module_file: str = None
    ):
        super(Config).__init__()
        self.pipeline_name = pipeline_name
        self.pipeline_root = pipeline_root
        self.data_root = data_root
        self.metadata_root = metadata_root
        self.module_file = module_file

    def __str__(self):
        return f'Config(pipeline_name={self.pipeline_name}, pipeline_root={self.pipeline_root}, data_root=' \
               f'{self.data_root}, metadata_root={self.metadata_root}, module_file={self.module_file})'

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def from_json_dict(json_dict: Dict[str, Any]):
        return Config(
            pipeline_name=json_dict['pipeline_name'],
            pipeline_root=json_dict['pipeline_root'],
            data_root=json_dict['data_root'],
            metadata_root=json_dict['metadata_root'],
            module_file=json_dict['module_file'],
        )

    @staticmethod
    def to_json_dict(instance: 'Config', path: str = None, store: bool = False):
        config_dict = dict(
            pipeline_name=instance.pipeline_name,
            pipeline_root=instance.pipeline_root,
            data_root=instance.data_root,
            metadata_root=instance.metadata_root,
            module_file=instance.module_file
        )
        if store:
            with tf.io.gfile.GFile(path, 'w') as f:
                tf.io.write_file(f, tf.convert_to_tensor(config_dict))
        else:
            return config_dict
