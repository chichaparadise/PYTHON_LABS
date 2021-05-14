import json

class JsonParser():
    def dumps(self, obj:object):
        return self.encode(obj)

    def dump(self, obj:object, fp="", indent=4):
        tokens = self.encode(obj)
        fp.write(tokens)

    def loads(self, string:str):
        return self.decode(string)[0]

    def load(self, fp=""):
        buffer = fp.read()
        return self.decode(buffer)[0]

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
                # string = string[index + 1 : string.rfind('}')] # go threw string until mett }
                # string = string[index + 1 : ]
                index += 1
                obj = {}
                while index < len(string):
                    if string[index] == '}':
                        break
                    tpl = self.decode(string[index : ])
                    if tpl[0] == None:
                        index += tpl[1]
                        continue
                    key = tpl[0]
                    index += tpl[1]
                    tpl = self.decode(string[index : ])
                    if tpl[0] == None:
                        index += tpl[1]
                        continue
                    obj[key] = tpl[0]
                    index += tpl[1] + 1
                return obj, index

            if string[index] == '[': 
                # string = string[index + 1 : string.rfind(']')]
                index += 1
                obj = []
                while index < len(string):
                    if string[index] == ']':
                        break
                    tpl = self.decode(string[index : ])
                    if tpl[0] == None:
                        index += tpl[1]
                        continue
                    obj.append(tpl[0])
                    index += tpl[1] + 1
                return obj, index
        
            if string[index] == '"':
                obj = string[index + 1 : string.find('"', index + 1)]
                return obj, index + 2 + len(obj)
        
            if string[index].isnumeric():
                end_index = index + 1
                num_type = int
                while(True):
                    if not index == len(string) - 1:
                        if string[end_index] == '.' and string[end_index + 1].isnumeric():
                            num_type = float
                    if not string[end_index].isnumeric():
                            break
                    end_index += 1
                obj = int(string[index : end_index]) if num_type is int else float(string[index : end_index])
                return obj, end_index

            if string[index : index + 4] == 'true':
                return True, index + 4

            if string[index : index + 5] == 'false':
                return False, index + 5

            if string[index : index + 4] == 'null':
                return None, index + 4

            index += 1
        return None, index

def detoken(string : str):
    ptr = 0
    while ptr < len(string):
        if string[ptr] == ' ' or string[ptr] == '\n':
            ptr += 1
            continue
        if string[ptr] == '{':
            ptr += 1
            result = detoken_dict(string[ptr : ])
            if result[0] is None:
                ptr += result[1]
                continue
            # tokens.append(result[0])
            ptr += result[1]
            return result[0], ptr
        if string[ptr] == '[':
            ptr += 1
            result = detoken_list(string[ptr : ])
            if result[0] is None:
                ptr += result[1]
                continue
            # tokens.append(result[0])
            ptr += result[1]
            return result[0], ptr
        if string[ptr] == '"':
            ptr += 1
            result = detoken_str(string[ptr : ])
            if result[0] is None:
                ptr += result[1]
                continue
            # tokens.append(result[0])
            ptr += result[1]
            return result[0], ptr
        if not ptr == len(string) - 1:
            if string[ptr] == '-' and string[ptr + 1].isnumeric():
                ptr += 1
                result = detoken_nums(string[ptr : ])
                if result[0] is None:
                    ptr += result[1]
                    continue
                # tokens.append(-1 * result[0])
                ptr += result[1]
                return -1 * result[0], ptr
        if string[ptr].isnumeric():
            result = detoken_nums(string[ptr : ])
            if result[0] is None:
                ptr += result[1]
                continue
            # tokens.append(result[0])
            ptr += result[1]
            return result[0], ptr
        if string[ptr : ptr + 5] == 'false':
            ptr += 5
            # tokens.append(False)
            return False, ptr
        if string[ptr : ptr + 4] == 'true':
            ptr += 4
            # tokens.append(True)
            return True, ptr
        if string[ptr : ptr + 4] == 'null':
            ptr += 4
            # tokens.append(None)
            return None, ptr
        ptr += 1
    return None, ptr

def detoken_dict(string : str):
    obj = {}
    ptr = 0
    while ptr < len(string):
        char = string[ptr]
        if string[ptr] == ' ' or string[ptr] == '\n':
            ptr += 1
            continue
        if string[ptr] == '}':
            ptr += 1
            break
        result = detoken(string[ptr : ])
        if result[0] is None:
            ptr += result[1]
            continue
        key = result[0]
        ptr += result[1]
        ptr = string.find(':', ptr)
        result = detoken(string[ptr : ])
        if result[0] is None:
            ptr += result[1]
            continue
        obj[key] = result[0]
        ptr += result[1]
    return obj, ptr

def detoken_list(string : str):
    obj = []
    ptr = 0
    while ptr < len(string):
        if string[ptr] == ' ' or string[ptr] == '\n':
            ptr += 1
            continue
        if string[ptr] == ']':
            ptr += 1
            break
        result = detoken(string[ptr : ])
        if result[0] is None:
            ptr += result[1]
            continue
        obj.append(result[0])
        ptr += result[1]
    return obj, ptr

def detoken_str(string : str):
    obj = ""
    ptr = 0
    while ptr < len(string):
        if string[ptr] == '"':
            ptr += 1
            break
        obj += string[ptr]
        ptr += 1
    return obj, ptr

def detoken_nums(string : str):
    obj = ""
    ptr = 0
    num_type = int
    while ptr < len(string):
        if not string[ptr].isnumeric():
            break
        if not ptr == len(string) - 1:
            if string[ptr] == '.' and string[ptr + 1].isnumeric():
                num_type = float
                continue
        obj += string[ptr]
        ptr += 1
    obj = int(obj) if num_type is int else float(obj)
    return obj, ptr

j = JsonParser()
s = object
# d = {'a' : 2, 'b' : {}}
# j.loads(j.dumps(d))
with open('out2.json', 'r') as file:
    s = json.load(file)
    print(s, "\n\n\n\n\n\n\n")
with open('out2.json', 'r') as file:
    a = file.read()
    print(detoken(a))