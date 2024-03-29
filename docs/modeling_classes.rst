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
* Index (string) an identifier for each zone (origin)
* Columns (string) an identifier for each zone (destination)
* Uses

  * Contains the distance from each zone to each zone. Distance can be straight line (e.g. meters) or via some other algorithm (e.g. walking time)
  * May or may not be symmetric (maybe you take a different route from 1 to 2 as from 2 to 1)

.. csv-table:: Example DistanceDataFrame
   :header: "Index", "(To) Zone 1", "(To) Zone 2", "(To) Zone 3"

   "(From) Zone 1", "N/A", "10 miles", "10 km"
   "(From) Zone 2", "10 miles", "N/A", "2 miles"
   "(From) Zone 3", "10 km", "2 miles", "N/A"

TripDataFrame
-----------

* Extends pandas.DataFrame
* Index (string) an identifier for each zone (origin)
* Columns (string) an identifier for each zone (destination)
* Uses

  * Contains the number of trips from each zone to each zone.
  * May or may not be symmetric

.. csv-table:: Example TripDataFrame
   :header: "Index", "(To) Zone 1", "(To) Zone 2", "(To) Zone 3"

   "(From) Zone 1", "N/A", "20 trips", "10 trips"
   "(From) Zone 2", "10 trips", "N/A", "2 trips"
   "(From) Zone 3", "20 trips", "2 trips", "N/A"

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

.. csv-table:: Example Population
   :header: "Index", "origin", "destination"

   "0", "Zone 1", "Zone 2"
   "1", "Zone 1", "Zone 2"
   "2", "Zone 3", "Zone 4"

ContourDataFrame
-----------

* Extends geopandas.GeoDataFrame
* Index - an identifier for each contour line
* Columns

  * geometry (shapely.Polygon) the geometry for each contour line
  * title (string) an identifier for each contour line

* Uses

  * Plotting contour lines around points

.. csv-table:: Example ContourDataFrame
   :header: "Index", "geometry", "title"

   "0", "Polygon", "<5 minutes"
   "1", "Polygon", "5-10 minutes"
   "2", "Polygon", "10-15 minutes"
