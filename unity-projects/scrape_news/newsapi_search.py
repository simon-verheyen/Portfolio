#
# Collector that will get all data on a search from the last period (probably per hour)
#   combines all data in one df and returns it
#
# Trying to get over max results limit for out limited access account a bit
#   by resetting the time criteria when it should collect the 6th page
#
# Will be called by the main script
#

from newsapi import NewsApiClient
from datetime import datetime, timedelta
import pandas as pd

""" only collects 1000 of 3000 entries in a month search """
""" something wrong with reading sources """

newsapi = NewsApiClient(api_key='6452f6e1b7bf430eb07477bbe23353c4')


def get_all(sources, country, category):
    if pd.isna(sources):
        df_all = get_without_source(country, category)
    else:
        df_all = get_with_source(sources)

    return df_all


def get_with_source(sources):
    page = 1
    count = 1

    while count > 0:
        articles = newsapi.get_top_headlines(sources=sources, page=page)

        if articles['status'] == 'ok':
            if page == 1:
                df_all = create_database(articles)
            else:
                df_page = create_database(articles)
                df_all = df_all.append(df_page, sort=False)
            page += 1
            count = articles['totalResults'] - 20 * page

    return df_all


def get_without_source(country, category):
    page = 1
    count = 1

    while count > 0:
        articles = newsapi.get_everything(country=country, category=category, language='en', page=page)

        if articles['status'] == 'ok':
            if page == 1:
                df_all = create_database(articles)
            else:
                df_page = create_database(articles)
                df_all = df_all.append(df_page, sort=False)
            page += 1
            count = articles['totalResults'] - 20 * page

    return df_all


def create_database(articles):
    if articles['totalResults'] > 0:
        df_articles = pd.DataFrame(articles['articles'])

        for i in range(df_articles.shape[0]):
            df_articles.at[i, 'source'] = df_articles.at[i, 'source']['id']

        df_articles = df_articles.drop(columns=['url'])
        df_articles = df_articles.drop(columns=['urlToImage'])
        df_articles = df_articles[~pd.isna(df_articles['content'])]

        return df_articles
