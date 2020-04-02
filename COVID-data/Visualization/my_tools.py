import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime


def read_csv(name, title):
    df = pd.read_csv('../data/' + name + '.csv')
    df['Date'] = df['Date'].astype('datetime64[ns]') 
    df = df.set_index('Date')
    df.name = title
    
    return df


df_cases_daily = read_csv('cases_daily', 'daily cases')
df_cases_total = read_csv('cases_total','Total cases')
df_cases_weekly = read_csv('cases_weekly', 'New cases weekly')

df_deaths_daily = read_csv('deaths_daily', 'daily deaths')
df_deaths_total = read_csv('deaths_total', 'Total deaths')
df_deaths_weekly = read_csv('deaths_weekly', 'New deaths weekly')

df_prevalence = read_csv('prevalence', 'Prevalence')
df_incidence_daily = read_csv('incidence_daily', 'Daily incidence')
df_incidence_weekly = read_csv('incidence_weekly', 'Weekly incidence')
df_mortality = read_csv('mortality', 'Mortality')

df_global = read_csv('global', 'Global data')

df_thresholds = pd.read_csv('../data/thresholds.csv').set_index('ind')

countries = df_cases_daily.columns
dates = df_cases_daily.index
weekly_dates = df_cases_weekly.index

latest_date = dates[-1]


def worst_in_cat(date, category):
    if type(date) == str:
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
    
    start_date = str(date - datetime.timedelta(days=7))
    end_date = str(date)
    
    if category == 'cases_daily':
        df = df_cases_daily
    elif category == 'cases_total':
        df = df_cases_total     
        
    elif category == 'deaths_daily':
        df = df_deaths_daily 
    elif category == 'deaths_total':
        df = df_deaths_total  
        
    elif category == 'prevalence':
        df = df_prevalence
    elif category == 'incidence_daily':
        df = df_incidence_daily
    elif category == 'incidence_weekly':
        df = df_incidence_weekly
        
    elif category == 'mortality':
        df = df_mortality
        
    df = df.loc[start_date:end_date]
    df = df.sum(axis=0)
    df = df.nlargest(10)
    most = df.index
    
    return most

def find_active():
    worst_cases = worst_in_cat(latest_date, 'cases_daily')
    worst_deaths = worst_in_cat(latest_date, 'deaths_daily')

    most_active = worst_cases.intersection(worst_deaths)
    active_countries = most_active.tolist()
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
    
    
def plot_spread(subject, countries=[], days=0):
    sizes = (17, 6)
    
    if days == 0:
        days = len(df_cases_daily)
    
    fig, (ax1, ax2) = plt.subplots(ncols=2)
    label1 = ''
    label2 = ''
    
    if subject == 'daily':
        title1 = 'Daily cases'
        title2 = 'Daily deaths'
        
        if countries:
            df_cases_daily[countries].tail(days).plot(figsize=sizes, ax=ax1)
            df_deaths_daily[countries].tail(days).plot(figsize=sizes, ax=ax2, legend=False)
            ax1.legend(frameon=False, loc='upper left')
        else: 
            df_cases_daily.tail(days).plot(figsize=sizes, ax=ax1, legend=False)
            df_deaths_daily.tail(days).plot(figsize=sizes, ax=ax2, legend=False)
            
    elif subject == 'weekly':
        title1 = 'Weekly cases'
        title2 = 'Weekly deaths'
        
        weeks = int(days / 7)
        
        if countries:
            df_cases_weekly[countries].tail(weeks).plot(figsize=sizes, ax=ax1)
            df_deaths_weekly[countries].tail(weeks).plot(figsize=sizes, ax=ax2, legend=False)
            ax1.legend(frameon=False, loc='upper left')
        else: 
            df_cases_weekly.tail(weeks).plot(figsize=sizes, ax=ax1, legend=False)
            df_deaths_weekly.tail(weeks).plot(figsize=sizes, ax=ax2, legend=False)
            
    elif subject == 'total':
        title1 = 'Total cases'
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
        ax1.set_ylim(ymin=100)
        ax2.set_yscale('log')
        ax2.set_ylim(ymin=10)
            
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
        days = len(df_cases_daily)
    
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
        
        
def plot_trends(countries=[], log=True):
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
    plt.xlim(xmin=100)
    
    plt.ylabel('weekly new cases') 
    
    if log:
        plt.xscale('log')
        plt.yscale('log')
        
    plt.title('Trends (logarithmic scale)')
    plt.show()
    
def convert_to_percent(x):
    str_x = f'{x * 100 : 9.3f}%'
    
    return str_x
    
def show_table(countries=[]):
    if countries == []:
        countries = df_cases_daily.columns
    
    ind = [[],[]]
    dict_data = {}
    
    daily = []
    weekly = []
    total = []
    
    prevalence = []
    incidence_daily = []
    incidence_weekly = []
    mortality = []
    
    ind[0].append('Global')
    ind[0].append('Global')

    ind[1].append('Cases')
    ind[1].append('Deaths')
    
    daily.append(df_global['cases_daily'].values[-1])
    daily.append(df_global['deaths_daily'].values[-1])

    weekly.append(df_cases_weekly.iloc[-1:].sum(axis=1).values[0])
    weekly.append(df_deaths_weekly.iloc[-1:].sum(axis=1).values[0])

    total.append(df_global['cases_total'].values[-1])
    total.append(df_global['deaths_total'].values[-1])

    prevalence.append(convert_to_percent(df_global['prevalence'].values[-1]))
    prevalence.append('')

    incidence_daily.append(convert_to_percent(df_global['incidence_daily'].values[-1]))
    incidence_daily.append('')

    incidence_weekly.append(convert_to_percent(df_incidence_weekly.iloc[-1:].sum(axis=1).values[0]))
    incidence_weekly.append('')

    mortality.append('')
    mortality.append(convert_to_percent(df_global['mortality'].values[-1]))
    
    
    for country in countries:
        ind[0].append(country)
        ind[0].append(country)
        
        ind[1].append('Cases')
        ind[1].append('Deaths')
        
        daily.append(df_cases_daily[country].values[-1])
        daily.append(df_deaths_daily[country].values[-1])
        
        weekly.append(df_cases_weekly[country].values[-1])
        weekly.append(df_deaths_weekly[country].values[-1])
        
        total.append(df_cases_total[country].values[-1])
        total.append(df_deaths_total[country].values[-1])
        
        prevalence.append(convert_to_percent(df_prevalence[country].values[-1]))
        prevalence.append('')
        
        incidence_daily.append(convert_to_percent(df_incidence_daily[country].values[-1]))
        incidence_daily.append('')
        
        incidence_weekly.append(convert_to_percent(df_incidence_weekly[country].values[-1]))
        incidence_weekly.append('')
        
        mortality.append('')
        mortality.append(convert_to_percent(df_mortality[country].values[-1]))
    
    dict_data['Today'] = daily
    dict_data['This week'] = weekly
    dict_data['Total'] = total
    
    dict_data['Prevalence'] = prevalence
    dict_data['Incidence today'] = incidence_daily
    dict_data['Incidence this week'] = incidence_weekly
    dict_data['Mortality'] = mortality
    
    df = pd.DataFrame(dict_data, index=ind)
        
    return df.style