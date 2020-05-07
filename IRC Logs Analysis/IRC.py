# -*- coding: utf-8 -*-
"""
Created on Tue May  5 00:54:29 2020

@author: David
"""

#%% Imports

import re
import pandas as pd

#%% Build functions

# Find all messages
def is_message(row):
    if re.search(r'<', row[6]):
        if re.search (r'(<\+evilbot>)', row):
            return False
        print('Row :', row)
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

def get_onion (row):
    if re.search (r'(\w+)(\.onion)', row):
        print('Onion:', row)
        return True
    return False

def darkweb_sites (row):
    site_row = re.search (r'(\w+)(\.onion)', row)
    return site_row.group()

#%% Open the data

raw_log = ""
with open('hackers.log', 'r+', errors='ignore') as f:
    raw_log = f.readlines()
    
# Select rows
raw_log = raw_log 

#%% Create for loop to iterate through rows for username and message
    
chat_records = []


for row in raw_log :
    if is_message(row):
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

#%% Create a for loop to iterate through for, seperating into individual words and counting most common

allwords = []

for row in raw_log :
    if is_message(row):
        all_words = get_words(row)
        allwords.extend(all_words)
    else:
        pass

word_df = pd.DataFrame(allwords)
word_df.rename(columns= {0:'Word'}, inplace=True)
word_df ['Count'] = 1
word_df = word_df[word_df.Word != " "][word_df.Word != "\n"][word_df.Word != " \n"][word_df.Word != ', \n']
word_count = word_df.groupby('Word').count()

#%%

darkweb = []

for row in raw_log:
    if get_onion(row):
        darksite = darkweb_sites(row)
        print('Dark Web:', darksite)
        darkweb.append(darksite)
    else:
        pass