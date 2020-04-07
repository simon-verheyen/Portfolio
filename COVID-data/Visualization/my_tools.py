import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
import pandas as pd
import datetime


def read_csv(name, title):
    df = pd.read_csv('../data/' + name + '.csv')
    df['Date'] = df['Date'].astype('datetime64[ns]') 
    df = df.drop(columns='Cases on an international conveyance Japan')
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

countries_all = df_cases_daily.columns
dates_daily = df_cases_daily.index
dates_3days = df_cases_3days.index
dates_weekly = df_cases_weekly.index

global_all = ['Global', 'Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America']

latest_date = dates_daily[-1]


def worst_in_crit(subj, date=latest_date, period=6):
    df = eval('df_' + subj)
    df = df.drop(columns=global_all)

    if subj == 'prevalence':
        df = df.iloc[-1:]
        worst = df.apply(pd.Series.nlargest, axis=1, n=10).columns
    else:
        start_date = date - datetime.timedelta(days=period)
        df = df.loc[start_date:date]
        df = df.sum(axis=0)
        df = df.nlargest(10)

        worst = df.index
    
    return worst

def find_crit(subj, period=6):
    if subj == 'recovered':
        start_date = latest_date - datetime.timedelta(days=period)
        recovered = []
    
        for country in countries_all:
            if df_cases_total.at[start_date,country] == df_cases_total.at[latest_date,country]:
                recovered.append(country)
                
        return recovered
    
    else:                
        if subj == 'active':
            crit1 = 'cases_daily'
            crit2 = 'deaths_daily'
        elif subj == 'impacted':
            crit1 = 'incidence_daily'
            crit2 = 'prevalence'

        list1 = worst_in_crit(crit1, period=period)
        list2 = worst_in_crit(crit2, period=period)

        return list1.intersection(list2).tolist()
    
def plot_spread(subj, per, countries=countries_all, scale='lin', days=len(dates_daily)):
    fig, (ax1, ax2) = plt.subplots(ncols=2)
    label1 = ''
    label2 = ''
    leg_loc = 'upper left'
    
    if subj == 'incidence':
        df2 = df_prevalence
        title2 = 'Prevalence (total cases / population)'
    elif subj == 'cases':
        df2 = df2 = eval('df_deaths_' + per)
        title2 = per.capitalize() + ' deaths'
        
    df1 = eval('df_' + subj + '_' + per)
    title1 = per.capitalize() + subj.capitalize()
            
    if scale == 'log':
        title1 = title1 + ' (log scale, normalizing translation)'
        title2 = title2 + ' (log scale, normalizing translation)'
        
        label1 = 'Days since 100 cases'
        label2 = 'Days since 10 deaths'
        
        if subj == 'cases':
            if per == 'total':
                leg_loc = 'lower right'
            else:
                leg_loc = 'upper right'
        else: 
            leg_loc = 'upper right'
        
        ax1.set_yscale('log')
        ax2.set_yscale('log')
        
        if per == 'total':
            per = 'daily'
        
        df1 = threshold_data(df1, 'cases', per, countries)
        df2 = threshold_data(df2, 'deaths', per, countries)
        
    if len(countries) == len(countries_all):
        df1.tail(days).plot(figsize=(17, 6), ax=ax1, legend=False)
        df2.tail(days).plot(figsize=(17, 6), ax=ax2, legend=False) 
    else: 
        df1[countries].tail(days).plot(figsize=(17, 6), ax=ax1)
        df2[countries].tail(days).plot(figsize=(17, 6), ax=ax2, legend=False)
        ax1.legend(frameon=False, loc=leg_loc)
        
            
    ax1.set_title(title1)
    ax1.set_xlabel(label1)
    ax2.set_title(title2)
    ax2.set_xlabel(label2)

    plt.show()
    
def threshold_data(df, subj, per, countries=[], reset=True):
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

