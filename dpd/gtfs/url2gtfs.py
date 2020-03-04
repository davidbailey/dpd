import tempfile

import gtfs_kit
import requests

def url2gtfs(url, dist_units="mi"):
    """ 
    Downloads a gtfs zip into a temp file and returns it as a gtfs_kit object.
    """
    r = requests.get(url)
    with tempfile.NamedTemporaryFile() as f:
        f.write(r._content)
        f.seek(0)  # https://stackoverflow.com/questions/10478242/temp-readline-empty
        return gtfs_kit.read_gtfs(f.name, dist_units=dist_units)
