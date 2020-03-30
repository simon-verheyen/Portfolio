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

df_thresholds = pd.read_csv('data/threshold_dates.csv').set_index('ind')
df_thresholds.name = 'Threshold dates'


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
    
def plot_side_by_side(df1, df2, countries=[], leg=True, scale='linear', title='', days=0, location='upper left'):
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
        
        ax1.legend(frameon=False, loc=location)
        ax2.legend(frameon=False, loc=location)
     
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
    
    df_cases_threshold = data_from_threshold(df_cases_total, country_list,'cases')
    df_deaths_threshold = data_from_threshold(df_deaths_total, country_list, 'deaths')
                                              
    plot_side_by_side(df_cases_threshold, df_deaths_threshold, title='Logaritmic scale + Normalized translation', scale='log', countries=country_list, location='lower right')
    
def show_table(countries):
    ind = [[],[]]
    struct_data = [('New', []), ('Total', []), ('Relative', [])]
    
    for country in countries:
        ind[0].append(country)
        ind[0].append(country)
        
        ind[1].append('Cases')
        ind[1].append('Deaths')
        
        struct_data[0][1].append(df_cases_new[country].values[-1])
        struct_data[0][1].append(df_deaths_new[country].values[-1])
        
        struct_data[1][1].append(df_cases_total[country].values[-1])
        struct_data[1][1].append(df_deaths_total[country].values[-1])
        
        cases_perc = f'{df_cases_relative[country].values[-1] * 100 : 9.2f}%'
        deaths_perc = f'{df_deaths_relative[country].values[-1] * 100 : 9.2f}%'
        
        struct_data[2][1].append(cases_perc)
        struct_data[2][1].append(deaths_perc)
    
    d = {title: content for (title, content) in struct_data}
    df = pd.DataFrame(d, index=ind)
        
    display(df.style)
    
def data_from_threshold(df, countries, category):
    d = {}
    
    if category == 'cases':
        start_dates = df_thresholds.iloc[0]
    else:
        start_dates = df_thresholds.iloc[1]
    
    for country in countries:
        if country in start_dates.index:
            date = start_dates[country]
            d[country] = df.loc[df.index >= date][country].reset_index(drop=True)
        
    df = pd.DataFrame(d)
    df.dropna(axis=0, how='all', subset=None, inplace=True)
    
    if category == 'cases':
        df.name = 'Total cases after first 100'
    else: 
        df.name = 'Total deaths after first 10'
    
    return df