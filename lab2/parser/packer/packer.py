import types
import inspect
import builtins
import importlib
import json
import dis

def get_codeobject_attrs(obj):
    if isinstance(obj, types.CodeType):
        obj_dict = {}
        for key in dir(obj):
            if key.startswith('co_'):
                value = obj.__getattribute__(key)
                # if key == 'co_lnotab' or key == 'co_code':
                #     value = [byte for byte in value]
                if key == 'co_consts':
                    consts = []
                    for item in value:
                        val = get_codeobject_attrs(item)
                        consts.append(val if val else item)
                    value = tuple(consts)
                obj_dict[key] = value
        return obj_dict

def unpack_codeobject(obj_dict):
    code_obj = types.CodeType(obj_dict['co_argcount'],
                      obj_dict['co_posonlyargcount'],
                      obj_dict['co_kwonlyargcount'],
                      obj_dict['co_nlocals'],
                      obj_dict['co_stacksize'],
                      obj_dict['co_flags'],
                      obj_dict['co_code'],
                      obj_dict['co_consts'],
                      obj_dict['co_names'],
                      obj_dict['co_varnames'],
                      obj_dict['co_filename'],
                      obj_dict['co_name'],
                      obj_dict['co_firstlineno'],
                      obj_dict['co_lnotab'],
                      obj_dict['co_freevars'],
                      obj_dict['co_cellvars']
                      )
    return code_obj
                      
def pack(obj):
    obj_dict = {}
    if type(obj) in (int, float, str, bool):
        if type(obj) == int:
            obj_dict['type'] = 'int'
            obj_dict['data'] = obj
            return obj_dict
        elif type(obj) == float:
            obj_dict['type'] = 'float'
            obj_dict['data'] = obj
            return obj_dict
        elif type(obj) == bool:
            obj_dict['type'] = 'bool'
            obj_dict['data'] = obj
            return obj_dict
        elif type(obj) == str:
            obj_dict['type'] = 'str'
            obj_dict['data'] = obj
            return obj_dict

    if type(obj) in (dict, list, tuple, set, frozenset):
        if isinstance(obj, dict):
            obj_dict['type'] = 'dict'
            obj_dict['data'] = {key : pack(val) for key, val in obj.items()}
            return obj_dict
        if isinstance(obj, list):
            obj_dict['type'] = 'list'
            obj_dict['data'] = [pack(el) for el in obj]
            return obj_dict
        if isinstance(obj, tuple):
            obj_dict['type'] = 'tuple'
            obj_dict['data'] = [pack(el) for el in obj]
            return obj_dict
        if isinstance(obj, list):
            obj_dict['type'] = 'set'
            obj_dict['data'] = [pack(el) for el in obj]
            return obj_dict
        if isinstance(obj, list):
            obj_dict['type'] = 'frozenset'
            obj_dict['data'] = [pack(el) for el in obj]
            return obj_dict

    if isinstance(obj, bytes):
        obj_dict['type'] = 'bytes'
        obj_dict['data'] = [byte for byte in obj]
        return obj_dict

    if isinstance(obj, bytearray):
        obj_dict['type'] = 'bytearray'
        obj_dict['data'] = [byte for byte in obj]
        return obj_dict

    if isinstance(obj, types.CodeType):
        obj_dict['type'] = 'codeobject'
        obj_dict['data'] = pack(get_codeobject_attrs(obj))
        # result = pack(obj_dict)
        return obj_dict
    
    if isinstance(obj, types.FunctionType):
        obj_dict['type'] = 'function'
        obj_dict['data'] = pack(pack_function(obj))
        # result = pack(obj_dict)
        return obj_dict

    if isinstance(obj, types.BuiltinFunctionType):
        obj_dict['type'] = 'builtinfunction'
        obj_dict['data'] = pack(pack_builtinsfunc(obj))
        # result = pack(obj_dict)
        return obj_dict

