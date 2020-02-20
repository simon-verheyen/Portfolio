#
# Script only needs to be run once to setup basis and every ... long periode... to update
#
# First function requests the available sources from newsapi and creates data-frame for it
# Second function takes all country codes and names from UN website and creates data-frame or it
# Third function finds available  countries for newsapi and creates subset of global-country data-frame for this
#
# All data-frames are saved:
#   Format msgpack, for efficiency (both time and computational intensity)
#   Readable for all(?) other languages
#

""" Still need to find an efficient way to deal with aliases """
""" Check which countries are missing from newsapi country db and why -> tw (taiwan) & hk (hong kong)"""
""" Need a better all_country collection """

import requests
import pandas as pd
from bs4 import BeautifulSoup
from newsapi import NewsApiClient


# Requests sources from NewsAPI, puts the info in a data-frame and saves as csv
def create_newsapi_sources_database():
    newsapi = NewsApiClient(api_key='6452f6e1b7bf430eb07477bbe23353c4')
    sources = newsapi.get_sources()

    if sources['status'] == 'ok':
        df_sources = pd.DataFrame(sources['sources'])
        df_sources.to_csv('data_newsapi_sources', index=False)


# Communicates with UN webpage, extracts all country names, ISO2- and ISO3 codes
# Combines this information in a data-frame and saves as csv
def create_all_countries_database():
    url = 'http://www.fao.org/countryprofiles/iso3list/en/'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    country_info = [('name', []), ('official_name', []), ('ISO2', []), ('ISO3', [])]

    table = soup.find_all('table')
    table_rows = table[0].find_all('tr')
    i = 0

    for tr in table_rows:
        if i == 0:
            i += 1
            continue

        td = tr.find_all('td')
        name = td[0].text.strip()

        if not name.find('(') == -1:
            name = name.partition('(')[0].lower()

        all_names = [name, td[1].text.strip().lower(), td[3].text.strip().lower(), td[2].text.strip().lower()]

        for i in range(4):
            country_info[i][1].append(all_names[i])

    # Transforms the list of tuples into a dict
    Dict = {title: column for (title, column) in country_info}

    # Transforms the dict into a pandas data-frame
    df_countries = pd.DataFrame(Dict)
    df_countries.to_csv('data_all_country', index=False)


# Communicates with NewsAPI page containing all possible countries to search.
# Takes these countries makes a subset of the data found on th UN page
def create_newsapi_countries_database():
    url = 'https://newsapi.org/sources'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    content_divs = soup.findAll('kbd')
    names = []

    for a in content_divs:
        names.append(a.text.strip().lower())

    df_all_countries = pd.read_csv('data_all_country')
    df_newsapi_countries = df_all_countries.loc[df_all_countries['ISO2'].isin(names)].reset_index()

    for i in range(df_newsapi_countries.shape[0]):
        print(names[i] + ' ' + df_newsapi_countries.at[i, 'ISO2'])

    df_newsapi_countries.to_csv('data_newsapi_country', index=False)


# Only needs to run once to create databases
# Need to create update function to call every period o time to update databases for changes
def main():
    create_newsapi_sources_database()
    create_all_countries_database()
    create_newsapi_countries_database()


if __name__ == '__main__':
    main()
