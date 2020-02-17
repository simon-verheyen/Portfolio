#
# Manages the automatic searches that need to happen.
# Every entry is a keyword with an allowed combination of criteria
#   Criteria in saved in string form for ease of reading
#
# Only called when adding or removing searches
#

from datetime import date
import pandas as pd


# Loads/Creates search df, checks if crit are allowed or present already, adds search and saves df
def add_search_term(keyword='', sources='', countries='', categories='', api='newsapi', language='en'):
    keyword = keyword.lower()
    filename = 'data_searches_' + api

    if sources and (countries or categories):
        print("search on source and other criteria can't be done")
        return

    try:
        api_criteria = pd.read_csv('data_sources_' + api)
        if language:
            filename += '_' + language
            lang_crit = api_criteria.loc[api_criteria['language'] == language]

    except IOError:
        print("Couldn't find criteria")
        return

    bad_source = False
    bad_country = False
    bad_category = False

    if sources:
        for source in sources.split(","):
            if lang_crit[lang_crit['id'].isin([source])].empty:
                bad_source = True

    if countries:
        for country in sources.split(","):
            if lang_crit[lang_crit['country'].isin([country])].empty:
                bad_country = True

    if categories:
        for category in categories.split(","):
            if lang_crit[lang_crit['category'].isin([category])].empty:
                bad_category = True

    if bad_source or bad_country or bad_category:
        print("Bad criteria input")
        return

    try:
        df_to_search = pd.read_csv(filename)

    except IOError:
        print("Creating new search file: " + str(date.today()))

        structure = {'keyword': [keyword], 'source': [sources], 'country': [countries],
                     'category': [categories], 'api': [api], 'language': [language], 'search_count': [0], 'oldest_search': []}

        df_to_search = pd.DataFrame(structure)
        df_to_search.to_csv(filename, index=False)

        return

    present = False
    key_ind = df_to_search.index[df_to_search['keyword'] == keyword].tolist()

    if len(key_ind) > 0:
        for i in key_ind:
            same_source = False
            if not pd.isna(df_to_search.at[i, 'source']) and df_to_search.at[i, 'source'] == sources:
                same_source = True
            elif pd.isna(df_to_search.at[i, 'source']) and not sources:
                same_source = True

            same_country = False
            if not pd.isna(df_to_search.at[i, 'country']) and df_to_search.at[i, 'country'] == countries:
                same_country = True
            elif pd.isna(df_to_search.at[i, 'country']) and not countries:
                same_country = True

            if not pd.isna(df_to_search.at[i, 'category']) and df_to_search.at[i, 'category'] == categories:
                same_category = True
            elif pd.isna(df_to_search.at[i, 'category']) and not categories:
                same_category = True

            same_api = df_to_search.at[i, 'api'] == api
            same_lang = df_to_search.at[i, 'language'] == language

            if same_source and same_country and same_category and same_api and same_lang:
                present = True

    if not present:
        structure = {'keyword': keyword, 'source': sources, 'country': countries,
                     'category': categories, 'api': api, 'language': language, 'search_count': 0}

        df_to_search = df_to_search.append(structure, ignore_index=True, sort=False)

    df_to_search.to_csv(filename, index=False)


# Loads df if possible, checks if provided crit are in if, and removes if they are
def remove_search_term(keyword, sources='', countries='', categories='', api='newsapi', language='en'):
    keyword = keyword.lower()
    filename = 'data_searches_' + api

    if language:
        filename += '_' + language

    try:
        df_to_search = pd.read_csv(filename)

    except IOError:
        print("couldn't find the database")
        return

    keys_ind = df_to_search.index[df_to_search['keyword'] == keyword].tolist()

    if len(keys_ind) == 0:
        print("keyword not found")

    else:
        for i in keys_ind:
            correct_entry = True

            if not pd.isna(df_to_search.at[i, 'source']) and df_to_search.at[i, 'source'] != sources:
                correct_entry = False
            elif pd.isna(df_to_search.at[i, 'source']) and sources:
                correct_entry = False

            if not pd.isna(df_to_search.at[i, 'country']) and df_to_search.at[i, 'country'] != countries:
                correct_entry = False
            elif pd.isna(df_to_search.at[i, 'country']) and countries:
                correct_entry = False

            if not pd.isna(df_to_search.at[i, 'category']) and df_to_search.at[i, 'category'] != categories:
                correct_entry = False
            elif pd.isna(df_to_search.at[i, 'category']) and categories:
                correct_entry = False

            if correct_entry:
                df_to_search = df_to_search.drop(df_to_search.index[i])
                break

        df_to_search.to_csv(filename, index=False)
