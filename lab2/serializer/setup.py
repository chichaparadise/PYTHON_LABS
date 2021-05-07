#!/usr/bin/env python
  
from setuptools import setup

setup(
    name='Serializer',
    version='1.0.0',
    description='LR2',
    packages=['src', 'src/Factory', 'src/JsonSerializer', 'src/TomlSerializer', 'src/YamlSerializer', 'src/PickleSerializer', 'src/packer'],
    author='BigDickClub',
    entry_points={
        'console_scripts': [
            'redump = src.redump:main'
        ]})
