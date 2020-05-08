# -*- coding: utf-8 -*-
"""
Created on Tue May  5 00:54:29 2020

@author: David
"""

#%% Imports

import re
import pandas as pd
from nltk.corpus import words

#%% Build functions

# Find all messages
def is_message(row):
    if re.search(r'<', row[6]):
        if re.search (r'(<\+evilbot>)', row):
            return False
        return True
    return False

# Get Username
def get_user_name (row):
    username = re.search (r'<([ +%~@&])([-|\[\]\w\^\{\}\\\`]+)>', row)
    return username.group(2)
    
# Get Message
def get_chat_message(row):
    row_parts = re.split(r'> ', row)
    message = '> '.join(row_parts[1:])
    print('Message:', message)
    return message

# Get log on
def get_log_on(row):
    logon = re.search(r'joined #hack', row)
    return logon

# Get log on name
def log_on_name(row):
    loginid = re.search (r' ([\[])([\w\.`\[\]\|^_{\\}-]+)([@])', row)
    return loginid.group(2)

# Get individual words
def get_words(row):
    word_parts = re.split(r'(\w+)', row)
    print( 'Row Part', word_parts)
    words = word_parts[7:]
    print('Words:', words)
    return words  

# Find all dark web links
def get_onion (row):
    if re.search (r'(\w+)(\.onion)', row):
        print('Onion:', row)
        return True
    return False

# Get all darkweb links
def darkweb_sites (row):
    site_row = re.search (r'(\w+)(\.onion)', row)
    return site_row.group()

# Find all URLs
def find_URL (row):
    if re.search (r'(\S+\.\w+\.\D\S+)(\s)', row):
        print('Line:', row)
        return True
    return False

# Get all URLs
def get_url (row):
    site_url = re.search (r'(\S+\.\w+\.\D\S+)(\s)', row)
    return site_url.group(1)

# Get individual hour
def get_hour(row):
    time_hour = re.split(r'(\w+)', row)
    hour = time_hour[1]
    print('Hour:', hour)
    return hour  

#%% Open the data

raw_log = ""
with open('hackers.log', 'r+', errors='ignore') as f:
    raw_log = f.readlines()
    
# Select rows
raw_log = raw_log #[]

#%% Create for loop to iterate through rows for username and message
    
chat_records = []


for row in raw_log :
    if is_message(row):
        print('Row :', row)
        username = get_user_name(row)
        print("Username :", username)   
        message = get_chat_message(row)
        chat_row = {'username': username, 'message': message}
        chat_records.append(chat_row)
    else:
        pass

# All chat messages 
chat_records_df = pd.DataFrame(chat_records)

# All usernames that sent a message and the ammount of messages each username sent 
username_df = pd.DataFrame()
username_df['Username'] = chat_records_df['username']
username_df['Message Count'] = 1
username_count = username_df.groupby('Username').count()
username_count = username_count.sort_values('Message Count', ascending = False)

# Total number of written messages
chat_records_df[['message']].count()

#%% Create for loop to iterate through rows for Log in

login_records = []

for row in raw_log :
    if get_log_on(row):
        print("Found Log:", row)
        logid = log_on_name(row)
        print("LoginID:", logid)
        Login_names = {'LoginID': logid}
        login_records.append(Login_names)
    else:
        pass

# All logins (Different then username) and how many times they logged in
login_ID_df = pd.DataFrame(login_records)
login_ID_df ['Logins'] = 1
login_count = login_ID_df.groupby('LoginID').count()
login_count = login_count.sort_values('Logins', ascending = False)

#%% Create a for loop to iterate through rows, seperating into individual words and counting most common

allwords = []

for row in raw_log :
    if is_message(row):
        all_words = get_words(row)
        allwords.extend(all_words)
    else:
        pass

# All words and frequency
word_df = pd.DataFrame(allwords)
word_df.rename(columns= {0:'Word'}, inplace=True)
word_df ['Count'] = 1
word_df = word_df[word_df.Word != " "][word_df.Word != "\n"][word_df.Word != " \n"][word_df.Word != ', \n']
word_count = word_df.groupby('Word').count()

#%% Create a for loop to iterate throws rows, retrieving all .onion links

darkweb = []

for row in raw_log:
    if get_onion(row):
        darksite = darkweb_sites(row)
        print('Dark Web:', darksite)
        darkweb.append(darksite)
    else:
        pass

#%% Messages by hour of the day

hours = []

for row in raw_log:
    if is_message(row):
        print('Row:',row)
        hour = get_hour(row)
        hours.append(hour)
    else:
        pass
        
# Hour of the day with the most messages
hours_df = pd.DataFrame(hours)
hours_df.rename(columns= {0:'Hour of Day'}, inplace=True)
hours_df ['Count'] = 1
hours_count = hours_df.groupby('Hour of Day').count()
hours_count = hours_count.sort_values('Count', ascending = False)

#%% Create for loop to iterate through rows, retriveing all urls

url = []

for row in raw_log:
    if is_message (row):
        if find_URL(row):
            url_found = get_url(row)
            print('URL:', url_found)
            url.append(url_found)
    else:
        pass

# Distinct URls
distinct_URL = set(url)
print(len(distinct_URL))

# Most posted URls
url_df = pd.DataFrame(url)
url_df.rename(columns= {0: "URL"}, inplace=True)
url_df ['Count'] = 1
url_count = url_df.groupby("URL").count()
url_count = url_count.sort_values('Count', ascending = False)
# Top 5 most posted URls
url_top5 = url_count.head()

#%%

# Create list of all words within words dictonary
word_list = words.words()

# Create new dataframe for editing out recognized words
noneng = word_count
non_eng = noneng.drop(word_list, errors='ignore') # Drop all words lsited within the words list

