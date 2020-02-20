from data_management import get_data, get_country_data, get_global_data
import tools_data as mt
import nn
import numpy as np

input_data = get_global_data(['child_mortality', 'population', 'children_per_mother', 'income_per_person'])
output = get_global_data(['life_expectancy'])
data_norm = mt.normalize_df(input_data)

param = nn.train_network([4,3,2,1], data_norm, output, 100, 0.01, 'regression')



