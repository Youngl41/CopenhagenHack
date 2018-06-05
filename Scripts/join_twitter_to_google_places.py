#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 12:03:17 2018

@author: Young
"""


# Import general modules
import os
import sys
import copy
import json
import numpy as np
import pandas as pd
import random
import datetime
from pprint import pprint
from collections import Counter

# Import geospatial modules
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection

# Custom utility functions
util_dir = '/Users/Hackathon/CopenhagenHack/Scripts/Utility Functions'
sys.path.append(util_dir)


# =============================================================================
# Utility Functions
# =============================================================================
# Haversine distance
def hav_dist(long1, lat1, long2, lat2):
    long1_ = long1 * np.pi / 180
    lat1_ = lat1 * np.pi / 180
    long2_ = long2 * np.pi / 180
    lat2_ = lat2 * np.pi / 180
    r = 6371000
    def hav(angle):
        return np.sin(angle/2.0)**2
    
    dist = 2 * r * np.arcsin(np.sqrt(hav(lat2_ - lat1_) + np.cos(lat1_) * np.cos(lat2_) * hav(long2_ - long1_)))
    return dist


# =============================================================================
# Load Data
# =============================================================================
data_dir = '/Users/Hackathon/CopenhagenHack/Data'
working_dir = '/Users/Hackathon/CopenhagenHack/Working'

twitter_sentiment_path = os.path.join(data_dir, '2018-06-05_sentiment.csv')
google_places_path = os.path.join(working_dir, 'clean_google_places.csv')

google_places_pdf = pd.read_csv(google_places_path)
twitter_sentiment_pdf = pd.read_csv(twitter_sentiment_path)



list_of_closest_places_to_tweet = []
for idx, row in twitter_sentiment_pdf.iterrows():
    longitude_ = row['longitude']
    latitude_ = row['latitude']
    google_places_pdf_ = copy.deepcopy(google_places_pdf)
    google_places_pdf_.loc[:, 'proximity'] = list(map(lambda x: hav_dist(x[0], x[1], longitude_, latitude_), np.array(google_places_pdf_[['lng', 'lat']])))
    closest_place = google_places_pdf_.sort_values('proximity').iloc[0]['name']
    list_of_closest_places_to_tweet.append(closest_place)

twitter_sentiment_pdf.loc[:, 'place'] = list_of_closest_places_to_tweet
twitter_sentiment_pdf = twitter_sentiment_pdf[['tweet_text',
       'compound', 'place']]
twitter_sentiment_pdf.columns = ['tweet_text', 'overall_twitter_sentiment', 'place']

google_places_tweet_pdf = pd.merge(google_places_pdf,twitter_sentiment_pdf, left_on='name', right_on='place', how='left')
google_places_tweet_pdf = google_places_tweet_pdf.drop_duplicates()

google_places_tweet_pdf.to_csv(google_places_path, index=False)
