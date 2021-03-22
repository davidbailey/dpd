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
        "astropy",
        "bs4",
        "flask",
        "folium",
        "geonetworkx",
        "geopandas",
        "gtfs_kit",
        "ipfn",
        "matplotlib",
        "mesa",
        "movingpandas",
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
        "werkzeug",
    ],
    tests_requires=["black", "coveralls", "pytest", "pytest-cov"],
)
