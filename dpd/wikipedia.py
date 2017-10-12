import bs4
import requests
import pandas

def get_wikipedia_table(url, number):
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r._content, 'html.parser')
    columns = list(map(bs4.element.Tag.getText, soup.find_all('table')[number].find_all('tr')[0].find_all(['td', 'th'])))
    rows = list(map(lambda row: list(map(bs4.element.Tag.getText, row.find_all(['td', 'th']))), soup.find_all('table')[number].find_all('tr')))
    dataframe = pandas.DataFrame(rows, columns=columns)
    dataframe.drop(0, inplace=True)
    return dataframe
