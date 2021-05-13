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
        obj = object
        index = 0
        while index < len(string):
            if string[index] == '{':
                obj = {}
                key = self.decode(string[index + 1 : string.find(':')])
                index = string.find(':') + 1
                end_index = string.find('}') if string.find(',') == -1 else string.find(',')
                value = self.decode(string[index : end_index])
                obj[key] = value
                index = end_index
            if string[index] == '[':
                obj = []
                end_index = string.find(']') if string.find(',') == -1 else string.find(',')
                value = self.decode(string[index + 1 : end_index])
                obj.append(value)
                index = end_index
            if string[index] == '"':
                end_index = string.find('"')
                obj = string[index + 1 : end_index]
                index = end_index
            if string[index].isnumeric():
                end_index = index + 1
                num_type = int
                while(True):
                    if string[end_index] == '.' and string[end_index + 1].isnumeric():
                        num_type = float
                    elif string[end_index].isnumeric():
                        num_type = int
                    else:
                        end_index -= 1
                        break
                    end_index += 1
                obj = int(string[index : end_index]) if num_type is int else float(string[index : end_index])
                index = end_index
            if string[index : index + 3] == 'true':
                end_index = index + 3
                obj = True
                index = end_index
            if string[index : index + 4] == 'false':
                end_index = index + 4
                obj = False
                index = end_index
            if string[index : index + 3] == 'null':
                end_index = index + 3
                obj = None
                index = end_index
            index += 1
        return obj

a = JsonParser()
di = {"False":None, 'b':[True, "name", 5.5, 4], "a":2}
# s = a.encode(d)
with open('testin.json', 'w') as file:
    a.dump(di, fp=file)
# print(s)