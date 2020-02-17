#
# Manages the automatic searches that need to happen.
# Set up that per keyword it provides all the criteria that need to be searched on one by one
# Next upgrade will be that criteria are lists(?) so that:
#   more complex searches can be done
#   searching becomes more streamlined
#


""" Implement multiple entries functionality for sources/countries/categories/newsapi """
""" Implement verification of source, countries, category with support db's """
""" Check case sensitivity """

from datetime import date
import pandas as pd


def add_search_term(keyword, source='-', country='-', category='-', api='newsapi'):
    keyword = keyword.lower()

    try:
        df_to_search = pd.read_csv('data_to_search')

    except IOError:
        print("Created new file: " + str(date.today()))

        structure = {'keyword': [keyword], 'source': [source], 'country': [country],
                     'category': [category], 'api': [api], 'search_count': [0]}

        df_to_search = pd.DataFrame(structure)
        df_to_search.to_csv('data_to_search', index=False)

        return

    if keyword not in df_to_search['keyword'].values:
        structure = {'keyword': keyword, 'source': source, 'country': country,
                     'category': category, 'api': api, 'search_count': 0}

        df_to_search = df_to_search.append(structure, ignore_index=True)
        df_to_search.to_csv('data_to_search', index=False)

    else:
        key_ind = df_to_search.index[df_to_search['keyword'] == keyword].tolist()

        if len(key_ind) == 1:
            if source is not None:
                if df_to_search.at[key_ind[0], 'source'] == '-':
                    df_to_search.at[key_ind[0], 'source'] = source

                else:
                    sources_present = df_to_search.at[key_ind[0], 'source'].split()
                    if source not in sources_present:
                        df_to_search.at[key_ind[0], 'source'] = " ".join(sources_present)

            if country is not None:
                if df_to_search.at[key_ind[0], 'country'] == '-':
                    df_to_search.at[key_ind[0], 'country'] = country

                else:
                    countries_present = df_to_search.at[key_ind[0], 'country'].split()
                    if country not in countries_present:
                        countries_present.append(country)
                        df_to_search.at[key_ind[0], 'country'] = " ".join(countries_present)

            if category is not None:
                if df_to_search.at[key_ind[0], 'category'] == '-':
                    df_to_search.at[key_ind[0], 'category'] = category

                else:
                    categories_present = df_to_search.at[key_ind[0], 'category'].split()
                    if category not in categories_present:
                        df_to_search.at[key_ind[0], 'category'] = " ".join(categories_present)

            df_to_search.to_csv('data_to_search', index=False)

        else:
            print('Error: Keyword present more than once')
            clean_up()
            add_search_term(keyword, source, country, category, api)


def remove_search_term(keyword, source='', country='', category='', full=True):
    try:
        df_to_search = pd.read_csv('data_to_search')

    except IOError:
        print('couldnt find the database')
        return

    keys_ind = df_to_search.index[df_to_search['keyword'] == keyword].tolist()

    if len(keys_ind) == 0:
        print('keyword not found')

    elif len(keys_ind) == 1:

        if full:
            print(keys_ind[0])
            df_to_search = df_to_search.drop(keys_ind[0])

        else:
            if not country == '':
                countries_present = df_to_search.at[keys_ind, 'country'].split()
                if country in countries_present:
                    countries_present.remove(country)
                    df_to_search.at[keys_ind, 'country'] = " ".join(countries_present)

            if not source == '':
                sources_present = df_to_search['source'].split()
                if source not in sources_present:
                    sources_present.remove(source)
                    df_to_search.at[keys_ind, 'source'] = " ".join(sources_present)

            if not category == '':
                categories_present = df_to_search['category'].split()
                if category not in categories_present:
                    categories_present.remove(country)
                    df_to_search.at[keys_ind, 'country'] = " ".join(countries_present)

        df_to_search.reset_index(drop=True)
        df_to_search.to_csv('data_to_search', index=False)

    elif len(keys_ind) > 1:
        clean_up()
        remove_search_term(keyword, source, country, category, full)


# For now not used/needed, since df should never put in 2 entries but just in case
def clean_up():
    try:
        df_to_search = pd.read_csv('data_to_search')

    except IOError:
        print('couldnt find the database')
        return

    for i in range(df_to_search['keyword'].count()):
        keys_ind = df_to_search.index[df_to_search['keyword'] == df_to_search.at[i, 'keyword']].tolist()

        if not len(keys_ind) > 1:
            all_sources = []
            all_countries = []
            all_categories = []
            all_apis = []

            for j in keys_ind:
                for source in df_to_search.at[j, 'sources'].split():
                    if source not in all_sources:
                        all_sources.append(source)
                for country in df_to_search.at[j, 'country'].split():
                    if country not in all_countries:
                        all_countries.append(country)
                for category in df_to_search.at[j, 'category'].split():
                    if category not in all_categories:
                        all_categories.append(category)
                for api in df_to_search.at[j, 'api'].split():
                    if api not in all_apis:
                        all_apis.append(api)

            df_to_search.at[keys_ind[0], 'source'] = " ".join(all_sources)
            df_to_search.at[keys_ind[0], 'country'] = " ".join(all_countries)
            df_to_search.at[keys_ind[0], 'category'] = " ".join(all_categories)
            df_to_search.at[keys_ind[0], 'api'] = " ".join(all_apis)

            df_to_search.drop(index=keys_ind[1:])

    df_to_search.reset_index(drop=True)
    df_to_search.to_csv('data_to_search', index=False)
