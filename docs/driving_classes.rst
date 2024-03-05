Driving Classes
=======


.. uml:: dpd.driving
   :classes:
	


How did we get here?
A little history: the goal has always been to compute a trip given a route. 

1. The first model was the simplest: time = distance / speed. However, this model does not include acceleration and deceleration so it is not possible to compute the result of adding or removing a stop.
2. The next model included a stop penalty. This is more realistic, but still ignores factors like changing speed limits. Also, many vehicles do not have uniform acceleration/deceleration.
3. The current model is based on a dynamic body simulation: instead of computing with a few formulas, this version simulates a vehicle that will speed up, slow down, etc. This works well for modeling stops, speed limits, traffic, etc.

Network
-----------

* Extends dict


Schedule
-----------
* Extends pandas.DataFrame


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
* Extends geopandas.GeoDataFrame

Trips
-----------

* Extends dict
