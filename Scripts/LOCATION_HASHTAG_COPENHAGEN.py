#!/usr/bin/python2.7

# -*- coding: utf-8 -*-

"""
Created on Sun May  1 15:49:01 2016

@author: Mia
"""



import json
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from twitter import OAuth, TwitterStream
import unicodedata
import datetime

__author__ = 'Mia Carina Mayer'


def getConnection():
    # http://initd.org/psycopg/docs/usage.html
    connection = psycopg2.connect(user="postgres", password="Hufkpas4%")
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    return connection


def getDatabase(db):
    # http://initd.org/psycopg/docs/usage.html
    connection = psycopg2.connect(database=db, user="postgres", password="Hufkpas4%")
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    return connection


def submitToDatabase(query, query_values, connection):
    answer = connection.cursor()
    answer = answer.execute(query,(query_values))
    return answer


def normalizeText(tweet_text):
    str_text = tweet_text
    normalizedText = '\'' + str_text.replace("'", r"''") + '\''
    return normalizedText


consumer_key = "Ko7MJsiRheT0uqdTIxs4tlRoN"
consumer_secret = "37txp8tG4aujvVlzJxO4amx6fH25dfzpS6UiBPBwDcwL8jHv9o"

access_token = "1957759963-3s7YRnFDuhLl1bguOvoVl4jW7teuYLCuBENLas1"
access_secret = 'Ehde1kXD2k68FwqvjMWrkiga4ulqhDNSKQk1CfTcKyjTy'

raw_connection = getConnection()

if __name__ == "__main__":

    
    # Create the DataBase
    database_create = "CREATE DATABASE copenhagen_hack WITH OWNER = mia ENCODING = 'UTF8' TABLESPACE = pg_default;"
    
    # Submit CREATE  database     
    submitToDatabase(database_create, (), raw_connection)
    raw_connection.close()
       
    # Create the Tables                                      
    tweet_table_create = "CREATE TABLE IF NOT EXISTS tweets (id serial PRIMARY KEY, user_id char(50) NOT NULL, text char(160) NOT NULL, URL char(160) NOT NULL, latitude float, longitude float, created_at bigint, retweet_count int NOT NULL, hashtags character varying (160));"
    twitter_users_create = "CREATE TABLE IF NOT EXISTS twitter_users (id serial PRIMARY KEY, user_id char(50) NOT NULL, user_name char(50) NOT NULL, screen_name char(50) NOT NULL, followers_count int NOT NULL, friends_count int NOT NULL);"
    
    # Submit CREATE tables
    database_connection = getDatabase("copenhagen_hack")
    submitToDatabase(tweet_table_create, (), database_connection)
    submitToDatabase(twitter_users_create, (), database_connection)

    # Create authentication for Twitter
    oauth = OAuth(access_token, access_secret, consumer_key, consumer_secret)
    
    # Initiate the connection to Twitter Streaming API
    twitter_stream = TwitterStream(auth=oauth)
    
    # Get a sample of the public data following through Twitter (just Europe)
    iterator = twitter_stream.statuses.filter(locations= "12.4529,55.6150,12.6507,55.7326")
    
    # http://isithackday.com/geoplanet-explorer/index.php? Order: SW 2nd value, SW 1st value, NE 2nd value, NE 1st value
    # Copenhagen 12.4529, 55.6150, 12.6507, 55.7326



    # Set tweet count to zero
    tweet_count = 0
       
    for tweet in iterator:
        try:
            # Increase the tweet count by one
            tweet_count += 1
            print (tweet_count)
                
            # Set a timestamp for the filename later
            timestamp = datetime.date.today()
            timestamp = str(timestamp)
        
            # Dump tweet as json into data
            backup_data = json.dumps(tweet)
            backup_data = backup_data.lower()
        
            # Print the tweets so you see something happening
            
            if 'copenhagen' in backup_data: 
                print (backup_data)
                # Open file and dump data into it
                with open('/Users/Hackathon/CopenhagenHack/Data/' + timestamp + '_' + 'copenhagen.txt', 'a') as outfile:
                    outfile.write(backup_data + '\n')
            
                # Close file to avoid conflict
                outfile.close()
        
            # Create timeline of tweets for database
            timelineTweetsJson = json.dumps(tweet)
            
            data = json.loads(timelineTweetsJson)
    
            # Capture tweet text
                
            tweet_text = data['text'].lower()
            tweet_text = unicodedata.normalize('NFKD', tweet_text).encode('ascii','ignore').strip('"')
            if len(tweet_text) > 160:
                tweet_text = tweet_text[0:160]

            # The following objects are nullable
            if data['entities']['urls'] != []:
                url = data['entities']['urls'][0]['expanded_url']
                url = str(url)
                if len(url) > 160 :
                    url = data['entities']['urls'][0]['url']
            else:
                url = str('').encode('ascii','ignore')
            
            # Obtain hashtags
            if data['entities']['hashtags'] !=[]:
                hashtags = [];
                for i in range(0,len(data['entities']['hashtags'])):              
                    hashtags.append(data['entities']['hashtags'][i]['text'].lower())
            else:
                hashtags = str('')
            
            # Obtain coordinates
            if data['coordinates'] != None: 
                latitude = data['coordinates']['coordinates'][1]
            else:
                latitude = float(0)
            if data['coordinates'] != None: 
                longitude = data['coordinates']['coordinates'][0]
            else:
                longitude = float(0)
                
            # Obtain time
            created_at = data['timestamp_ms']
            created_at = int(created_at)
            
            userid = data['user']['id']
            
            username = data['user']['name'].lower()
            username = unicodedata.normalize('NFKD', username).encode('ascii','ignore').strip('"')
            
            
            # Set query values for tweets table
            values_tweets = userid, tweet_text, url, latitude, longitude, created_at, data['retweet_count'], hashtags
            query_tweets = "INSERT INTO tweets (user_id, text, URL, latitude, longitude, created_at, retweet_count, hashtags) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s);" 
            submitToDatabase(query_tweets, values_tweets, database_connection)
                
                
            # Set query values for user table
            values_users = userid, username, data['user']['screen_name'], data['user']['followers_count'], data['user']['friends_count']
            query_users = "INSERT INTO twitter_users (user_id, user_name, screen_name, followers_count, friends_count) VALUES (%s, %s, %s, %s, %s);" 
            submitToDatabase(query_users, values_users, database_connection)
            
            
        except (RuntimeError, TypeError, NameError):
            pass
                

