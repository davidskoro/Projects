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

# display values grouped by state
statecfr = state.groupby('state').sum()
statecfr['cfr'] = statecfr['deaths'] / statecfr['cases']

# display values grouped by county
countycfr = county.groupby('county').sum()
countycfr['cfr'] = countycfr['deaths'] / countycfr['cases']

#%% Visualize the data

# plot cases and deaths over time
daily.plot.line(y=['cases','deaths'])

# plot case fatality rare over time 
daily.plot.line(y='cfr')    

#%%
