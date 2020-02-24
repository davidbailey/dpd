# dpd

[![Build Status](https://travis-ci.com/davidbailey/dpd.svg?branch=master)](https://travis-ci.com/davidbailey/dpd)
[![Coverage Status](https://coveralls.io/repos/github/davidbailey/dpd/badge.svg?branch=master)](https://coveralls.io/github/davidbailey/dpd?branch=master)
[![Documentation Status](https://readthedocs.org/projects/dpd/badge/?version=latest)](https://dpd.readthedocs.io/en/latest/?badge=latest)

dpd is a growing library of transportation-related functions. Currently it is useful for plotting population, employee, and job densities and public transportation accessibility. There are also functions for computing a cost-benefit analysis and multiple-criteria analysis.

Installation
--------

```bash
pip install git+https://github.com/davidbailey/dpd.git
```

Documentation
--------

Documentation is available at https://dpd.readthedocs.io/en/latest/.


Examples
--------

[Cost-benefit Analysis](https://dpd.readthedocs.io/en/latest/notebooks/cba.html)


http://nbviewer.jupyter.org/github/davidbailey/dpd/blob/master/dpd.ipynb

```
data = {'Total Population': 'DP02_0086E', 'White': 'DP05_0059E', 'Black': 'DP05_0060E', 'Indian': 'DP05_0061E', 'Asian': 'DP05_0062E', 'Islander': 'DP05_0063E', 'Other': 'DP05_0064E', 'Hispanic': 'DP05_0066E'}
df = dpd.get_uscensus_data_by_tract('2016', '06', '037', data)
```

Multiple-criteria Analysis
```
from dpd.mca import MultipleCriteriaAnalysis
from dpd.d3 import radar_chart
from IPython.core.display import HTML

attributes = ['Cost', 'Time', 'Comfort']
alternatives = ['Tram', 'Bus']
mca = MultipleCriteriaAnalysis(attributes, alternatives)
mca.mca['Tram']['Cost'] = 200
mca.mca['Bus']['Cost'] = 100
mca.mca['Tram']['Time'] =50
mca.mca['Bus']['Time'] = 100
mca.mca['Tram']['Comfort'] = 800
mca.mca['Bus']['Comfort'] = 500
legend_options, d, title = mca.to_d3_radar_chart()
HTML(radar_chart(legend_options, d, title))
```

Get a table from a Wikipedia article:
```
from dpd.wikipedia import get_wikipedia_table

df = get_wikipedia_table('https://en.wikipedia.org/wiki/List_of_10-meter_diving_platforms_in_the_United_States', 0)
```

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
