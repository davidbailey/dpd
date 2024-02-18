Driving Classes
=======

Network
-----------

* Extends dict


Schedule
-----------
* Extends geopandas.GeoDataFrame


Route
-----------

* Extends geopandas.GeoSeries
* Index - an identifier for each Point, often just a range, but can also be e.g. a Node ID from OpenStreetMap
* Column

  * geometry (shapely.Point) each point along the route

* Uses

  * Basis for a transportation model or simulation
  * Plotting a route
  * Can be combined with Stops

.. csv-table:: Example Route with Stops
   :header: "Index", "geometry", "name"

   "0", "Point(0,0)", "Stop 1"
   "1", "Point(0,1)", ""
   "2", "Point(0,2)", "Stop 2"


Stops
-----------

* Extends geopandas.GeoSeries
* Index - same as Route - an identifier for each Point, often just a range, but can also be e.g. a Node ID from OpenStreetMap
* Column

  * name (string) the name of the location of a stop along the route, blank if the point is just for geometry


Trip
-----------

