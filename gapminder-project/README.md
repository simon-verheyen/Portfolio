# Gapminder Project

This is a longterm project where I use data from gapminder.org, an open source data collection ngo, to create my own data management, visualization and machine learning applications.

- Archive:
Contains old jupyter notebooks used for tested that are not functional anymore since the script/folder architectur changed after creating these.

- Data:
Contains all the data sets used for this project.
---

- data-management.py:
Script used to load up needed data bases t create and return one dataframe or dictionary containing al the data that has been requested.
Search terms can be per country (or global average) and multiple variables like life expectancy or vaccination percentages.

- data-tools.py:
 Script used for visualizing and adjusting the datasets created by data-management.
 This is the script that needs the most work still.
 
 - nn.py:
 Script that combines all the functions in nn_tools to create and train a artificial neural network, as well as get predictions once it is trained.
 
 - nn_tools.py:
 Script contains all the needed functions and steps to setup a neural network as well as train it through gradient descent.
 With multiple optimization and regularization techniques, like L2 and weighted decay regularization, adam optimization and more.
