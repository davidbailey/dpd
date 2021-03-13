import requests


def route(origin, destination, url_base, mode, options="?annotations=nodes"):
    url = (
        url_base
        + "/route/v1/"
        + mode
        + "/"
        + str(origin.xy[0][0])
        + ","
        + str(origin.xy[1][0])
        + ";"
        + str(destination.xy[0][0])
        + ","
        + str(destination.xy[1][0])
        + options
    )
    r = requests.get(url)  # make this async
    return r.json()
