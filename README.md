# dpd

[![Build Status](https://github.com/davidbailey/dpd/actions/workflows/main.yml/badge.svg)](https://github.com/davidbailey/dpd/actions/workflows/main.yml)
[![Coverage Status](https://coveralls.io/repos/github/davidbailey/dpd/badge.svg?branch=trunk)](https://coveralls.io/github/davidbailey/dpd?branch=trunk)
[![Documentation Status](https://readthedocs.org/projects/dpd/badge/?version=latest)](https://dpd.readthedocs.io/en/latest/?badge=latest)

dpd is a growing library of transportation-related tools sorted into submodules. Please let me know if you find these tools useful or interesting.

* Analysis - a class for performing a cost-beneift analysis and a class for performing a multiple-criteria analysis. E.g. [Analysis](https://dpd.readthedocs.io/en/latest/notebooks/analysis.html)
* D3.js - functions for generating D3.js radar charts and dendrograms from python code.
* Driving - classes to calculate driving times along routes, specifically timetables for public transportation routes. E.g. [Driving](https://dpd.readthedocs.io/en/latest/notebooks/driving.html)
* Folium - an example [Folium Flask App](https://dpd.readthedocs.io/en/latest/notebooks/folium_flask_app.html)
* Geometry - functions for computing geometric operations and classes for storing geometric objects: [Geometry](https://dpd.readthedocs.io/en/latest/notebooks/geometry.html)
* Kinematics - a class for modeling a kinematic body
* Mapping - classes for creating a map. E.g. [Agent-based Transportation Model](https://dpd.readthedocs.io/en/latest/notebooks/agent-based_transportation_model.html)
* Modeling - classes for performing transportation modeling. E.g. [Agent-based Transportation Model](https://dpd.readthedocs.io/en/latest/notebooks/agent-based_transportation_model.html), [Four-step Transportation Model](https://dpd.readthedocs.io/en/latest/notebooks/four_step_transportation_model.html), and [Gravity Model](https://dpd.readthedocs.io/en/latest/notebooks/gravity_model.html)
* Open Source Routing Machine (OSRM) - functions to interact with an OSRM server
* OpenStreetMap (OSM) - a class for downloading relations, ways, and nodes from OpenStreetMap and a class for creating a map object.
* Shapely - functions for working with shapely geometries
* US Census -  functions for gathering data from the US Census. E.g. [Density and public transportation](https://dpd.readthedocs.io/en/latest/notebooks/density_and_public_transportation.html) and [Four-step Transportation Model](https://dpd.readthedocs.io/en/latest/notebooks/four_step_transportation_model.html)
* Utils - utility functions used by other submodules
* Werkzeug - a class to run a Werkzeug server in a thread.
* Wikipedia - functions for gathering data from Wikipedia. E.g. [Wikipedia](https://dpd.readthedocs.io/en/latest/notebooks/wikipedia.html)

Installation
--------

```bash
sudo apt install python3-dev libproj-dev proj-data proj-bin libgeos-dev gdal-bin libgdal-dev
pip install git+https://github.com/davidbailey/dpd.git
```

Documentation
--------

Documentation is available at https://dpd.readthedocs.io/en/latest/.