def plot_trends(countries=countries_all, log=True, subj='spread', per='weekly'):
    plt.figure(figsize=(17,9))
    leg = True
    
    if subj == 'impact':
        x = 'prevalence'
        y = 'incidence_' + per
        
        plt.xlabel('Prevalence (total cases / population)')
        plt.ylabel('Incidence (' + per + ' cases / population)') 
    elif subj == 'spread':
        x = 'cases_total'
        y = 'cases_' + per
        
        plt.xlabel('Total cases')
        plt.ylabel(per + ' cases')
    
    df_x_full = eval('df_' + x)
    df_y_full = eval('df_' + y)
    
    df_x_full = threshold_data(df_x_full, 'cases', per, countries, reset=True)
    df_y_full = threshold_data(df_y_full, 'cases', per, countries, reset=True)

    for country in countries:
        plt.plot(df_x_full[country], df_y_full[country], label=country)
        
    if len(countries) != len(countries_all):
        plt.legend(loc='upper left', frameon=False)
    
    if log:
        plt.xscale('log')
        plt.yscale('log')
        
    plt.title('Trends')
    plt.show()
    
def plot_trends_dynamically(name, countries=[]):
    fig, ax = plt.subplots(figsize=(13,9))
    leg = ax.legend()
    
    df_x_full = threshold_data(df_prevalence, 'cases', 'weekly', countries, reset=False)
    df_y_full = threshold_data(df_incidence_weekly, 'cases', 'weekly', countries, reset=False)
    
    def animate(i):
        ax.clear()
        
        ax.set_xscale('log')
        ax.set_yscale('log')

        ax.set_xlabel('Prevalence (total cases / population)')
        ax.set_ylabel('Incidence (weekly cases / population)')

        i += 1
        for country in countries:
            x = df_x_full.iloc[:i][country]
            y = df_y_full.iloc[:i][country]
            
            line, = ax.plot(x, y, '-o', markevery=[-1],label=country)
            plt.annotate(country, (x[-1],y[-1]), textcoords="offset points", xytext=(5,10), ha='right', color=line.get_color())
        
        if i > len(df_x_full) - 1:
            i = len(df_x_full) - 1
        
        ax.annotate(df_x_full.index[i].date(), xy=(0.85, 0.05), xycoords='axes fraction', fontsize=15)
        ax.legend(loc="upper left", frameon=False)
        ax.set_title('Trends (logarithmic scale)')
        
    anim = animation.FuncAnimation(fig, animate, frames=15)
    anim.save(name + '.gif', writer=animation.PillowWriter(fps=2))
    
def convert_to_percent(x):
    str_x = '%.3f' % (x * 100) + '%'
    
    return str_x
    
def show_table(countries=countries_all):
    if 'Global' not in countries:
        countries = ['Global'] + countries
    
    dict_data = {}
    ind = [[],[]]
    daily = []
    days = []
    weekly = []
    total = []
    prevalence = []
    incidence_daily = []
    incidence_3days = []
    incidence_weekly = []
    mortality = []
    
    
    for country in countries:
        ind[0].append(country)
        ind[0].append(country)
        
        ind[1].append('Cases')
        ind[1].append('Deaths')
        
        daily.append(df_cases_daily[country].values[-1])
        daily.append(df_deaths_daily[country].values[-1])
        
        days.append(df_cases_3days[country].values[-1])
        days.append(df_deaths_3days[country].values[-1])
        
        weekly.append(df_cases_weekly[country].values[-1])
        weekly.append(df_deaths_weekly[country].values[-1])
        
        total.append(df_cases_total[country].values[-1])
        total.append(df_deaths_total[country].values[-1])
        
        prevalence.append(convert_to_percent(df_prevalence[country].values[-1]))
        prevalence.append('')
            
        incidence_daily.append(convert_to_percent(df_incidence_daily[country].values[-1]))
        incidence_daily.append('')
        
        incidence_3days.append(convert_to_percent(df_incidence_3days[country].values[-1]))
        incidence_3days.append('')
                      
        incidence_weekly.append(convert_to_percent(df_incidence_weekly[country].values[-1]))
        incidence_weekly.append('')
                      
        mortality.append('')
        mortality.append(convert_to_percent(df_mortality[country].values[-1]))
    
    dict_data['Today'] = daily
    dict_data['3 day av'] = weekly
    dict_data['Weekly av'] = weekly
    
    dict_data['Incidence today'] = incidence_daily
    dict_data['Incidence 3day av'] = incidence_daily
    dict_data['Incidence weekly av'] = incidence_weekly
    
    dict_data['Total'] = total
    dict_data['Prevalence'] = prevalence

    dict_data['Mortality'] = mortality
    
    df = pd.DataFrame(dict_data, index=ind)
        
    return df.style