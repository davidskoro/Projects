# -*- coding: utf-8 -*-
"""
COVID-19 Analysis

"""

import pandas as pd

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

# plot case fatality rare over time 
cfr = daily.plot.line(y='cfr')
cfr.set(xlabel='Date', ylabel='Ammount', title="Case Fataltity Rate over Time")
cfr.get_figure()
cfr.get_figure().savefig('output/Time_CFR.jpg', bbox_inches='tight')

#%%
