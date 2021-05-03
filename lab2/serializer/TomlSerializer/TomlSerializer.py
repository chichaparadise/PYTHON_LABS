from serializer.packer.packer import *
# import parser.packer.unpacker
import toml

class TomlSerializer():

    def __init__(self, path:str):
        self.path = path
        self.packer = packer.Packer()
        self.unpacker = unpacker.Unpack()

    def dump(self, obj:object):
        obj_dict = self.packer.pack(obj)
        with open(path, 'w') as file:
            toml.dump(obj_dict, file)

    def dumps(self, obj:object):
        obj_dict = self.packer.pack(obj)
        result_string = toml.dumps(obj_dict)
        return result_string

    def load(self):
        obj_dict = {}
        with open(path, 'r') as file:
            obj_dict = toml.load(file)
        obj = unpacker.unpack(obj_dict)             # may be make both packer and unpacker callable
        return obj

    def loads(self, obj_str:str):
        obj_dict = toml.loads(obj_str)
        obj = unpacker.unpack(obj_dict)
        return obj

