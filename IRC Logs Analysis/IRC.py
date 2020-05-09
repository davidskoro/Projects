# -*- coding: utf-8 -*-
"""
-------------------------
IRC Logs - Text Analysis
-------------------------

Analyzed textual log data from an online chat forum 
associated with hacking and the dark web.

@author: David
"""

#%% Imports

import re
import pandas as pd
from nltk.corpus import words

#%% Build functions

def is_message(row):
    '''
    Find if a row contains a message

    Parameters
    ----------
    row: str
       row from chat log
    
    Returns
    ----------
    bool
        True if row contains a message  
    '''
    if re.search(r'<', row[6]): # Find rows that contain "<"
        if re.search (r'(<\+evilbot>)', row): # Filter out evilbot (chatbot)
            return False
        return True
    return False

def get_user_name (row):
    '''
    Get the username of someone who sent a message

    Parameters
    ----------
    row: str
       row from chat log
    
    Returns
    ----------
    String containing username
    '''
    username = re.search (r'<([ +%~@&])([-|\[\]\w\^\{\}\\\`]+)>', row) # Include all special characters used in Usernames
    return username.group(2)
    
# Get Message
def get_chat_message(row):
    '''
    Get message content

    Parameters
    ----------
    row: str
       row from chat log
    
    Returns
    ----------
    Sent message
    '''
    row_parts = re.split(r'> ', row) # Split on ">". Message begins after ">"
    message = '> '.join(row_parts[1:])
    print('Message:', message)
    return message

# Get log on
def get_log_on(row):
    '''
    Find if a user joined the chat room

    Parameters
    ----------
    row: str
       row from chat log
    
    Returns
    ----------
    Row in which the user joined
    '''
    logon = re.search(r'joined #hack', row) # Include all rows that contain "joined #hack"
    return logon

# Get log on name
def log_on_name(row):
    '''
    Get the loginID of a user that joined

    Parameters
    ----------
    row: str
       row from chat log
    
    Returns
    ----------
    LogID of user
    '''
    loginid = re.search (r' ([\[])([\w\.`\[\]\|^_{\\}-]+)([@])', row) # Include all special characters used in login names
    return loginid.group(2)

# Get individual words
def get_words(row):
    '''
    Get all words in a message

    Parameters
    ----------
    row: str
       row from chat log
    
    Returns
    ----------
    All words within the message content
    '''
    word_parts = re.split(r'(\w+)', row) # Split on every word
    print( 'Row Part', word_parts)
    words = word_parts[7:] # Select words after the username 
    print('Words:', words)
    return words  

# Find all dark web links
def get_onion (row):
    '''
    Find if a row contains a .onion link

    Parameters
    ----------
    row: str
       row from chat log
    
    Returns
    ----------
    bool
        True if row contains a .onion link 
    '''
    if re.search (r'(\S+)(\.onio)(\S+)', row): # Find rows that contain a word followed by ".onion"
        print('Onion:', row)
        return True
    return False

# Get all darkweb links
def darkweb_sites (row):
    '''
    Get a .onion link from row

    Parameters
    ----------
    row: str
       row from chat log
    
    Returns
    ----------
    The full .onion link
    '''
    site_row = re.search (r'(\S+)(\.onio)(\S+)', row) # Include rows that contain a word followed by ".onion"
    return site_row.group()

# Find all URLs
def find_URL (row):
    '''
    Find if a row contains a url

    Parameters
    ----------
    row: str
       row from chat log
    
    Returns
    ----------
    bool
        True if row contains a url
    '''
    if re.search (r'(\S+\.\w+\.\D\S+)(\s)', row): # Find rows that contain a url
        print('Line:', row)
        return True
    return False

# Get all URLs
def get_url (row):
    '''
    Get the url from a message

    Parameters
    ----------
    row: str
       row from chat log
    
    Returns
    ----------
    Full URL
    '''
    site_url = re.search (r'(\S+\.\w+\.\D\S+)(\s)', row) # Include rows that contain a url
    return site_url.group(1)

# Get individual hour
def get_hour(row):
    '''
    Get the hour a message was sent during

    Parameters
    ----------
    row: str
       row from chat log
    
    Returns
    ----------
    The hour in which the message was sent
    '''
    time_hour = re.split(r'(\w+)', row) # Split on every word
    hour = time_hour[1] # Select the 2nd word 
    print('Hour:', hour)
    return hour  

#%% Open the data

raw_log = ""
with open('hackers.log', 'r+', errors='ignore') as f:
    raw_log = f.readlines()
    
# Select rows
raw_log = raw_log [0:]

#%% Create for loop to iterate through rows for username and message

chat_records = [] # Dataframe for storing username and message


