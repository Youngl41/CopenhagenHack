#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 12:35:41 2018

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

# Check if name is inside the list of names
def check_name(name, list_of_names):
    if name in list_of_names:
        return 'Yes'
    else:
        return 'No'

# =============================================================================
# Load Data
# =============================================================================
# Paths
main_dir = '/Users/Hackathon/CopenhagenHack/Data/Copenhagen-shp/shape'
working_dir = '/Users/Hackathon/CopenhagenHack/Working'

#loc_path = os.path.join(data_dir, 'clean_loc.csv')
google_places_path = os.path.join(working_dir, 'clean_google_places.csv')
crowdiness_path = os.path.join(working_dir, 'crowdiness.csv')
sample_loc_path = os.path.join(working_dir, 'sample_loc.csv')
weather_path = os.path.join(working_dir, 'clean_weather_hist.csv')
google_restaurants_path = os.path.join(working_dir, 'clean_google_restaurant.csv')

sample_loc_pdf = pd.read_csv(sample_loc_path, parse_dates=['date'])
#loc_pdf = pd.read_csv(loc_path, parse_dates=['date'])
google_places_pdf = pd.read_csv(google_places_path)
crowdiness_pdf = pd.read_csv(crowdiness_path)
weather_pdf = pd.read_csv(weather_path)
google_rest_pdf = pd.read_csv(google_restaurants_path)

# Location data
#loc_polys = list(map(lambda x: Point(x[0], x[1]), np.array(loc_pdf[['longitude', 'latitude']])))
sample_loc_pdf.loc[:, 'date'] = pd.to_datetime(sample_loc_pdf.date).dt.date
crowdiness_pdf.loc[:, 'date'] = pd.to_datetime(crowdiness_pdf.date).dt.date

# Weather data
weather_pdf.loc[:, 'datetime'] = pd.to_datetime(weather_pdf.time_tuple)
weather_pdf.loc[:, 'hour'] = weather_pdf.datetime.dt.hour
weather_pdf.loc[:, 'date'] = weather_pdf.datetime.dt.date


# =============================================================================
# Calculate Nearest Places
# =============================================================================
#loc_pdf.iloc[1998453]
longitude = 12.572031123921613
latitude = 55.67274264022657
date = datetime.date(2018, 5, 3)
hour = 16
segment = 'Family Person'
visited_places = ['Ny Carlsberg Glyptotek',
 "Ripley's Believe It or Not! Museum",
 'Eksperimentariet',
 'The Danish Film Institute, Museum and Cinema',
 'Experimentarium',
 'Galleri Tom Christoffersen',
 'H.C. Andersen Eventyrhuset',
 "Ripley's Museum",
 'City Hall Square',
 'Charlottenborg Palace',
 'Cinemateket']
num_places_visited = len(visited_places)

# Calculate close places
google_places_pdf.loc[:, 'proximity'] = list(map(lambda x: hav_dist(x[0], x[1], longitude, latitude), np.array(google_places_pdf[['lng', 'lat']])))
closest_places_pdf = google_places_pdf[google_places_pdf['proximity'] < 400]
filtered_crowdiness_pdf = crowdiness_pdf[(crowdiness_pdf['date'] == date) & 
                                            (crowdiness_pdf['hour'] == hour)][['name', 'capacity', 'num_users', 'traffic', 'traffic_class']]
nearby_places_now_pdf = pd.merge(closest_places_pdf, filtered_crowdiness_pdf, on=['name'], how='inner')
nearby_places_now_pdf = nearby_places_now_pdf[['formatted_address',
       'formatted_phone_number', 'icon',
       'international_phone_number', 'name', 'opening_hours', 'photos',
       'rating', 'reviews', 'types', 'url', 'vicinity', 'website', 'neg_sentiment', 'neu_sentiment', 'pos_sentiment',
       'overall_sentiment_score', 'tweet_text', 'overall_twitter_sentiment', 'lng',
       'lat', 'proximity', 'capacity', 'num_users', 'traffic',
       'traffic_class']]
nearby_places_now_pdf.loc[:, 'visited_already'] = list(map(lambda x: check_name(x, visited_places), nearby_places_now_pdf.loc[:, 'name']))
nearby_places_now_pdf.loc[:, 'PREDICTED_SATISFACTION'] = list(np.array(nearby_places_now_pdf.loc[:, 'rating']) * np.random.uniform(0.90, 0.99,size=(1,len(nearby_places_now_pdf.loc[:, 'rating'])))[0])
nearby_places_now_pdf.to_csv(os.path.join(working_dir, 'temp_output.csv'), index=False)
person_metadata = pd.DataFrame([longitude, latitude, date, hour, segment, num_places_visited]).transpose()
person_metadata.columns = ['longitude', 'latitude', 'date', 'hour', 'segment', 'num_places_visited']
person_metadata.to_csv(os.path.join(working_dir, 'temp_person_coord.csv'), index=False)

weather_now_pdf = weather_pdf[(weather_pdf['date'] == date) &
            (weather_pdf['hour'] == hour)].iloc[0]
weather_now_pdf.to_csv(os.path.join(working_dir, 'temp_weather.csv'), index=False)



