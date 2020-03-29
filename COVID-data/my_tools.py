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


def read_csv(name, title):
    df = pd.read_csv('data/' + name + '.csv')
    df['Date'] = df['Date'].astype('datetime64[ns]') 
    df = df.set_index('Date')
    df.name = title
    
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
    
def plot_side_by_side(df1, df2, countries=[], leg=True, scale='linear', title='', days=0):
    if days == 0:
        days = len(df1)
    
    fig, (ax1, ax2) = plt.subplots(ncols=2)
    if title:
        fig.suptitle(title)
    
    if leg:
        if not countries:
            df1.tail(days).plot(figsize=(17,6), ax=ax1)
            df2.tail(days).plot(figsize=(17,6), ax=ax2)
        else:
            df1[countries].tail(days).plot(figsize=(17,6), ax=ax1)
            df2[countries].tail(days).plot(figsize=(17,6), ax=ax2)
        
        ax1.legend(frameon=False, loc='upper left')
        ax2.legend(frameon=False, loc='upper left')
     
    else:
        if not countries:
            df1.tail(days).plot(figsize=(17,6), ax=ax1, legend=False)
            df2.tail(days).plot(figsize=(17,6), ax=ax2, legend=False)
        else:
            df1.tail(days)[countries].plot(figsize=(17,6), ax=ax1, legend=False)
            df2.tail(days)[countries].plot(figsize=(17,6), ax=ax2, legend=False)
    
    ax1.set_xlabel('')
    ax1.set_yscale(scale)
    ax1.set_title(df1.name)
  
    ax2.set_xlabel('')
    ax2.set_yscale(scale)
    ax2.set_title(df2.name)
    
    plt.show()
    
def show_everything(country_list, amount_days, header):
    plot_side_by_side(df_cases_new, df_deaths_new, title=header, countries=country_list, days=amount_days)

    plot_side_by_side(df_cases_total, df_deaths_total, title='Linear scale', countries=country_list, days=amount_days)
    plot_side_by_side(df_cases_total, df_deaths_total, title='Logaritmic scale', scale='log', countries=country_list, days=amount_days)

    plot_side_by_side(df_cases_relative, df_deaths_relative, title='Linear scale', countries=country_list, days=amount_days)
    plot_side_by_side(df_cases_relative, df_deaths_relative, title='Logaritmic scale', scale='log', countries=country_list, days=amount_days)
    
def show_table(countries):
    info_new = []
    info_total = []
    info_relative = []
    
    d = {}
    
    for country in countries:
        info_new.append([country, df_cases_new[country].values[-1], df_deaths_new[country].values[-1]])
        info_total.append([country, df_cases_total[country].values[-1], df_deaths_total[country].values[-1]])
        info_relative.append([country, df_cases_relative[country].values[-1], df_deaths_relative[country].values[-1]])
        
    d['New'] = pd.DataFrame(columns=['ind', 'Cases', 'Deaths'], data=info_new).set_index('ind')
    d['Total'] = pd.DataFrame(columns=['ind', 'Cases', 'Deaths'], data=info_total).set_index('ind')
    d['Relative'] = pd.DataFrame(columns=['ind', 'Cases', 'Deaths'], data=info_relative).set_index('ind')
    
    df = pd.concat(d, axis=1)
    return df