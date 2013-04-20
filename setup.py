#!/usr/bin/env python

from setuptools import setup

with open('requirements.txt', 'r') as f:
    install_requires = [i.strip() for i in f.readlines()]


setup(name='msgQ',
      version='0.0.1',
      description='System wide message queue',
      author='hbc',
      author_email='bcxxxxxx@gmail.com',
      packages=[
          'msgQ',
          'msgQ.server',
          'msgQ.scripts'
      ],
      entry_points={
          'console_scripts': [
              'msgq-guardd=msgQ.scripts.guard:main',
              'msgq-guard=msgQ.scripts.guard:serve',
          ]
      },
      install_requires=install_requires)
