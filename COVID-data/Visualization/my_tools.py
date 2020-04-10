import matplotlib.pyplot as plt
from matplotlib import animation
import matplotlib.ticker as ticker
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

'../data/deaths_population.csv'
df_incidence_daily = read_csv('incidence_daily', 'Daily incidence')
df_incidence_3days = read_csv('incidence_3days', '3days incidence')
df_incidence_weekly = read_csv('incidence_weekly', 'Weekly incidence')

df_thresholds = pd.read_csv('../data/thresholds.csv').set_index('ind')
                              
df_prevalence = read_csv('prevalence', 'Prevalence')
df_deaths_population = read_csv('deaths_population', 'Deaths over population')
df_mortality = read_csv('mortality', 'Mortality')

countries_all = df_cases_daily.columns
dates_daily = df_cases_daily.index
dates_3days = df_cases_3days.index
dates_weekly = df_cases_weekly.index

global_all = ['Global', 'Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America']

latest_date = dates_daily[-1]
print('Latest update at ' + str(datetime.date.today()))
print('Latest data point at ' + str(latest_date.date()))

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
    
def plot_mortality(countries=[], days=len(dates_daily)):
    fig, (ax1, ax2) = plt.subplots(ncols=2)
    
    df1 = threshold_data(df_mortality * 100, 'deaths', 'daily', countries, reset=False)
    df2 = threshold_data(per_million(df_deaths_population), 'deaths', 'daily', countries, reset=False)
    df1[countries].tail(days).plot(figsize=(17, 6), ax=ax1)
    df2[countries].tail(days).plot(figsize=(17, 6), ax=ax2, legend=False)

    ax1.legend(loc='upper left', frameon=False)
    ax1.yaxis.set_major_formatter(ticker.PercentFormatter())
    
    ax1.set_title('Mortality')
    ax1.set_ylabel('Deaths / Cases')
    ax1.set_xlabel('')    
    
    ax2.set_title('Deaths in population')
    ax2.set_ylabel('Deaths per million')
    ax2.set_xlabel('')              
    
    
def plot_spread(subj, per, countries=countries_all, scale='lin', days=len(dates_daily), leg='l'):
    fig, (ax1, ax2) = plt.subplots(ncols=2)
    label1 = ''
    label2 = ''
    leg_loc = 'upper left'
    if leg == 'l':   
        leg1 = True
        leg2 = False
    else:
        leg1 = False
        leg2 = True
    
    if subj == 'incidence':
        df1 = per_million(eval('df_' + subj + '_' + per))
        df2 = per_million(df_prevalence)
        
        title1 = 'Incidence ' 
        title2 = 'Prevalence (total)'
        ax1.set_ylabel('New cases per million')
        ax2.set_ylabel('Cases per million')
        threshold_filter = 'cases'
        
    elif subj == 'cases':
        df1 = eval('df_' + subj + '_' + per)
        df2 = eval('df_deaths_' + per)
        title1 = 'New cases'
        title2 = 'New deaths'
        threshold_filter = 'deaths'
        if per == '3days':
            title2 = title2 + ' (3 day av.)'
        elif per == 'weekly':
            title2 = title2 + ' (weekly av.)' 
        elif per == 'daily': 
            title2 = title2 + ' (daily)'
        
    if per == '3days':
        title1 = title1 + ' (3 day av.)'
    elif per == 'weekly':
        title1 = title1 + ' (weekly av.)' 
    elif per == 'daily': 
        title1 = title1 + ' (daily)'
    else:
        title1 = 'Total cases'
        title2 = 'Total deaths'
            
    if scale == 'log':
        if subj == 'cases':
            if per == 'total':
                leg_loc = 'lower right'
            else:
                leg_loc = 'upper right'
        else: 
            leg_loc = 'lower right'
        
        ax1.set_yscale('log')
        ax2.set_yscale('log')
        
        label1 = 'Days since 100 cases'
        label2 = 'Days since 10 deaths'
        
        ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y,pos: ('{{:.{:1d}f}}'.format(int(np.maximum(-np.log10(y),0)))).format(y)))
        ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y,pos: ('{{:.{:1d}f}}'.format(int(np.maximum(-np.log10(y),0)))).format(y)))
        
        if per == 'total':
            per = 'daily'
        
        df1 = threshold_data(df1, 'cases', per, countries)
        df2 = threshold_data(df2, threshold_filter, per, countries)
        
    if len(countries) == len(countries_all):
        df1.tail(days).plot(figsize=(17, 6), ax=ax1, legend=False)
        df2.tail(days).plot(figsize=(17, 6), ax=ax2, legend=False) 
    else: 
        df1[countries].tail(days).plot(figsize=(17, 6), ax=ax1, legend=leg1)
        df2[countries].tail(days).plot(figsize=(17, 6), ax=ax2, legend=leg2)
        if leg1:
            ax1.legend(frameon=False, loc=leg_loc)
        else:
            ax2.legend(frameon=False, loc=leg_loc)    
        
    ax1.set_title(title1)
    ax2.set_title(title2)
    ax1.set_xlabel(label1)
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
    if reset:
        if per == '3days':
            df_new['index'] = df_new.reset_index()['index'] * 3
            df_new = df_new.set_index('index')
        elif per == 'weekly':
            df_new['index'] = df_new.reset_index()['index'] * 7
            df_new = df_new.set_index('index')

    return df_new
    
