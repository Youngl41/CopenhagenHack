#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 14:48:34 2018

@author: Young
"""

# =============================================================================
# Import Modules
# =============================================================================
import json
import pandas as pd
import datetime
import os

data_path = '/Users/Hackathon/CopenhagenHack/Data/2018-06-04_copenhagen.txt'


# =============================================================================
# Map Function
# =============================================================================
def map_process_json(json_data):
    # Capture tweet text
    tweet_text = json_data['text'].lower()
    #tweet_text = unicode_data.normalize('NFKD', tweet_text).encode('ascii','ignore').strip('"')
    if len(tweet_text) > 160:
        tweet_text = tweet_text[0:160]
    
    # The following objects are nullable
    if json_data['entities']['urls'] != []:
        url = json_data['entities']['urls'][0]['expanded_url']
        url = str(url)
        if len(url) > 160 :
            url = json_data['entities']['urls'][0]['url']
    else:
        url = str('').encode('ascii','ignore')
    
    # Obtain hashtags
    if json_data['entities']['hashtags'] !=[]:
        hashtags = [];
        for i in range(0,len(json_data['entities']['hashtags'])):
            hashtags.append(json_data['entities']['hashtags'][i]['text'].lower())
    else:
        hashtags = str('')
    
    # Obtain coordinates
    if json_data['coordinates'] != None: 
        latitude = json_data['coordinates']['coordinates'][1]
    else:
        latitude = float(0)
    if json_data['coordinates'] != None: 
        longitude = json_data['coordinates']['coordinates'][0]
    else:
        longitude = float(0)
        
    # Obtain time
    created_at = json_data['timestamp_ms']
    created_at = int(created_at)
    
    userid = json_data['user']['id']
    
    username = json_data['user']['name'].lower()
    #username = unicode_data.normalize('NFKD', username).encode('ascii','ignore').strip('"')
    
    return userid, username, json_data['user']['screen_name'], json_data['user']['followers_count'], json_data['user']['friends_count'], tweet_text, url, latitude, longitude, created_at, json_data['retweet_count'], hashtags


# =============================================================================
# Main
# =============================================================================
if __name__ == '__main__':
    file = open(data_path, 'r')
    a = file.read()
    
    # Convert large string to list of strings
    list_of_jsons = list(map(lambda x: x+'}', a.split('}\n')))[:-1]
    
    # Apply map job to invidual json files
    list_of_results = []
    for idx, json_str in enumerate(list_of_jsons):
        data = json.loads(json_str)
        try:
            list_of_results.append(map_process_json(data))
        except KeyError:
            pass
    
    # Convert to PDF
    processed_tweet_pdf = pd.DataFrame(list_of_results)
    processed_tweet_pdf.columns = ['userid', 'username', 'screen_name', 'followers_count', 'friends_count', 'tweet_text', 'url', 'latitude', 'longitude', 'created_at', 'retweet_count', 'hashtags']
    
    # Set a timestamp for the filename later
    timestamp = datetime.date.today()
    timestamp = str(timestamp)
            
            
    processed_tweet_pdf.to_csv('/Users/Hackathon/CopenhagenHack/Data/' + os.path.basename(data_path).split('_')[0] + '_' + 'copenhagen.csv')

