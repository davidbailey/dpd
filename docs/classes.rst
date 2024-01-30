Classes

Zones
* Extends GeoDataFrame
* Index (string) an identifier for each zone
* Columns
  * geometry (shapely.Geometry) a geometry (typically a polygon, but could also e.g. be a centroid) for each zone
  * population (int, column name population is a suggestion, not a requirement) the number of people living, working, studying, etc. in each zone
  * area (float (e.g. square meters), column name area is a suggestion, not a requirement) the area of the zone (could be land area, or another area)
  * density (float (e.g. people/square meters), column name area is a suggestion, not a requirement) population/area
* Uses
  * Basis for a transportation model or simulation
  * Plotting geometries or population densities

