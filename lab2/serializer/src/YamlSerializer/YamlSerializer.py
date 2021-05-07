from src.packer import packer, unpacker
from io import StringIO
import yaml


class YamlSerializer:
    def __init__(self, path: str):
        self.path = path
        self.packer = packer.Packer()
        self.unpacker = unpacker.Unpacker()

    def dump(self, obj: object):
        obj_dict = self.packer.pack(obj)
        with open(self.path, "w") as file:
            yaml.dump(obj_dict, file)

    def dumps(self, obj: object):
        obj_dict = self.packer.pack(obj)
        result_string = yaml.dump(obj_dict)
        return result_string

    def load(self):
        obj_dict = {}
        with open(self.path, "r") as file:
            obj_dict = yaml.safe_load(file)
        obj = self.unpacker.unpack(obj_dict)  # may be make both packer and unpacker callable
        return obj

    def loads(self, obj_str: str):
        str_stream = StringIO(obj_str)
        obj_dict = yaml.safe_load(str_stream)
        obj = self.unpacker.unpack(obj_dict)
        return obj