for row in raw_log :
    if is_message(row):
        print('Row :', row)
        username = get_user_name(row)
        print("Username :", username)   
        message = get_chat_message(row)
        chat_row = {'username': username, 'message': message}
        chat_records.append(chat_row) # Store chat_row values within the chat_records dataframe
    else:
        pass

# All chat messages stored as a dataframe
chat_records_df = pd.DataFrame(chat_records)

# All usernames that sent a message and the ammount of messages each username sent 
username_df = pd.DataFrame()
username_df['Username'] = chat_records_df['username']
username_df['Message Count'] = 1 # New column to count occurrences
username_count = username_df.groupby('Username').count() # How many messages sent by each username
username_count = username_count.sort_values('Message Count', ascending = False)
username_count.to_csv('output/Msgs_per_user.csv')

# Total number of written messages
chat_records_df[['message']].count()

#%% Create for loop to iterate through rows for Log in

login_records = [] #Dataframe for storing login records

for row in raw_log :
    if get_log_on(row):
        print("Found Log:", row)
        logid = log_on_name(row)
        print("LoginID:", logid)
        Login_names = {'LoginID': logid}
        login_records.append(Login_names) #Store login_names within the login_records dataframe
    else:
        pass

# All logins (Different then username) and how many times they logged in
login_ID_df = pd.DataFrame(login_records)
login_ID_df ['Logins'] = 1 #New column to count logins
login_count = login_ID_df.groupby('LoginID').count() #How many logins from each loginID
login_count = login_count.sort_values('Logins', ascending = False)
login_count.to_csv('output/Logins_per_LoginID.csv')

#%% Create a for loop to iterate through rows, seperating into individual words and counting most common 

allwords = [] #Dataframe for storing words

for row in raw_log :
    if is_message(row):
        all_words = get_words(row)
        allwords.extend(all_words) #Store word values within the allwords dataframe
    else:
        pass

# All words and frequency
word_df = pd.DataFrame(allwords)
word_df.rename(columns= {0:'Word'}, inplace=True)
word_df ['Count'] = 1 #New column to count frequency of word
word_df = word_df[word_df.Word != " "][word_df.Word != "\n"][word_df.Word != " \n"][word_df.Word != ', \n'][word_df.Word != ', '] # Filter out common non-words
word_count = word_df.groupby('Word').count() #How often each word was used
word_count = word_count.sort_values('Count', ascending=False)
word_count.to_csv('output/Mostcommon_words.csv')

#%% Create a for loop to iterate throws rows, retrieving all .onion links

darkweb = [] #Dataframe for storing darkweb sites

for row in raw_log:
    if get_onion(row):
        darksite = darkweb_sites(row)
        print('Dark Web:', darksite)
        darkweb.append(darksite) #Include .onion values within the darkweb dataframe
    else:
        pass
    
darkweb_sites = pd.DataFrame(darkweb)
darkweb_sites.rename(columns= {0:'Site'}, inplace=True)
darkweb_sites.to_csv('output/Darkweb_Sites.csv')

#%% Messages by hour of the day 

hours = [] #New dataframe to store hour values

for row in raw_log:
    if is_message(row):
        print('Row:',row)
        hour = get_hour(row)
        hours.append(hour) #Include the hour values within the hours dataframe
    else:
        pass
        
# Hour of the day with the most messages
hours_df = pd.DataFrame(hours)
hours_df.rename(columns= {0:'Hour of Day'}, inplace=True)
hours_df ['Count'] = 1 #New column to count frequency
hours_count = hours_df.groupby('Hour of Day').count() #How many msgs are sent by hour
hours_count = hours_count.sort_values('Count', ascending = False)
hours_count.to_csv('output/hourly_msgs.csv')

#%% Create for loop to iterate through rows, retriveing all urls

url = [] #New dataframe to store url values

for row in raw_log:
    if is_message (row):
        if find_URL(row):
            url_found = get_url(row)
            print('URL:', url_found)
            url.append(url_found) #Include the url values within the url dataframe
    else:
        pass

# Distinct URls
distinct_URL = set(url)
print(len(distinct_URL))

# Most posted URls
url_df = pd.DataFrame(url)
url_df.rename(columns= {0: "URL"}, inplace=True)
url_df ['Count'] = 1 #New column to count frequency
url_count = url_df.groupby("URL").count() #How many times is each url sent
url_count = url_count.sort_values('Count', ascending = False)
url_count.to_csv('output/URL_count.csv')

# Top 5 most posted URls
url_top5 = url_count.head()
url_top5.to_csv('output/URL_top5.csv')

#%% Find words not recognized in the english dictonary

# Create list of all english words within words dictonary
word_list = words.words()

# Create new dataframe for editing out recognized english words
noneng = word_count
non_eng = noneng.drop(word_list, errors='ignore') # Drop all words lsited within the words list

non_eng.to_csv('output/Mostcommon_NotEnglish.csv')
