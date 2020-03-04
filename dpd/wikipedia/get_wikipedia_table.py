"""
wikipedia: a collection of functions to make interacting with wikipedia easier
"""
import bs4
import requests
import pandas


def get_wikipedia_table(url, number=0):
    """
    Get a table from wikipedia and return it as a Pandas DataFrame.

    Args:
        url (str): the url of the wikipedia page from which to get the table
	number (int): which table on the page to return (for pages with multiple tables)

    Returns:
        pandas.DataFrame: A dataframe containing the table
    """
    request = requests.get(url)
    soup = bs4.BeautifulSoup(request.content, "html.parser")
    rows = list(
        map(
            lambda row: list(
                map(
                    lambda element: bs4.element.Tag.getText(element).rstrip(),
                    row.find_all(["td", "th"]),
                )
            ),
            soup.find_all("table")[number].find_all("tr"),
        )
    )
    dataframe = pandas.DataFrame(rows[1:], columns=rows[0])
    return dataframe
