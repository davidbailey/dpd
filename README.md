# dpd

dpd is a growing library of transportation-related functions. Currently it is useful for plotting population, employee, and job densities and public transportation accessibility. There are also functions for computing a cost-benefit analysis and multiple-criteria analysis.

Install
--------

```bash
pip install git+https://github.com/davidbailey/dpd.git
```

Examples
--------

http://nbviewer.jupyter.org/github/davidbailey/dpd/blob/master/dpd.ipynb

```
data = {'Total Population': 'DP02_0086E', 'White': 'DP05_0059E', 'Black': 'DP05_0060E', 'Indian': 'DP05_0061E', 'Asian': 'DP05_0062E', 'Islander': 'DP05_0063E', 'Other': 'DP05_0064E', 'Hispanic': 'DP05_0066E'}
df = dpd.get_uscensus_data_by_tract('2016', '06', '037', data)
```

```
from dpd import CostBenefitAnalysis

discount_rate=.03
start_year=2017
duration=3 # years

cba = CostBenefitAnalysis(start_year=start_year, duration=duration)
cba.add_cost(name='cost 1', value=10, start_year=start_year, duration=2)
cba.add_cost(name='cost 2', value=10, start_year=start_year, duration=2)
cba.add_benefit(name='benefit 1', value=20, start_year=start_year + 1, duration=2)
cba.add_benefit(name='benefit 2', value=20, start_year=start_year + 1, duration=2)

# cba_table = cba.to_dataframe().T # in year of expenditure 
cba_table = cba.discount(start_year, discount_rate).T
print('Benefit-cost ratio: ', cba_table['Sum']['Benefits Total'] / cba_table['Sum']['Costs Total'])
cba_table
```

Documentation
--------

GTFS
* url2gtfs(string: url)
    * url is the URL of a GFTS file
    * Returns a gtfstk.feed.Feed
* get_rail_stops(gtfstk.feed.Feed: gtfs)
    * gtfs is the the FTFS object from url2gtfs (or gtfstk) that you would like to get only the rail stops from
    * Returns a pandas.core.frame.DataFrame
* plot_stops(folium.folium.Map: foliumMap, pandas.core.frame.DataFrame: stops, string: markercolor)
    * foliumMap is the map to plot the stops on
    * stops is the DataFrame that contains the stops from url2gtfs().stops or get_rail_stops
    * color is a string of the marker color for the stops
    * Returns pandas.core.series.Series of folium.map.Marker
    * This method requires a OSRM server of the area running on http://localhost:5000

Overpass
* query2elements(string: query, [element_type: string, string: endpoint])
  * string is an [Overpass API](https://wiki.openstreetmap.org/wiki/Overpass_API/Language_Guide) [wiki.openstreetmap.org] query string
  * element_type is rels (default), ways, nodes
  * endpoint is an Overpass API endpoint
  * Test queries at [overpass turbo](http://overpass-turbo.eu) [overpass-turbo.eu]
  * Returns dict

US Census
* get_uscensus_data_by_tract
* get_uscensus_geometry
* add_density_to_tracts
* get_uscensus_density_by_tract

Wikipedia
* get_wikipedia_table(string: url, int: number)
    * url is the URL of the Wikipedia page that contains the table
    * this function should also work for any page with a table
    * number is the number of the table on the page. e.g. if it is the first (or only) table on the page, number is 0.
    * Returns a pandas.core.frame.DataFrame
