#!/usr/bin/env python

from setuptools import setup

setup(name='DPD',
      version='0.25',
      description='A Python Transportation Toolkit',
      author='David Bailey',
      author_email='david@davidabailey.com',
      url='https://github.com/davidbailey/dpd',
      packages=['dpd'],
      license='Public Domain',
      install_requires=['geopandas', 'requests', 'shapely', 'bs4', 'pandas', 'gtfstk', 'pyproj', 'folium', 'matplotlib', 'mplleaflet']
)