#add unpacking of codeobject
#add unpacking of codeobject
def unpack(obj_dict):
    obj = object
    try:
        t = obj_dict['type']
    except:
        KeyError
        return

    if t in ('int', 'float', 'bool', 'str'):
        if t == 'int':
            return int(obj_dict['data'])
        if t == 'float':
            return float(obj_dict['data'])
        if t == 'bool':
            return bool(obj_dict['data'])
        if t == 'str':
            return str(obj_dict['data'])    #excess
        
    if t in ('dict', 'list', 'tuple', 'set', 'frozenset'):
        if t == 'dict':
            tmp = {key : unpack(val) for key, val in obj_dict['data'].items()}
            if 'type' in tmp.keys():
                if 'data' in tmp.keys():
                    return unpack(tmp['data'])
            return tmp
        if t == 'list':
            return [unpack(el) for el in obj_dict['data']]
        if t == 'tuple':
            o = [unpack(el) for el in obj_dict['data']]
            return tuple(o)
        if t == 'set':
            o = [unpack(el) for el in obj_dict['data']]
            return set(o)
        if t == 'frozenset':
            o = [unpack(el) for el in obj_dict['data']]
            return frozenset(o)

    if t == 'bytes':
        return bytes(obj_dict['data'])

    if t == 'codeobject':
        obj = unpack_codeobject(unpack(obj_dict['data']))
        return obj

    if t == 'function':
        obj = unpack_function(unpack(obj_dict['data']))
        return obj

    if t == 'builtinfunction':
        obj = unpack_builtinsfunc(unpack(obj_dict['data']))
        return obj

def rec_unpack(obj_dict, final_dict):
    if(isinstance(obj_dict, dict)):
        for key, val in obj_dict.items():
            rec_unpack(val, final_dict)
            final_dict[key] = unpack(val) if unpack(val) != None else val

def pack_builtinsfunc(obj):
    obj_dict = {}
    obj_dict['type'] = 'builtinfunction'
    obj_dict['module'] = obj.__module__
    obj_dict['attributes'] = {'__name__' : obj.__name__}
    return obj_dict

def unpack_builtinsfunc(obj_dict):
    module = importlib.import_module(obj_dict['module'])
    obj = getattr(module, obj_dict['attributes']['__name__'])
    return obj

def pack_function(obj):
    obj_dict = {}
    attrs = {}
    globs = {}
    attrs['__name__'] = obj.__qualname__
    attrs['__defaults__'] = obj.__defaults__
    attrs['__closure__'] = obj.__closure__  

    code_dict = {}
    # for code_attr in dir(obj.__code__):
    #         if code_attr.startswith('co_'):
    #             code_dict[code_attr] = obj.__code__.__getattribute__(code_attr)
    # attrs['__code__'] = code_dict
    attrs['__code__'] = obj.__code__
    global_ns = {}
    get_closure_globs(obj.__code__, global_ns)
    obj_dict['__globals__'] = global_ns
    obj_dict['attributes'] = attrs
    return obj_dict


def get_closure_globs(code_obj, globs):
    if isinstance(code_obj, types.CodeType):
        for var in code_obj.co_consts:
            get_closure_globs(var, globs)
            mod = importlib.import_module(__name__)
        for name in code_obj.co_names:
            if name in dir(mod):
                    globs[name] = getattr(mod, name)
            elif name in dir(builtins):
                globs[name] = getattr(builtins, name)

def unpack_function(obj_dict):
    attrs = obj_dict['attributes']
    obj = types.FunctionType(code=attrs['__code__'],
                             globals=obj_dict['__globals__'],
                             name=attrs['__name__'],
                             argdefs=attrs['__defaults__'],
                             closure=attrs['__closure__'])
    # obj.__module__ = obj_dict['module']
    return obj

def fuck(name): print('fuck you, ', name)

dic = pack(fuck)
# print(dict)
# b = pack(print)
# print(b)



# class MyMeta(type):
#     def __new__(cls, classname, supers, dict):
#         print("in metaclass __new__ method")
#         return type.__new__(cls, classname, supers, dict)
#     def __init__(cls, classname, supers, dict):
#         print("in metaclass __init__ method")

