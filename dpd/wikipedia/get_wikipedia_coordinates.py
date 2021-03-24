"""
wikipedia: a collection of functions to make interacting with wikipedia easier
"""
import bs4
import requests


def get_wikipedia_coordinates(url)
    """
    Get the latitude, longitude coordinates from a wikipedia page and return it as a tuple.

    Args:
        url (str): the url of the wikipedia page from which to get the coordinates 

    Returns:
        (latitude, longitude): a tuple containing the coordinates
    """
    request = requests.get(url)
    soup = bs4.BeautifulSoup(request.content, "html.parser")
    latitude = soup.find_all("span", attrs={'class':'latitude'})[0].contents[0]
    longitude = soup.find_all("span", attrs={'class':'longitude'})[0].contents[0]
    return (latitude, longitude)


