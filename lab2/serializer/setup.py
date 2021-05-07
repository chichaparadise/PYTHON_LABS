#!/usr/bin/env python
  
from setuptools import setup

setup(
    name='Serializer',
    version='Rubicon X',
    description='LR2',
    packages=['src'],
    author='BigDickClub',
    entry_points={
        'console_scripts': [
            'redump = src.redump:main'
        ]})
