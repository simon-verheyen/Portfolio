#
# Requests sources from NewsAPI, puts the info in a data-frame and saves as csv
# Only called once
#

from newsapi import NewsApiClient
import pandas as pd


def create_newsapi_sources_database():
    newsapi = NewsApiClient(api_key='6452f6e1b7bf430eb07477bbe23353c4')
    sources = newsapi.get_sources()

    if sources['status'] == 'ok':
        df_sources = pd.DataFrame(sources['sources'])
        df_sources = df_sources.drop(columns=['description', 'url'])
        df_sources.to_csv('data_sources_newsapi', index=False)
