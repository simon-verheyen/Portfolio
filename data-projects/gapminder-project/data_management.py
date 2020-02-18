import pandas as pd


def get_country_data(country, attr=[], from_param=1800, to=2018):
    attr = ['Year'] + attr
    structure = [(attr, []) for attr in attr]
    for x in range(from_param, to + 1):
        structure[0][1].append(x)

    for i in range(1, len(attr)):
        path = 'data/'
        filename = get_filename(attr[i])
        if filename == '':
            print("Bad attribute input: " + attr[i])
            return

        path += filename
        df = pd.read_csv(path, index_col='country')
        attr_values = df.loc[country, [str(x) for x in range(from_param, to + 1)]].tolist()

        for j in range(len(attr_values)):
            structure[i][1].append(attr_values[j])

    Dict = {title: columns for (title, columns) in structure}
    new_df = pd.DataFrame(Dict).set_index('Year')

    new_df.name = country

    return new_df


def get_global_data(attr=[], from_param=1800, to=2018):
    df_pop = pd.read_csv('data/population_total.csv', index_col='country')[[str(x) for x in range(from_param, to + 1)]]
    total_pop_per_year = df_pop.sum(axis=0, skipna=True).tolist()

    attr = ['Year'] + attr
    structure = [(attr, []) for attr in attr]

    for x in range(from_param, to + 1):
        structure[0][1].append(x)

    for i in range(1, len(attr)):
        path = 'data/'
        filename = get_filename(attr[i])

        if filename == '':
            print("Bad attribute input: " + attr[i])
            return

        path += filename
        df = pd.read_csv(path, index_col='country')[[str(x) for x in range(from_param, to + 1)]]

        df_rel = df * df_pop / total_pop_per_year
        av_values = df_rel.sum(axis=0, skipna=True).tolist()

        for val in av_values:
            structure[i][1].append(val)

    Dict = {title: columns for (title, columns) in structure}
    new_df = pd.DataFrame(Dict).set_index('Year')

    new_df.name = 'Global'

    return new_df


def get_filename(attr):
    if attr == 'child_mortality':
        filename = 'child_mortality_0_5_year_olds_dying_per_1000_born.csv'
    elif attr == 'av_child_per_mother':
        filename = 'children_per_woman_total_fertility.csv'
    elif attr == 'income_per_person':
        filename = 'income_per_person_gdppercapita_ppp_inflation_adjusted.csv'
    elif attr == 'av_life_expectancy':
        filename = 'life_expectancy_years.csv'
    elif attr == 'population':
        filename = 'population_total.csv'
    else:
        filename = ''

    return filename
