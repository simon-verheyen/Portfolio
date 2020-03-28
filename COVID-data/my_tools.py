import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime


df_cases_new = pd.read_csv('data/cases_new.csv').set_index('Date')
df_cases_new.name= 'New cases'
df_cases_total = pd.read_csv('data/cases_total.csv').set_index('Date')
df_cases_total.name = 'Total cases'
df_cases_relative = pd.read_csv('data/cases_relative.csv').set_index('Date')
df_cases_relative.name = 'Cases over population size'

df_deaths_new = pd.read_csv('data/deaths_new.csv').set_index('Date')
df_deaths_new.name = 'New deaths'
df_deaths_total = pd.read_csv('data/deaths_total.csv').set_index('Date')
df_deaths_total.name = 'Total deaths'
df_deaths_relative = pd.read_csv('data/deaths_relative.csv').set_index('Date')
df_deaths_relative.name = 'Deaths over cases'


def read_csv(name):
    df = pd.read_csv('data/' + name + '.csv')
    df['Date'] = df['Date'].astype('datetime64[ns]') 
    df = df.set_index('Date')
    df.name = name
    
    return df

def worst_in_cat(date, category):
    if type(date) == str:
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
    
    start_date = str(date - datetime.timedelta(days=14))
    end_date = str(date)
    
    if category == 'cases_new':
        df = df_cases_new
    elif category == 'cases_total':
        df = df_cases_total     
    elif category == 'cases_relative':
        df = df_cases_relative
        
    elif category == 'deaths_new':
        df = df_deaths_new 
    elif category == 'deaths_total':
        df = df_deaths_total  
    elif category == 'deaths_relative':
        df = df_deaths_relative
        
    df = df.loc[start_date:end_date]
    df = df.sum(axis=0)
    df = df.nlargest(10)
    most = df.index
    
    return most


def plot_df(df, leg=False, size=(15,9), title='', scale='linear'):
    df.plot(figsize=size, legend=leg)
    
    if title != '':
        plt.title(title)
    else:
        plt.title(df.name)
            
    plt.yscale(scale)
    plt.show()
    
def plot_side_by_side(df1, df2, countries=[], leg=True, scale='linear', title=''):
    fig, (ax1, ax2) = plt.subplots(ncols=2)
    if title:
        fig.suptitle(title)
    
    if leg:
        if not countries:
            df1.plot(figsize=(17,6), ax=ax1)
            df2.plot(figsize=(17,6), ax=ax2)
        else:
            df1[countries].plot(figsize=(17,6), ax=ax1)
            df2[countries].plot(figsize=(17,6), ax=ax2)
        
        ax1.legend(frameon=False, loc='upper left')
        ax2.legend(frameon=False, loc='upper left')
     
    else:
        if not countries:
            df1.plot(figsize=(17,6), ax=ax1, legend=False)
            df2.plot(figsize=(17,6), ax=ax2, legend=False)
        else:
            df1[countries].plot(figsize=(17,6), ax=ax1, legend=False)
            df2[countries].plot(figsize=(17,6), ax=ax2, legend=False)
    
    ax1.set_xlabel('')
    ax1.set_yscale(scale)
    ax1.set_title(df1.name)
  
    ax2.set_xlabel('')
    ax2.set_yscale(scale)
    ax2.set_title(df2.name)
    
    plt.show()