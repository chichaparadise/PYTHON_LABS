import serializer.JsonSerializer.JsonSerializer as js
import serializer.PickleSerializer.PickleSerializer as ps
import serializer.TomlSerializer.TomlSerializer as ts
import serializer.YamlSerializer.YamlSerializer as ys

class SerializerFactory():

    def __init__(self, path:str):
        self.path = path

    def create_serializer(self, extension = 'json'):
        if extension.lower() == 'json':
            return js.JsonSerializer(path)
        elif extension.lower() == 'pickle':
            return ps.PickleSerializer(path)
        elif extension.lower() == 'toml':
            return ts.TomlSerializer(path)
        elif extension.lower() == 'yaml':
            return ys.YamlSerializer(path)