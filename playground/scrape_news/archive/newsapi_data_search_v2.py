#
# By calling full_search(keyword) function all data (headlines and normal articles) will be collected,
#   cleaned up and provided in data-frame ordered by publication time.
#
# For now only created to look for all information on a specific keyword
#
# Script that will talk to the API and place the data into data-frames
# With non-commercial key NewsAPI can only be searched 1 month in the past (2020-01-08)
# First request will be for month worth of data to start with as big a data-set as possible,
# Afterwards algorithm can be set by get_date_after_period (now set to 1 day) to rerun every defined period
#

from newsapi import NewsApiClient
import pandas as pd
import datetime

# NewsAPI splits between headlines and all other, decision process to be implemented
# Create connection to NewsAPI wit personal key
newsapi = NewsApiClient(api_key='6452f6e1b7bf430eb07477bbe23353c4')


# Communicates with NewsAPI to gather top headlines info on keyword
def get_headlines(keyword):
    # (q=, source=, country=, category=)
    top_headlines = newsapi.get_top_headlines(q=keyword,
                                              language='en')

    df_top = create_database(top_headlines, 'top')

    return df_top


# Communicates with NewsAPI to gather all articles info on keyword
def get_all(keyword, period):
    if period == 0:
        from_parameter = get_date_prev_month()

    else:
        from_parameter = get_date_after_period(period)

    # (q=, source=, domain=, from_param=, language=, to=, page=, sort_by=)
    all_articles = newsapi.get_everything(q=keyword,
                                          from_param=from_parameter,
                                          language='en',
                                          pagesize=100)

    total_count = all_articles['totalResults']
    df_all = create_database(all_articles, 'all')
    total_count -= 100
    page = 2

    while total_count > 0:
        all_articles = newsapi.get_everything(q=keyword,
                                              from_param=from_parameter,
                                              language='en',
                                              pagesize=100,
                                              page=page)

        df_page = create_database(all_articles, 'all')
        df_all = df_all.merge(df_page, how='outer')
        total_count -= 100
        page += 1

    df_all = df_all.sort_values(by=['publishedAt'])

    return df_all


# Function used after collecting NewsAPI data to mold data into standardized data-frame
#   Doing so creates a unique key for every entry, created for publication time, source and author name
#   Will be refined in the future
def create_database(articles, article_type):
    if articles['status'] == 'ok':
        df_articles = pd.DataFrame(articles['articles'])

        df_articles = df_articles.drop(columns=['urlToImage'])
        df_articles = df_articles[~pd.isna(df_articles['content'])]

        df_articles['unique_key'] = ''
        df_articles['article_type'] = article_type

        for i in range(df_articles.shape[0]):
            df_articles.at[i, 'source'] = df_articles.at[i, 'source']['name']

            author = df_articles.at[i, 'author']
            source = df_articles.at[i, 'source']
            key = df_articles.at[i, 'publishedAt']

            author_key = ''
            source_key = ''
            title_key = df_articles.at[i, 'title'][0]
            type_key = df_articles.at[i, 'article_type'][0]

            if author:
                author_split = author.split()
                for name in author_split:
                    if not name[0] == '(':
                        author_key += name[0]

            if source:
                source_split = source.split()
                for name in source_split:
                    source_key += name[0]

            key += '-' + author_key + '-' + title_key + '-' + source_key + type_key

            df_articles.at[i, 'unique_key'] = key

        return df_articles


# Finds date 1 month before call, since this is max history we can access in NewsAPI
# Used in first data gathering to collect as much as possible
def get_date_prev_week():
    date_prev_week = datetime.date.today() - datetime.timedelta(days=7)

    from_parameter = date_prev_week.strftime("%Y-%m-%d")

    return from_parameter


# Finds date X-days before call
# Will be used for automatic periodic data collection
def get_date_after_period(delta_time):
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=delta_time)

    from_parameter = yesterday.strftime("%Y-%m-%d")

    return from_parameter
