#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="dpd",
    version="0.57",
    description="A Python Transportation Toolkit",
    author="David Bailey",
    author_email="david@davidabailey.com",
    url="https://github.com/davidbailey/dpd",
    packages=find_packages(),
    license="Public Domain",
    install_requires=[
        "geopandas",
        "requests",
        "shapely",
        "bs4",
        "pandas",
        "gtfs_kit",
        "pyproj",
        "folium",
        "matplotlib",
        "mplleaflet",
        "flask",
        "ipfn",
        "networkx",
        "mesa",
    ],
    tests_requires=["black", "coveralls", "pytest", "pytest-cov"],
)
