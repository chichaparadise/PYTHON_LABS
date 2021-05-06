from src.Factory import SerializerFactory as sf

class Serializer():

    def __init__(self, path, extension='json'):
        self.extension = extension
        self.factory = sf.SerializerFactory(path)
        self.serializer = self.factory.create_serializer(extension)

    def dump(self, obj):
        self.serializer.dump(obj)

    def dumps(self, obj):
        return self.serializer.dumps(obj)

    def load(self):
        return self.serializer.load()

    def loads(self, obj_str):
        return self.serializer.loads(obj_str)