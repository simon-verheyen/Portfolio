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
df_cases_weekly = read_csv('cases_weekly', 'New cases weekly')

df_deaths_new = read_csv('deaths_new', 'New deaths')
df_deaths_total = read_csv('deaths_total', 'Total deaths')
df_deaths_weekly = read_csv('deaths_weekly', 'New deaths weekly')

df_prevalence = read_csv('prevalence', 'Prevalence')
df_incidence = read_csv('incidence', 'Incidence')
df_mortality = read_csv('mortality', 'Mortality')

df_global = read_csv('global', 'Global data')

df_thresholds = pd.read_csv('data/thresholds.csv').set_index('ind')

today = datetime.date.today()

countries = df_cases_new.columns
dates = df_cases_new.index
weekly_dates = df_cases_weekly.index


def worst_in_cat(date, category):
    if type(date) == str:
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
    
    start_date = str(date - datetime.timedelta(days=7))
    end_date = str(date)
    
    if category == 'cases_new':
        df = df_cases_new
    elif category == 'cases_total':
        df = df_cases_total     
        
    elif category == 'deaths_new':
        df = df_deaths_new 
    elif category == 'deaths_total':
        df = df_deaths_total  
        
    elif category == 'prevalence':
        df = df_prevalence
    elif category == 'incidence':
        df = df_incidence
    elif category == 'mortality':
        df = df_mortality
        
    df = df.loc[start_date:end_date]
    df = df.sum(axis=0)
    df = df.nlargest(10)
    most = df.index
    
    return most

def find_active():
    worst_cases_new = worst_in_cat(today, 'cases_new')
    worst_deaths_new = worst_in_cat(today, 'deaths_new')

    most_active_today = worst_cases_new.intersection(worst_deaths_new)
    active_countries = most_active_today.tolist()
    active_countries.sort()
    
    return active_countries
    
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
    plot_side_by_side(df_global['cases_total'], df_global['prevalence'], leg=False, title='Global info')
    plot_side_by_side(df_global['deaths_total'], df_global['mortality'], leg=False)
    
    
def plot_both(subject, countries=[], days=0):
    sizes = (17, 6)
    
    if days == 0:
        days = len(df_cases_new)
    
    fig, (ax1, ax2) = plt.subplots(ncols=2)
    label1 = ''
    label2 = ''
    
    if subject == 'new':
        title1 = 'New cases'
        title2 = 'New deaths'
        
        if countries:
            df_cases_new[countries].tail(days).plot(figsize=sizes, ax=ax1)
            df_deaths_new[countries].tail(days).plot(figsize=sizes, ax=ax2, legend=False)
            ax1.legend(frameon=False, loc='upper left')
        else: 
            df_cases_new.tail(days).plot(figsize=sizes, ax=ax1, legend=False)
            df_deaths_new.tail(days).plot(figsize=sizes, ax=ax2, legend=False)
            
    elif subject == 'weekly':
        title1 = 'Weekly new cases'
        title2 = 'Weekly new deaths'
        
        if countries:
            df_cases_weekly[countries].tail(days).plot(figsize=sizes, ax=ax1)
            df_deaths_weekly[countries].tail(days).plot(figsize=sizes, ax=ax2, legend=False)
            ax1.legend(frameon=False, loc='upper left')
        else: 
            df_cases_weekly.tail(days).plot(figsize=sizes, ax=ax1, legend=False)
            df_deaths_weekly.tail(days).plot(figsize=sizes, ax=ax2, legend=False)
            
    elif subject == 'total':
        title1 = 'Total Cases'
        title2 = 'Total deaths'
        
        if countries:
            df_cases_total[countries].tail(days).plot(figsize=sizes, ax=ax1)
            df_deaths_total[countries].tail(days).plot(figsize=sizes, ax=ax2, legend=False)
            ax1.legend(frameon=False, loc='upper left')
        else: 
            df_cases_total.tail(days).plot(figsize=sizes, ax=ax1, legend=False)
            df_deaths_total.tail(days).plot(figsize=sizes, ax=ax2, legend=False)
            
    elif subject == 'total_log':
        title1 = 'Total cases (log scale + normalizing translation)'
        title2 = 'Total deaths (log scale + normalizing translation)'
        
        label1 = 'Days since 100 cases'
        label2 = 'Days since 10 deaths'
        
        df_cases_threshold = threshold_data(df_cases_total, 'cases', 'daily')
        df_deaths_threshold = threshold_data(df_deaths_total, 'deaths', 'daily')
        
        if countries:
            df_cases_threshold[countries].dropna(axis=0, how='all').plot(figsize=sizes, ax=ax1, legend=False)
            df_deaths_threshold[countries].dropna(axis=0, how='all').plot(figsize=sizes, ax=ax2)
            ax2.legend(frameon=False, loc='lower right')
        else: 
            df_cases_threshold.tail(days).plot(figsize=sizes, ax=ax1, legend=False)
            df_deaths_threshold.tail(days).plot(figsize=sizes, ax=ax2, legend=False)
        
        ax1.set_yscale('log')
        ax2.set_yscale('log')

    ax1.set_title(title1)
    ax1.set_xlabel(label1)
    ax2.set_title(title2)
    ax2.set_xlabel(label2)

    plt.show()
    
