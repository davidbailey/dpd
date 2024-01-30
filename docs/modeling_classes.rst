Modeling Classes
=======

Zones
-----------

* Extends geopandas.GeoDataFrame
* Index (string) an identifier for each zone
* Columns

  * geometry (shapely.Geometry) a geometry (typically a polygon, but could also e.g. be a centroid) for each zone
  * population (int, column name population is a suggestion, not a requirement) the number of people living, working, studying, etc. in each zone
  * area (float (e.g. square meters), column name area is a suggestion, not a requirement) the area of the zone (could be land area, or another area)
  * density (float (e.g. people/square meters), column name area is a suggestion, not a requirement) population/area

* Uses

  * Basis for a transportation model or simulation
  * Plotting geometries or population densities

.. csv-table:: Example Zones
   :header: "Index", "geometry", "population", "area", "density"

   "Zone 1", "Polygon", "1000", "10", "100"
   "Zone 2", "Polygon", "2000", "20", "100"
   "Zone 3", "Polygon", "1000", "20", "50"


DistanceDataFrame
-----------

* Extends pandas.DataFrame
* Index (string) an identifier for each zone
* Columns (string) an identifier for each zone
* Uses

  * Contains the distance from each zone to each zone. Distance can be straight line (e.g. meters) or via some other algorithm (e.g. walking time)

.. csv-table:: Example Zones
   :header: "Index", "Zone 1", "Zone 2", "Zone 3"

   "Zone 1", "N/A", "10 miles", "10 km"
   "Zone 2", "10 miles", "N/A", "2 miles"
   "Zone 3", "10 km", "2 miles", "N/A"

TripDataFrame
-----------

* Extends pandas.DataFrame
* Index (string) an identifier for each zone
* Columns (string) an identifier for each zone
* Uses

  * Contains the number of trips from each zone to each zone.

Population
-----------

* Extends pandas.DataFrame
* Index (string) an identifier for each trip
* Columns

  * Origin (string) an identifier for each origin zone
  * Destination (string) an identifier for each destination zone

* Uses

  * Contains a row for each trip
  * Expanded view of a TripDataFrame
  * Can be converted into Zones with GroupBy
  * Basis for a transportation model or simulation

ContourDataFrame
-----------

* Extends geopandas.GeoDataFrame
* Index - an identifier for each contour line
* Columns

  * geometry (shapely.Polygon) the geometry for each contour line
  * title (string) an identifier for each contour line

* Uses

  * Plotting contour lines around points
