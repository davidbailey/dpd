import numpy
import requests


def contour_plot(ax, point, resolution, number_of_points, levels=[300, 600, 900], mode="walking", url_base="http://router.project-osrm.org/route/v1/"):
    """
    Plots contour lines denoting access times to a point (e.g. public transportation station) from a region around the point
    """
    x = numpy.linspace(point.x - resolution, point.x + resolution, number_of_points)
    y = numpy.linspace(point.y - resolution, point.y + resolution, number_of_points)
    url = url_base + mode + "/" + str(point.x) + "," + str(point.y)
    for i in x:
        for j in y:
            url += ";" + str(i) + "," + str(j)
    url += "?sources=0"
    request = requests.get(url)
    durations = request.json()["durations"][0][1:]
    z = numpy.array(durations).reshape([len(x), len(y)])
    ax.contour(x, y, z, levels=levels)
