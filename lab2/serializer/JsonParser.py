import types

SPACES = 3 * " "

class JsonParser():
    def dumps(self, obj:object):
        return self.encode(obj)

    def dump(self, obj:object, fp="", indent=4):
        tokens = self.encode(obj)
        fp.write(tokens)

    def loads(self, string:str):
        return self.decode(string)

    def load(self, fp=""):
        buffer = fp.read()
        return self.decode(buffer)

    def encode(self, obj:object):
        tokens = []
        if(isinstance(obj, dict)):
            tokens.append('{')
            while(obj.keys()):
                key, value = obj.popitem()
                # tokens.append(SPACES)
                if not isinstance(key, str):
                    raise KeyError('Key must be a string')
                else:
                    tokens.append(self.encode(key))
                    tokens.append(': ')
                    tokens.append(self.encode(value))
                    if(obj.keys()):
                        tokens.append(', ')
            tokens.append('}')
        if(isinstance(obj, list)):
            tokens.append('[')
            while(obj):
                value = obj.pop()
                tokens.append(self.encode(value))
                if(obj):
                    tokens.append(', ')
            tokens.append(']')
        if((isinstance(obj, int) or isinstance(obj, float)) and not isinstance(obj, bool)):
            tokens.append(obj)
        if(obj in (True, False, None)):
            if obj is True:
                tokens.append('true')
            if obj is False:
                tokens.append('false')
            if obj is None:
                tokens.append('null')
        if(isinstance(obj, str)):
            tokens.append('"')
            tokens.append(obj)
            tokens.append('"')
        return ''.join(str(token) for token in tokens)


    def decode(self, string:str):
        pass