""" Implement other search criteria """
""" Implement shorter period possibility """
""" Use support db's to check criteria """
""" Check amount of articles get returned (capped at 20??)"""

import newsapi_data_search
import pandas as pd
import datetime

period = 1  # days


def first_collection(keyword):
    first_df = newsapi_data_search.get_all(keyword).set_index(['index'])

    first_df = first_df[~pd.isna(first_df['content'])]
    first_df = first_df.sort_values(by=['publishedAt'])

    first_df.to_csv('data_newsapi_' + keyword, index=False)


def periodic_collection(keyword):
    new_df = newsapi_data_search.full_search(keyword, period).set_index(['index'])

    if not new_df[0].count() == 0:
        try:
            stored_data = pd.read_msgpack('data_newsapi_' + keyword)

        except IOError:
            date = datetime.date.today().strftime("%Y-%m-%d")
            new_df.to_msgpack('data_newsapi_error_' + date + '_' + keyword)

            return

        stored_data = stored_data.merge(new_df)
        stored_data = stored_data.sort_values(by=['publishedAt'])

        stored_data.to_csv('data_newsapi_' + keyword, index=False)


def main():
    try:
        df_to_search = pd.read_csv('data_to_search')

    except IOError:
        print('count not load search crit.')
        return

    newsapi_ind = df_to_search.index[df_to_search['api'] == 'newsapi'].tolist()

    for i in newsapi_ind:
        if df_to_search.at[i, 'search_count'] == 0:
            first_collection(df_to_search.at[i, 'keyword'])
        else:
            periodic_collection(df_to_search.at[i, 'keyword'])

        df_to_search.at[i, 'search_count'] += 1
        df_to_search.to_csv('data_to_search')


if __name__ == '__main__':
    main()
