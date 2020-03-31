import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime


def read_csv(name, title):
    df = pd.read_csv('data/' + name + '.csv')
    df['Date'] = df['Date'].astype('datetime64[ns]') 
    df = df.set_index('Date')
    df.name = title
    
    return df


df_cases_new = read_csv('cases_new', 'New cases')
df_cases_total = read_csv('cases_total','Total cases')
df_cases_relative = read_csv('cases_relative', 'Cases over population size')
df_cases_weekly = read_csv('cases_weekly', 'New cases weekly')

df_cases_threshold = pd.read_csv('data/cases_threshold.csv').reset_index(drop=True)
df_cases_threshold.name = 'Total cases after threshold'

df_deaths_new = read_csv('deaths_new', 'New deaths')
df_deaths_total = read_csv('deaths_total', 'Total deaths')
df_deaths_relative = read_csv('deaths_relative', 'Deaths over cases')
df_deaths_weekly = read_csv('deaths_weekly', 'New deaths weekly')

df_deaths_threshold = pd.read_csv('data/deaths_threshold.csv').reset_index(drop=True)
df_deaths_threshold.name = 'Total deaths after threshold'

df_global_data = read_csv('global_data', 'Global data')


def worst_in_cat(date, category):
    if type(date) == str:
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
    
    start_date = str(date - datetime.timedelta(days=7))
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

def plot_global():
    plot_side_by_side(df_global_data['cases_total'], df_global_data['cases_relative'], leg=False, title='Global info')
    plot_side_by_side(df_global_data['deaths_total'], df_global_data['deaths_relative'], leg=False)
    
    
def plot_new(countries=[], days=0):
    sizes = (17, 4)
    
    if days == 0:
        days = len(df_cases_new)
    
    fig, (ax1, ax2) = plt.subplots(ncols=2)
    
    if countries:
        df_cases_new[countries].tail(days).plot(figsize=sizes, ax=ax1)
        df_deaths_new[countries].tail(days).plot(figsize=sizes, ax=ax2, legend=False)
        ax1.legend(frameon=False, loc='upper left')
    else: 
        df_cases_new.tail(days).plot(figsize=sizes, ax=ax1, legend=False)
        df_deaths_new.tail(days).plot(figsize=sizes, ax=ax2, legend=False)

    ax1.set_title('Cases')
    ax1.set_xlabel('')
    ax2.set_title('Deaths')
    ax2.set_xlabel('')

    plt.show()
    
def plot_total(subject ,countries=[], days=0):
    sizes = (17, 4)
    
    if subject == 'cases':
        name = 'Cases'
        df1 = df_cases_total
        df2 = df_cases_threshold
    
    if subject == 'deaths':
        name = 'Deaths'
        df1 = df_deaths_total
        df2 = df_deaths_threshold
    
    if days == 0:
        days = len(df_cases_new)
    
    fig, (ax1, ax2) = plt.subplots(ncols=2)
    
    if countries != []:
        df1[countries].tail(days).plot(figsize=sizes, ax=ax1)
        df2[countries].dropna(axis=0, how='all').plot(figsize=sizes, ax=ax2, legend=False)
        
        ax1.legend(frameon=False, loc='upper left')
        ax2.set_xlabel('Days since 100 cases')
        
    else: 
        df1.tail(days).plot(figsize=sizes, ax=ax1, legend=False)
        df2.dropna(axis=0, how='all').plot(figsize=sizes, ax=ax2, legend=False)
        ax2.set_xlabel('Days since 10 deaths')
    
    ax1.set_title('linear')
    ax1.set_xlabel('')
    ax2.set_yscale('log')
    ax2.set_title('logarithmic + normalizing translation')

    plt.show()
        
def plot_trends(countries=[]):
    plt.figure(figsize=(17,6))
    leg = True
    
    if countries == []:
        countries = df_cases_total.columns
        leg = False
    
    for country in countries:
        x = df_cases_total.loc[df_cases_weekly.index, country].tolist()
        y = df_cases_weekly[country].tolist()
        
        if leg:
            plt.plot(x, y, label=country)
        else:
            plt.plot(x, y)

    plt.xlabel('total cases')
    plt.xscale('log')
    plt.xlim(xmin=100)
    
    plt.ylabel('weekly new cases') 
    plt.yscale('log')
    
    if leg:
        plt.legend(loc='upper left', frameon=False)
    plt.title('Trends')
    plt.show()
    
def show_table(countries=[]):
    if countries == []:
        countries = df_cases_new.columns
    
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

"""
def show_everything(country_list, amount_days):
    plot_new(country_list, days=amount_days)
    plot_3('cases', countries=country_list, days=amount_days)
    plot_3('deaths', countries=country_list, days=amount_days)
    plot_trends(country_list)
    show_table(country_list)
    
def plot_3(subject, countries=[], days=0, location='upper left'):
    sizes = (17, 4)
    if days == 0:
        days = len(df_cases_new)
    
    if subject == 'cases':
        name = 'TOTAL CASES'
        df1 = df_cases_total
        df2 = df_cases_threshold
    
    if subject == 'deaths':
        name = 'TOTAL DEATHS'
        df1 = df_deaths_total
        df2 = df_deaths_threshold
    
    fig, (ax1, ax2, ax3) = plt.subplots(ncols=3)
    fig.suptitle(name)
        
    if not countries:
        df1.tail(days).plot(figsize=sizes, ax=ax1, legend=False)
        df1.tail(days).plot(figsize=sizes, ax=ax2, legend=False)
        df2.plot(figsize=sizes, ax=ax3, legend=False)
    else:
        df1[countries].tail(days).plot(figsize=sizes, ax=ax1, legend=False)
        df1[countries].tail(days).plot(figsize=sizes, ax=ax2, legend=False)
        df2[countries].plot(figsize=sizes, ax=ax3, legend=False)
    
    ax3.legend(frameon=False, loc='lower right')
    
    ax1.set_xlabel('')
    ax1.set_title('linear')
  
    ax2.set_xlabel('')
    ax2.set_yscale('log')
    ax2.set_title('logarithmic')
    
    ax3.set_xlabel('')
    ax3.set_yscale('log')
    ax3.set_title('logarithmic, from threshold')
    
    plt.show()"""