def plot_total(subject ,countries=[], days=0):
    sizes = (17, 4)
    
    if subject == 'cases':
        name = 'Cases'
        df1 = df_cases_total
        df2 = threshold_data(df_cases_total, 'cases', 'daily')
    
    if subject == 'deaths':
        name = 'Deaths'
        df1 = df_deaths_total
        df2 = threshold_data(df_deaths_total, 'deaths', 'daily')
    
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

def threshold_data(df, subject, period, countries=countries):
    d = {}

    for country in countries:
        if subject == 'cases':
            start_date = df_thresholds.at['cases', country]
        elif subject == 'deaths':
            start_date = df_thresholds.at['deaths', country]

        if period == 'daily':
            mask = df.index >= start_date
        elif period == 'weekly':
            allowed_dates = df.index[df.index >= start_date]
            allowed_weekly = allowed_dates[[date in weekly_dates for date in allowed_dates]]
            mask = [date in allowed_weekly for date in df.index]

        if not any(mask):
            mask = [False for i in range(len(df.index))]
            
        country_data = df.loc[mask][country].reset_index(drop=True)
        d[country] = country_data

    df_new = pd.DataFrame(d)

    return df_new
        
        
def plot_trends(countries=[]):
    plt.figure(figsize=(17,6))
    leg = True
    
    df_x = threshold_data(df_cases_total, 'cases', 'weekly')
    df_y = threshold_data(df_cases_weekly, 'cases', 'weekly')
    
    if countries == []:
        countries = df_cases_total.columns
        leg = False
    
    for country in countries:
        if leg:
            plt.plot(df_x[country], df_y[country], label=country)
        else:
            plt.plot(df_x[country], df_y[country])
         
    if leg:
        plt.legend(loc='upper left', frameon=False)
        
    plt.xlabel('Total cases')
    plt.xscale('log')
    plt.xlim(xmin=100)
    
    plt.ylabel('weekly new cases') 
    plt.yscale('log')
        
    plt.title('Trends (logarithmic scale)')
    plt.show()
    
def show_table(countries=[]):
    if countries == []:
        countries = df_cases_new.columns
    
    ind = [[],[]]
    dict_data = {}
    
    daily = []
    weekly = []
    total = []
    
    prevalence = []
    incidence = []
    mortality = []
    
    for country in countries:
        ind[0].append(country)
        ind[0].append(country)
        
        ind[1].append('Cases')
        ind[1].append('Deaths')
        
        daily.append(df_cases_new[country].values[-1])
        daily.append(df_deaths_new[country].values[-1])
        
        weekly.append(df_cases_weekly[country].values[-1])
        weekly.append(df_deaths_weekly[country].values[-1])
        
        total.append(df_cases_total[country].values[-1])
        total.append(df_deaths_total[country].values[-1])
        
        prevalence.append(f'{df_prevalence[country].values[-1] * 100 : 9.2f}%')
        prevalence.append('')
        
        incidence.append(f'{df_incidence[country].values[-1] * 100 : 9.3f}%')
        incidence.append('')
        
        mortality.append('')
        mortality.append(f'{df_mortality[country].values[-1] * 100 : 9.2f}%')
    
    dict_data['New daily'] = daily
    dict_data['New weekly'] = weekly
    dict_data['Total'] = total
    
    dict_data['Prevalence'] = prevalence
    dict_data['Incidence'] = incidence
    dict_data['Mortality'] = mortality
    
    df = pd.DataFrame(dict_data, index=ind)
        
    return df.style