#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='DPD',
      version='0.55',
      description='A Python Transportation Toolkit',
      author='David Bailey',
      author_email='david@davidabailey.com',
      url='https://github.com/davidbailey/dpd',
      packages=find_packages(),
      license='Public Domain',
      install_requires=['geopandas', 'requests', 'shapely', 'bs4', 'pandas', 'gtfstk', 'pyproj', 'folium', 'matplotlib', 'mplleaflet']
)