def dec(func):
    def wrap(*args, **kwargs):
        print("in", func.__name__)
        return func(*args, **kwargs)
    return wrap


# class Example(metaclass=MyMeta):
#     data = 1
#     self_dict = {}
#     def __init__(self):
#         self.b = 3
#     def f(self, name):
#         print("fuck off", name)
#     @staticmethod
#     def hi(self): pass
#     @classmethod
#     def clf(self):pass
#     def decf(self):pass
#     decf = dec(decf)

# n_d = pack_function(MyMeta.__new__)
# n = unpack_function(n_d['attributes'])
# i_d = pack_function(MyMeta.__init__)
# i = unpack_function(i_d['attributes'])

# b = type('MyM', (type, ), {'__init__' : i, '__new__' : n})



# d = {attr : getattr(MyMeta, attr) for attr in MyMeta.__dict__ if not attr.startswith('__')}
# print(d)

# f_d = pack_function(Example.f)
# f = unpack_function(f_d['attributes'])

# a = b('Ex', (), {'data' : 1, 'self_dict' : {}, 'f' : f})

# print(a.__class__)
# print([attr for attr in Example.__dict__ if not attr.startswith('__')])

def inst(obj):
    if type(obj) == type(type):
        print("True")
    else:
        l = str(type(obj)).strip("'><'").split('.')
        print(l[1])

# def sayhi(name):
#     print("hi", name)

def pack_type(obj):
    obj_dict = {}
    obj_dict['type'] = 'type'
    attrs = {}
    for key, value in obj.__dict__.items():
        if key == '__module__':
            obj_dict[key] = value
        else:
            attrs[key] = pack(value)
        
#pack_type(Example)
# print(*[attr for attr in inspect.getmembers(Example, lambda a: not(inspect.isroutine(a)))], sep='\n')

# print(Example.__dict__)


x = lambda n : n ** 3
zhop = 4
def hi():
    a = 2
    def clos():
        global x
        global zhop
        nonlocal a
        f = x(zhop)
        return f*a
    return clos


def get_codeobject_attrs(obj):
    if isinstance(obj, types.CodeType):
        obj_dict = {}
        for key in dir(obj):
            if key.startswith('co_'):
                value = obj.__getattribute__(key)
                obj_dict[key] = value
        return obj_dict

# d = pack(sayhi)
# c = pack(hi.__code__)

a = None
with open('out.json', 'r') as file:
    a = json.load(file)

o = unpack(a)
o('sveta')
# with open("out.json", "w") as writer:
#     print(b, a, e, sep='\n\n\n', file=writer)
# print(b()())
# print(*[attr for attr in inspect.getmembers(hi.__code__.co_consts[2], lambda a:not(inspect.isroutine(a)))], sep='\n')
# print(*[attr for attr in inspect.getmembers(hi.__code__, lambda a:not(inspect.isroutine(a)))], sep='\n')

# print(inspect.getclosurevars(hi.__code__.co_varnames[0]))


# print(hi.__code__.co_consts[2])

# pack_type(Example)

# print(*[attr for attr in inspect.classify_class_attrs(Example) if not inspect.isroutine(attr)], sep='\n')

# print(types.FunctionType)
# print(Example.__dict__)

# inst(a)
# dic = pack_function(len)
# a = unpack_function(dic)
# print(a(dic))


# class singleton:
#     def __init__ (self, aClass) : # При декорировании @
#         self.aClass = aClass
#         self.instance = None
#     def __call__ (self, *args, **kwargs) : # При создании экземпляров
#         if self.instance == None:
#             self.instance = self.aClass(*args, **kwargs) # Один экземпляр # на класс
#         return self.instance

# def singleton(aClass): # При декорировании @
#     instance = None
#     def onCall(*args, **kwargs): # При создании экземпляров
#         nonlocal instance # Оператор nonlocal в Python З.Х
#         if instance == None:
#             instance = aClass(*args, **kwargs) # Одна объемлющая область
# # видимости на класс
#         return instance
#     return onCall