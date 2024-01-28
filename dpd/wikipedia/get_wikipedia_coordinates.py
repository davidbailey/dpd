"""
wikipedia: a collection of functions to make interacting with wikipedia easier
"""

import bs4
import requests


def get_wikipedia_coordinates(url, timeout=60):
    """
    Get the latitude, longitude coordinates from a wikipedia page and return it as a tuple.

    Args:
        url (str): the url of the wikipedia page from which to get the coordinates

    Returns:
        (latitude, longitude): a tuple containing the coordinates
    """
    request = requests.get(url, timeout=timeout)
    soup = bs4.BeautifulSoup(request.content, "html.parser")
    if soup.find_all("span", attrs={"class": "latitude"}):
        latitude = soup.find_all("span", attrs={"class": "latitude"})[0].contents[0]
    else:
        latitude = None
    if soup.find_all("span", attrs={"class": "longitude"}):
        longitude = soup.find_all("span", attrs={"class": "longitude"})[0].contents[0]
    else:
        longitude = None
    return (latitude, longitude)
