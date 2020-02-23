from data_management import get_data, get_country_data, get_global_data
import tools_data as mt
import nn
import pandas as pd
import numpy as np

data = get_global_data(['child_mortality', 'population', 'children_per_mother', 'income_per_person', 'life_expectancy'])
data_norm = mt.normalize(data)

train_set = data_norm.loc[data_norm.index <= 1980]
test_set = data_norm.loc[data_norm.index > 1980]

train_X = train_set.loc[:, train_set.columns != 'life_expectancy']
train_Y = train_set.loc[:, train_set.columns == 'life_expectancy']

test_X = test_set.loc[:, test_set.columns != 'life_expectancy']
test_Y = test_set.loc[:, test_set.columns == 'life_expectancy']

nn.train_network([4, 3, 2, 1], train_X, train_Y, 20, 0.1, 0.001)

print(train_X.shape)
print(train_Y.shape)
print(test_X.shape)
print(test_Y.shape)