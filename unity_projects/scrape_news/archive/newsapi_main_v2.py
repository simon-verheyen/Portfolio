""" MERGE FUNCTION NOT CORRECT """
""" what happens when we go over the site call limit """

import newsapi_search
import pandas as pd
import datetime


def periodic_collection(keyword, source, ind):
    df_all = newsapi_search.get_all(keyword, source)
    file_name = 'data_newsapi_en_' + keyword + '_' + str(ind)

    try:
        stored_data = pd.read_csv(file_name)

    except IOError:
        df_all.to_csv(file_name, index=False)

        return

    stored_data = stored_data.append(df_all)
    stored_data.to_csv(file_name, index=False)


def main():
    try:
        df_to_search = pd.read_csv('data_searches_newsapi_en')

    except IOError:
        print("Couldn't load search criteria")
        return

    newsapi_ind = df_to_search.index[df_to_search['api'] == 'newsapi'].tolist()

    for i in newsapi_ind:
        if df_to_search.at[i, 'search_count'] == 0:
            df_to_search.at[i, 'oldest_search'] = datetime.datetime.today()

        periodic_collection(df_to_search.at[i, 'keyword'], df_to_search.at[i, 'source'], i)
        df_to_search.at[i, 'search_count'] += 1

    df_to_search.to_csv('data_searches_newsapi_en', index=False)


if __name__ == '__main__':
    main()
