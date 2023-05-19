# ./gptfx/pipeline/configs.py
import json
import os
from typing import Dict, Any

import tensorflow as tf
from tfx.utils.json_utils import Jsonable

_BASE_DIR = os.path.dirname(os.path.abspath(os.getcwd()))
_PIPELINE_NAME = 'gptfx_pipeline'
_PIPELINE_ROOT = os.path.join(_BASE_DIR, 'pipelines', _PIPELINE_NAME)
_DATA_ROOT = os.path.join(_PIPELINE_ROOT, 'data')
_METADATA_ROOT = os.path.join(_PIPELINE_ROOT, 'metadata')
_MODULE_FILE = os.path.join(_BASE_DIR, 'gptfx', 'components', 'transform_components', 'autogpt_utils.py')


class Config(Jsonable):
    def __init__(
        self,
        pipeline_name: str = None,
        pipeline_root: str = None,
        data_root: str = None,
        metadata_root: str = None,
        log_root: str = None,
        module_file: str = None
    ):
        super(Config).__init__()
        self.pipeline_name = pipeline_name
        self.pipeline_root = pipeline_root
        self.data_root = data_root
        self.metadata_root = metadata_root
        self.log_root = log_root
        self.module_file = module_file

    def __str__(self):
        return f'Config(pipeline_name={self.pipeline_name}, pipeline_root={self.pipeline_root}, data_root=' \
               f'{self.data_root}, metadata_root={self.metadata_root}, module_file={self.module_file})'

    def __repr__(self):
        return self.__str__()


def from_json_dict(config_dict: Dict[str, Any]) -> Config:
    config = Config()
    return config.from_json_dict(config_dict)


def to_json_dict(config: Config) -> Dict[str, Any]:
    return config.to_json_dict()


def get_config(path: str = None, **kwargs) -> Config:
    if kwargs and not path:
        return Config(**kwargs)
    elif path and not kwargs:
        config = Config()
        with tf.io.gfile.GFile(path, 'rb+') as f:
            json_dict = json.load(f)
        return config.from_json_dict(json_dict)
    else:
        raise ValueError('Either path or kwargs must be provided, but not both.')
