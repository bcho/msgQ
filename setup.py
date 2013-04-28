#!/usr/bin/env python

from setuptools import setup

import msgQ

with open('requirements.txt', 'r') as f:
    install_requires = [i.strip() for i in f.readlines()]


setup(name=msgQ.__name__,
      version=msgQ.__version__,
      description='System wide message queue',
      author='hbc',
      author_email='bcxxxxxx@gmail.com',
      packages=[
          'msgQ',
      ],
      entry_points={
          'console_scripts': [
              'msgqd=msgQ.cli:main',
          ]
      },
      install_requires=install_requires)
