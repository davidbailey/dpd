#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="dpd",
    version="0.66",
    description="A Python Transportation Toolkit",
    author="David Bailey",
    author_email="david@davidabailey.com",
    url="https://github.com/davidbailey/dpd",
    packages=find_packages(),
    license="Public Domain",
    install_requires=[
        "cartopy==0.19.0.post1",
        "astropy",
        "bs4",
        "flask",
        "folium",
        "geojsoncontour",
        "geonetworkx",
        "geopandas",
        "gtfs_kit",
        "ipfn",
        "matplotlib",
        "mesa",
        "movingpandas",
        "networkx",
        "numpy",
        "pandas",
        "pyrosm",
        "pyproj",
        "requests",
        "shapely",
        "us",
        "werkzeug",
    ],
    tests_requires=["bandit", "black", "coveralls", "flake8", "pytest", "pytest-cov"],
)
