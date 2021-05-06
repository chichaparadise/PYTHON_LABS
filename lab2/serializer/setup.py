#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name='src',

    packages=['src', 'src/Factory', 'src/JsonSerializer', 'src/packer', 'src/YamlSerializer',
              'src/TomlSerializer', 'src/PickleSerializer'],
    version='1.0.0',

    description='Serializer/Deserializer',
    author='BigDickClub',
    license='Apache',
    python_requires='>=3.8.5',
)

import os
from pathlib import Path

home = str(Path.home())

os.system('rm -rf ~/ser')
os.system('mkdir ~/ser')
os.system('cp -a . ~/ser')

os.system('chmod +x ~/ser/redump.py')
with open(home + '/.bashrc', 'a') as file:
    file.write("alias redump='" + "~/ser/redump.py'" + '\n')

