#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name="dpd",
    version="0.71",
    description="A Python Transportation Toolkit",
    author="David Bailey",
    author_email="david@davidabailey.com",
    url="https://github.com/davidbailey/dpd",
    packages=find_packages(),
    license="Public Domain",
    install_requires=[
        "astropy",
        "bs4",
        "cartopy",
        "flask",
        "folium",
        "forex_python",
        "geojsoncontour",
        "geonetworkx",
        "geopandas",
        "gtfs_kit",
        "h3",
        "haversine",
        "ipfn",
        "ipywidgets",
        "lonboard",
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
        "tobler",
        "us",
        "werkzeug",
    ],
    tests_requires=[
        "bandit",
        "black",
        "black[jupyter]",
        "coveralls",
        "flake8",
        "isort",
        "pytest",
        "pytest-cov",
    ],
)
