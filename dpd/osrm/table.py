import requests


def table(origins, destinations, url_base, mode, options=""):
    url = url_base + "/table/v1/" + mode + "/" + origins + destinations + options
    r = requests.get(url)  # make this async
    return r.json()
