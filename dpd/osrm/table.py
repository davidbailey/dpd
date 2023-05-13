import requests


def table(origins, destinations, url_base, mode, options="", timeout=600):
    url = url_base + "/table/v1/" + mode + "/" + origins + destinations + options
    r = requests.get(url, timeout=timeout)  # make this async
    return r.json()
