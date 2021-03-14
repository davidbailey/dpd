#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="dpd",
    version="0.58",
    description="A Python Transportation Toolkit",
    author="David Bailey",
    author_email="david@davidabailey.com",
    url="https://github.com/davidbailey/dpd",
    packages=find_packages(),
    license="Public Domain",
    install_requires=[
        "bs4",
        "flask",
        "folium",
        "geopandas",
        "gtfs_kit",
        "ipfn",
        "matplotlib",
        "mesa",
        "mplleaflet",
        "networkx",
        "numpy",
        "pandas",
        "polyline",
        "pyrosm",
        "pyproj",
        "requests",
        "shapely",
        "us",
    ],
    tests_requires=["black", "coveralls", "pytest", "pytest-cov"],
)
