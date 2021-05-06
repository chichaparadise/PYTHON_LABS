from src import Serializer as sr

a = sr.Serializer('out.json', 'json')

# b = a.load()
c = sr.Serializer('out.yaml', 'yaml')
f = c.load()
f('nastya')