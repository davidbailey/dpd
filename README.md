# dpd

dpd is a growing library of quality functions. Currently it is useful for plotting population, employee, and job densities and public transportation accessibility.

Install
--------

```bash
pip install git+https://github.com/davidbailey/dpd.git
```

Examples
--------

http://nbviewer.jupyter.org/github/davidbailey/dpd/blob/master/dpd.ipynb

Documentation
--------

US Census
* get_uscensus_population_by_tract
* get_uscensus_geometry
* add_density_to_tracts
* get_uscensus_density_by_tract

Wikipedia
* get_wikipedia_table(string: url, int: number)
    * url is the URL of the Wikipedia page that contains the table
    * number is the number of the table on the page. e.g. if it is the first (or only) table on the page, number is 0.
    * Returns a pandas.DataFrame

GTFS
* url2gtfs
* get_rail_stops
* plot_stops
