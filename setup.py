#!/usr/bin/python

from setuptools import setup
import os
import shutil

setup(
  name = "bitcpy",
  version = "0.2",
  packages=['bitcpy'],
  install_requires = ['xerox>=0.2.1'],
  dependency_links = ['git://github.com/bitly/bitly-api-python.git#egg=bitly_api'],
  entry_points = {'gui_scripts' : ['bitcpy = bitcpy:main']},
  package_data = {'bitcpy' : ['bitcpy.conf']}
)
