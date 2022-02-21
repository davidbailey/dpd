# dpd

[![Build Status](https://github.com/davidbailey/dpd/actions/workflows/python-app/badge.svg)]

[![Coverage Status](https://coveralls.io/repos/github/davidbailey/dpd/badge.svg?branch=trunk)](https://coveralls.io/github/davidbailey/dpd?branch=trunk)
[![Documentation Status](https://readthedocs.org/projects/dpd/badge/?version=latest)](https://dpd.readthedocs.io/en/latest/?badge=latest)

dpd is a growing library of transportation-related tools sorted into submodules. Please let me know if you find these tools useful or interesting.

* Cost-benefit analysis (CBA) - a class for performing a cost-beneift analysis. E.g. [Cost-benefit analysis](https://dpd.readthedocs.io/en/latest/notebooks/cba.html)
* D3.js - functions for generating D3.js documents from python code. Supports radar charts and dendrogram. E.g. [Multiple-criteria Analysis](https://dpd.readthedocs.io/en/latest/notebooks/mca.html)
* Driving - classes to calculate driving times along routes, specifically timetables for public transportation routes. E.g. [Driving](https://dpd.readthedocs.io/en/latest/notebooks/driving.html)
* Folium - functions for working with Folium maps. E.g. [Folium Flask App](https://dpd.readthedocs.io/en/latest/notebooks/folium_flask_app.html)
* General Transit Feed Specification (GTFS) - functions for extracting data from GTFS files and plotting schedules. E.gs. [plot_schedule](https://dpd.readthedocs.io/en/latest/notebooks/plot_schedule.html) and [Density and public transportation](https://dpd.readthedocs.io/en/latest/notebooks/density_and_public_transportation.html)
* Geometry - functions for commputing geometric operations. E.g. [Driving](https://dpd.readthedocs.io/en/latest/notebooks/driving.html)
* Mapping - classes for creating a road network map. E.g. [Agent-based Transportation Model](https://dpd.readthedocs.io/en/latest/notebooks/agent-based_transportation_model.html)
* Modeling - a set of classes for performing transportation modeling. E.g. [Agent-based Transportation Model](https://dpd.readthedocs.io/en/latest/notebooks/agent-based_transportation_model.html), [Four-step Transportation Model](https://dpd.readthedocs.io/en/latest/notebooks/four_step_transportation_model.html), and [Gravity Model](https://dpd.readthedocs.io/en/latest/notebooks/gravity_model.html)
* Multi-criteria analysis (MCA) - a class for performing multi-criteria analysis. E.g. [Multiple-criteria Analysis](https://dpd.readthedocs.io/en/latest/notebooks/mca.html)
* Open Source Routing Machine (OSRM) - functions to interact with an OSRM server
* OpenStreetMap (OSM) - a class for downloading relations, ways, and nodes from OpenStreetMap and a class for creating a road network map.
* Shapely - functions for working with shapely geometries
* US Census -  functions for gathering data from the US Census. E.g. [Density and public transportation](https://dpd.readthedocs.io/en/latest/notebooks/density_and_public_transportation.html) and [Four-step Transportation Model](https://dpd.readthedocs.io/en/latest/notebooks/four_step_transportation_model.html)
* Utils - utility functions used by other submodules
* Wikipedia - functions for gathering data from Wikipedia. E.g. [Wikipedia](https://dpd.readthedocs.io/en/latest/notebooks/wikipedia.html)

Installation
--------

```bash
pip install git+https://github.com/davidbailey/dpd.git
```

Documentation
--------

Documentation is available at https://dpd.readthedocs.io/en/latest/.
