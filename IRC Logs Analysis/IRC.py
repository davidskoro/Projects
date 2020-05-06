# -*- coding: utf-8 -*-
"""
Created on Tue May  5 00:54:29 2020

@author: David
"""

#%% Imports

import re
import pandas as pd

#%% Build functions

# Find messages
def is_message(row):
    if re.search(r'<', row[6]):
        print('Row :', row)
        return True
    return False

# Get Username
def get_user_name (row):
    #print('get_user_name: row = ', row)
    username = re.search (r'<([ +%~@&])([-|\[\]\w\^\{\}\\\`]+)>', row)
    #print('in get_user_name:' , username.group(2))
    return username.group(2)
    
# Get Message
def get_chat_message(row):
    row_parts = re.split(r'> ', row)
    #print( 'Row Part', row_parts)
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

chat_records_df = pd.DataFrame(chat_records)

username_df = pd.DataFrame()
username_df['Username'] = chat_records_df['username']
username_df['Message Count'] = 1
username_df = username_df[username_df.Username != 'evilbot']
username_count = username_df.groupby('Username').count()
username_count = username_count.sort_values('Message Count', ascending = False)

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

login_ID_df = pd.DataFrame(login_records)
login_ID_df ['Logins'] = 1
login_count = login_ID_df.groupby('LoginID').count()
login_count = login_count.sort_values('Logins', ascending = False)


