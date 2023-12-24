# dpd

[![Build Status](https://github.com/davidbailey/dpd/actions/workflows/main.yml/badge.svg)](https://github.com/davidbailey/dpd/actions/workflows/main.yml)
[![Coverage Status](https://coveralls.io/repos/github/davidbailey/dpd/badge.svg?branch=trunk)](https://coveralls.io/github/davidbailey/dpd?branch=trunk)
[![Documentation Status](https://readthedocs.org/projects/dpd/badge/?version=latest)](https://dpd.readthedocs.io/en/latest/?badge=latest)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

dpd is a growing library of transportation-related tools sorted into submodules. Please let me know if you find these tools useful or interesting.

## Documentation
--------

Documentation is available at https://dpd.readthedocs.io/en/latest/.

## Getting Started

### Prerequisities

```bash
apt install python3-dev libproj-dev proj-data proj-bin libgeos-dev gdal-bin libgdal-dev
```

### Installation

```bash
pip install git+https://github.com/davidbailey/dpd.git
```

### Testing

```bash
black --check .
isort --check --profile black .
bandit -r .
flake8
python -m pytest tests/
```

### Usage

* Analysis - The starting point is a decision - made up of one or more alternatives (e.g. Should we build a train, bus, bike path, or nothing?). Each alternative is made up of one or mote activities (e.g. design, build, operations, maintenance) which each have a start time, end time, cost, and benefit. The alternative class has the ability to compute a benefit-cost ratio, plot cash flow diagrams and create timelines. The decision class compares alternatives via multiple-criteria analysis. These tools show the relative merits (pros and cons) for each alternative. E.g. [Analysis](https://dpd.readthedocs.io/en/latest/notebooks/analysis.html)

The two primary sources for cost/benefit information are Driving and Modeling.

* Driving - Driving includes a route class to describe the physical geometry a transportation route (air, sea, road, or rail). A route has stops which can be used to calculate accessibility. A route can be driven to generate a trip (a time-indexed geometric series). A trip can be expanded to create a schedule. All of these classes relate closely to GTFS data structures. As mentioned, routes, trips, schedules, etc. all have design/build/operations/maintenance costs/benefits/timelines. The general idea is the user should be able to click on a few points, select a vehicle, and the class should output a cost estimate and timetable. E.g. [Driving](https://dpd.readthedocs.io/en/latest/notebooks/driving.html)

* Modeling - Modeling contains an Agent-based Transportation Model and a Four-step Transportation Model. These models should be able to answer questions about transportation supply and demand. They should also be able to answer second level questions about safety, equity, pollution, etc. E.g. [Agent-based Transportation Model](https://dpd.readthedocs.io/en/latest/notebooks/agent-based_transportation_model.html), [Four-step Transportation Model](https://dpd.readthedocs.io/en/latest/notebooks/four_step_transportation_model.html), and [Gravity Model](https://dpd.readthedocs.io/en/latest/notebooks/gravity_model.html)

There are also several supporting submodules that can be used by the above modules and can be used on their own.

* Folium - an example [Folium Flask App](https://dpd.readthedocs.io/en/latest/notebooks/folium_flask_app.html)
* Geometry - functions for computing geometric operations and classes for storing geometric objects: [Geometry](https://dpd.readthedocs.io/en/latest/notebooks/geometry.html)
* Mechanics - a class for modeling a kinematic body - this is used by both Driving and Modeling
* Geopandas - functions for working with geopandas GeoDataFrames
* Mapping - classes for creating a map. E.g. [Agent-based Transportation Model](https://dpd.readthedocs.io/en/latest/notebooks/agent-based_transportation_model.html)
* Open Source Routing Machine (OSRM) - functions to interact with an OSRM server
* OpenStreetMap (OSM) - a class for downloading relations, ways, and nodes from OpenStreetMap and a class for creating a map object.
* Shapely - functions for working with shapely geometries
* US Census -  functions for gathering data from the US Census. E.g. [Density and public transportation](https://dpd.readthedocs.io/en/latest/notebooks/density_and_public_transportation.html) and [Four-step Transportation Model](https://dpd.readthedocs.io/en/latest/notebooks/four_step_transportation_model.html)
* Utils - utility functions used by other submodules
* Werkzeug - a class to run a Werkzeug server in a thread.
* Wikipedia - functions for gathering data from Wikipedia. E.g. [Wikipedia](https://dpd.readthedocs.io/en/latest/notebooks/wikipedia.html)

## License
This project is licensed under the [MIT License](LICENSE.md).
