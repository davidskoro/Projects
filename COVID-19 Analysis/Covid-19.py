# -*- coding: utf-8 -*-
"""
COVID-19 Analysis

"""

import pandas as pd
from datetime import datetime , timedelta

#%% Read in the data

county = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv')
state = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv')

#%% Clean the data

state['date'] = pd.to_datetime(state['date'])
county['date'] = pd.to_datetime(state['date'])

state.describe (include='all')
county.describe (include='all')

#%% Summarize the data

# display values grouped by date
daily = state.groupby('date').sum()
daily['pct_cases'] = daily['cases'].pct_change()
daily['pct_deaths'] = daily['deaths'].pct_change()
daily['cfr'] = daily['deaths'] / daily['cases']
daily.to_csv('output/daily.csv')
                                
# display values grouped by state
statecfr = state.groupby('state').sum()
statecfr['cfr'] = statecfr['deaths'] / statecfr['cases']           
statecfr.to_csv('output/statecfr.csv')
statecfr.sort_values('cfr')
statecfr.sort_values('cfr', ascending=False)

# display values grouped by county
countycfr = county.groupby('county').sum()
countycfr['cfr'] = countycfr['deaths'] / countycfr['cases']
countycfr.to_csv('output/countycfr.csv')
countycfr.sort_values('cfr', ascending=False)

#%% Visualize the data

# plot cases and deaths over time
dcd = daily.plot.line(y=['cases','deaths'])
dcd.set(xlabel='Date',ylabel="Ammount", title="Cases and Deaths over Time")
dcd.get_figure()
dcd.get_figure().savefig('output/Time_Cases&Death.jpg', bbox_inches='tight')

# plot case fatality rate over time 
cfr = daily.plot.line(y='cfr')
cfr.set(xlabel='Date', ylabel='Ammount', title="Case Fataltity Rate over Time")
cfr.get_figure()
cfr.get_figure().savefig('output/Time_CFR.jpg', bbox_inches='tight')

# plot case growth rate over time
# dailygr = daily[daily.cases >= 10]
growth = daily.plot.line(y='cases', logy=True)
growth.set(title="Case Growth Rate USA Over Time", xlabel="Date", ylabel= "Ammount")
growth.get_figure()
growth.get_figure().savefig('output/Case_CGR.jpg', bbox_inches='tight')

# comapre the case growth rate to multiple states
states_compare = ['New York', 'California', 'Florida']
stategr = state[state['state'].isin(states_compare)]
stategrc= stategr[stategr.cases >=10] 
stategr_plot = stategrc.groupby(['date', 'state'])['cases'].sum()
stategr_plotf = stategr_plot.unstack().plot(logy=True)
stategr_plotf.set(title="Case Growth Rate by State", xlabel="Date", ylabel="Ammount")
stategr_plotf.get_figure()
stategr_plotf.get_figure().savefig('output/Case_CGRS.jpg', bbox_inches='tight')

#%% Insights from the past day

yesterday = datetime.today() - timedelta(days = 2)
yesterdayf = yesterday.strftime('%Y-%m-%d')

statepred = state[state.date >= yesterdayf]
statepredgroup = statepred.groupby(['state', 'date']).sum()
statepredgroup['new_cases'] = statepredgroup.sort_values(['state','date']).groupby('state')['cases'].diff()
statepredgroup['pct_increase'] = statepredgroup.sort_values(['state','date']).groupby('state')['cases'].pct_change()
statechanges = statepredgroup.dropna(subset=['new_cases'])

countypred = county
countypred['new_cases'] = countypred.sort_values(['date']).groupby('fips')['cases'].diff()
countypred['pct_increase'] = countypred.sort_values(['date']).groupby('fips')['cases'].pct_change()
countydrop = countypred.dropna(subset=['new_cases'])
countychanges = countydrop[countypred.date >= yesterday]
