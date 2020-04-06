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


df_cases_daily = read_csv('cases_daily', 'Daily cases')
df_cases_3days = read_csv('cases_3days', '3 days average cases')
df_cases_weekly = read_csv('cases_weekly', 'Weekly cases weekly')
df_cases_total = read_csv('cases_total','Total cases')

df_deaths_daily = read_csv('deaths_daily', 'Daily deaths')
df_deaths_3days = read_csv('deaths_3days', '3 days average  deaths')
df_deaths_weekly = read_csv('deaths_weekly', 'Weekly deaths')
df_deaths_total = read_csv('deaths_total', 'Total deaths')


df_incidence_daily = read_csv('incidence_daily', 'Daily incidence')
df_incidence_3days = read_csv('incidence_3days', '3days incidence')
df_incidence_weekly = read_csv('incidence_weekly', 'Weekly incidence')

df_thresholds = pd.read_csv('../data/thresholds.csv').set_index('ind')
                              
df_prevalence = read_csv('prevalence', 'Prevalence')
df_mortality = read_csv('mortality', 'Mortality')

df_global = read_csv('global', 'Global data')

df_africa = read_csv('africa', 'African data')
df_asia = read_csv('asia', 'Asian data')
df_europe = read_csv('europe', 'European data')
df_north_america = read_csv('north_america', 'North_american data')
df_oceania = read_csv('oceania', 'Oceania data')
df_south_america = read_csv('south_america', 'South American data')

countries_all = df_cases_daily.columns
dates_daily = df_cases_daily.index
dates_3days = df_cases_3days.index
dates_weekly = df_cases_weekly.index

latest_date = dates_daily[-1]


def worst_in_cat(date, subj, period=6):
    if type(date) == str:
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
    
    start_date = date - datetime.timedelta(days=period)

    df = eval('df_' + subj)
        
    df = df.loc[start_date:end_date]
    df = df.sum(axis=0)
    df = df.nlargest(10)
    worst = df.index
    
    return worst

def find_recovered(period=7):
    start_date = latest_date - datetime.timedelta(days=period)
    recovered = []
    
    for country in countries:
        if country != 'Cases on an international conveyance Japan':
            if df_cases_total.at[start_date,country] == df_cases_total.at[latest_date,country]:
                recovered.append(country)
    
    return recovered

def plot_global():
    plot_side_by_side(df_global['incidence_daily'], df_global['prevalence'], leg=False, title='Global info')
    plot_side_by_side(df_global['deaths_total'], df_global['mortality'], leg=False)
    
    
def plot_spread(subject, countries=[], scale='lin', days=0):
    sizes = (17, 6)
    
    if days == 0:
        days = len(df_cases_daily)
    
    fig, (ax1, ax2) = plt.subplots(ncols=2)
    label1 = ''
    label2 = ''
    
    if subject == 'incidence_daily':
        df1 = df_incidence_daily
        df2 = df_prevalence
        
        title1 = 'Incidence (daily cases / population)'
        title2 = 'Prevalence (total cases / population)'
        
        per = 'daily'
    elif subject == 'incidence_weekly':
        df1 = df_incidence_weekly
        df2 = df_prevalence
        
        title1 = 'Incidence (weekly cases / population)'
        title2 = 'Prevalence (total cases / population)'
        
        per = 'weekly'
    elif subject == 'incidence_3days':
        df1 = df_incidence_3days
        df2 = df_prevalence
        
        title1 = 'Incidence (3day av. cases / population)'
        title2 = 'Prevalence (total cases / population)'
        
        per = '3days'
    else:
        df1 = eval('df_cases_' + subject)
        df2 = eval('df_deaths_' + subject)
        
        title1 = subject.capitalize() + ' cases'
        title2 = subject.capitalize() + ' deaths'
        
        per = subject
        if subject == 'total':
            per = 'daily'
    
    if scale == 'lin':
        if countries:
            df1[countries].tail(days).plot(figsize=sizes, ax=ax1)
            df2[countries].tail(days).plot(figsize=sizes, ax=ax2, legend=False)
            ax1.legend(frameon=False, loc='upper left')
        else: 
            df1.tail(days).plot(figsize=sizes, ax=ax1, legend=False)
            df2.tail(days).plot(figsize=sizes, ax=ax2, legend=False)   
            
    elif scale == 'log':
        title1 = title1 + ' (log scale + normalizing translation)'
        title2 = title2 + ' (log scale + normalizing translation)'
        
        label1 = 'Days since 100 cases'
        label2 = 'Days since 10 deaths'
        
        if subject in ['daily', 'total', 'incidence_daily']:
            per = 'daily'
        elif subject in ['3days', 'incidence_3days']:
            per = '3days'
        else:
            per = 'weekly'
        
        df1 = threshold_data(df1, 'cases', per)
        df2 = threshold_data(df2, 'deaths', per)
        
        
        if countries:
            df1[countries].dropna(axis=0, how='all').plot(figsize=sizes, ax=ax1, legend=False)
            df2[countries].dropna(axis=0, how='all').plot(figsize=sizes, ax=ax2)
            ax2.legend(frameon=False, loc='lower right')
        else: 
            df1.tail(days).plot(figsize=sizes, ax=ax1, legend=False)
            df2.tail(days).plot(figsize=sizes, ax=ax2, legend=False)
        
        ax1.set_yscale('log')
        ax2.set_yscale('log')
            
    ax1.set_title(title1)
    ax1.set_xlabel(label1)
    #ax1.set_ylim(ymin=100)
    ax2.set_title(title2)
    ax2.set_xlabel(label2)
    #ax2.set_ylim(ymin=10)

    plt.show()
    