def plot_trends_dynamically(name, countries=[]):
    fig, ax = plt.subplots(figsize=(17,9))
    leg = ax.legend()
    
    df_x_full = threshold_data(per_million(df_prevalence), 'cases', 'weekly', countries, reset=False)
    df_y_full = threshold_data(per_million(df_incidence_weekly), 'cases', 'weekly', countries, reset=False)
    
    def animate(i):
        ax.clear()
        
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda y,pos: ('{{:.{:1d}f}}'.format(int(np.maximum(-np.log10(y),0)))).format(y)))
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y,pos: ('{{:.{:1d}f}}'.format(int(np.maximum(-np.log10(y),0)))).format(y)))
        ax.set_xlabel('Prevalence (Cases per Million)')
        ax.set_ylabel('Incidence (New cases per million)')

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
        ax.set_title('Trends (steps per week)')

    anim = animation.FuncAnimation(fig, animate, frames=20)
    anim.save('Dynamic-Trends/' + name + '.gif', writer=animation.PillowWriter(fps=2))

def per_million(x):
    if isinstance(x, pd.DataFrame):
        x_new = x * 1000000
        x_new.astype('int')
    elif isinstance(x, float):
        x_new = int(x * 1000000)
        
    return x_new
    
def percent(x):
    return f'{x * 100:.3f}%'
    
def show_table(countries=countries_all):
    if 'Global' not in countries:
        countries = ['Global'] + countries
    
    ind = [[],[]]
    dict_data = {'Total': [], 'Prevalence': [], 'Mortality': [], 'Today': [], '3 days av': [], 
                 'Weekly av': [], 'Incidence today': [], 'Incidence 3 days av': [], 'Incidence weekly av': []}
    
    for country in countries:
        ind[0] = ind[0] + [country, country]
        ind[1] = ind[1] + ['Cases', 'Deaths']
        
        dict_data['Total'] = dict_data['Total'] + [df_cases_total[country].values[-1], df_deaths_total[country].values[-1]]
        dict_data['Prevalence'] = dict_data['Prevalence'] + [percent(df_prevalence[country].values[-1]), '']
        dict_data['Mortality'] = dict_data['Mortality'] + ['', percent(df_mortality[country].values[-1])]
        
        add_today = [df_cases_daily[country].values[-1], df_deaths_daily[country].values[-1]]
        add_3days = [int(df_cases_3days[country].values[-1]), int(df_deaths_3days[country].values[-1])]
        add_weekly = [int(df_cases_weekly[country].values[-1]), int(df_deaths_weekly[country].values[-1])]
        
        dict_data['Today'] = dict_data['Today'] + add_today
        dict_data['3 days av'] = dict_data['3 days av'] + add_3days
        dict_data['Weekly av'] = dict_data['Weekly av'] + add_weekly
        
        add_today = [percent(df_incidence_daily[country].values[-1]), '']
        add_3days = [percent(df_incidence_3days[country].values[-1]), '']
        add_weekly = [percent(df_incidence_weekly[country].values[-1]), '']
        
        dict_data['Incidence today'] = dict_data['Incidence today'] + add_today
        dict_data['Incidence 3 days av'] = dict_data['Incidence 3 days av'] + add_3days          
        dict_data['Incidence weekly av'] = dict_data['Incidence weekly av'] + add_weekly
    
    df = pd.DataFrame(dict_data, index=ind)
        
    return df.style

"""
OLD FUNCTIONS:



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
        plt.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y,pos: ('{{:.{:1d}f}}'.format(int(np.maximum(-np.log10(y),0)))).format(y)))
        plt.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y,pos: ('{{:.{:1d}f}}'.format(int(np.maximum(-np.log10(y),0)))).format(y)))
        ax.set_xlabel('Prevalence (Cases per Million)')
        ax.set_ylabel('Incidence (New cases per million)')
        
    plt.title('Trends (log scale)')
    plt.show()
"""