#
# Main script that should be run on a timer
#   tries to open the searches df
#   per entry calls get_all() from newsapi_search.py
#   appends/creates a specific datafile per search
#

import newsapi_search
import pandas as pd
import datetime


def periodic_collection(source, country, category, ind):
    df_all = newsapi_search.get_all(source, country, category)
    file_name = 'data_newsapi_en_' + source + '_' + str(ind)

    if df_all is not None:
        try:
            stored_data = pd.read_csv(file_name)

        except IOError:
            print("Create new search dataset: " + str(datetime.date.today()))
            df_all.to_csv(file_name, index=False)

            return

        stored_data = stored_data.append(df_all, sort=False)
        stored_data.to_csv(file_name, index=False)

    else:
        print("Got back an empty result")


def main():
    try:
        df_to_search = pd.read_csv('data_searches_newsapi_en')

    except IOError:
        print("Couldn't load search criteria")
        return

    newsapi_ind = df_to_search.index[df_to_search['api'] == 'newsapi'].tolist()

    for i in newsapi_ind:
        periodic_collection(df_to_search.at[i, 'source'], df_to_search.at[i, 'country'], df_to_search.at[i, 'category'], i)
        df_to_search.at[i, 'search_count'] += 1

    df_to_search.to_csv('data_searches_newsapi_en', index=False)


if __name__ == '__main__':
    main()