def threshold_data(df, subj, per, countries=countries_all, reset=True):
    d = {}

    for country in countries:
        start_date = df_thresholds.at[subj, country]

        allowed_dates = df.index[df.index >= start_date]
        allowed_dates = allowed_dates[[date in eval('dates_' + per) for date in allowed_dates]]
        mask = [date in allowed_dates for date in df.index]
        
        country_data = df.loc[mask][country]
        if reset: 
            country_data = country_data.reset_index(drop=True)
            
        d[country] = country_data

    df_new = pd.DataFrame(d)

    return df_new
        
def plot_trends(countries=countries_all, log=True, glob=True, subject='spread', per='weekly'):
    plt.figure(figsize=(17,9))
    leg = True
    
    if subject == 'impact':
        x = 'prevalence'
        y = 'incidence_' + per
        
        plt.xlabel('Prevalence (total cases / population)')
        plt.ylabel('Incidence (' + per + ' cases / population)') 
    elif subject == 'spread':
        x = 'cases_total'
        y = 'cases_' + per
        
        plt.xlabel('Total cases')
        plt.ylabel(per + ' cases')
    
    df_x_full = eval('df_' + x)
    df_y_full = eval('df_' + y)
    
    df_x_full = threshold_data(df_x_full, 'cases', per, countries, reset=True)
    df_y_full = threshold_data(df_y_full, 'cases', per, countries, reset=True)
    
    if glob:
        df_global_trends = df_global.loc[df_global['cases_total'] > 100, [x, y]]
        df_global_trends = df_global_trends.loc[eval('dates_' + per)]
        
        plt.plot(df_global_trends[x], df_global_trends[y], label='Global')

    for country in countries:
        plt.plot(df_x_full[country], df_y_full[country], label=country)
        
    if len(countries) != len(countries_all):
        plt.legend(loc='upper left', frameon=False)
    
    if log:
        plt.xscale('log')
        plt.yscale('log')
        
    plt.title('Trends')
    plt.show()
    
def convert_to_percent(x):
    str_x = '%.3f' % (x * 100) + '%'
    
    return str_x
    
def show_table(countries=[]):
    if countries == []:
        countries = df_cases_daily.columns
    
    dict_data = {}
    
    ind = [['Global', 'Global'],['Cases', 'Deaths']]
    daily = [df_global['cases_daily'].values[-1], df_global['deaths_daily'].values[-1]]
    weekly = [df_global['cases_weekly'].values[-1], df_global['deaths_weekly'].values[-1]]
    total = [df_global['cases_total'].values[-1], df_global['deaths_total'].values[-1]]
    
    prevalence = [convert_to_percent(df_global['prevalence'].values[-1]), '']
    incidence_daily = [convert_to_percent(df_global['incidence_daily'].values[-1]), '']
    incidence_weekly = [convert_to_percent(df_global['incidence_weekly'].values[-1]), '' ]
    mortality = ['', convert_to_percent(df_global['mortality'].values[-1])]    
    
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