#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 12:42:20 2018

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
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

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
main_dir = '/Users/GitHub/CopenhagenHack/Data/Copenhagen-shp/shape'
working_dir = '/Users/GitHub/CopenhagenHack/Working'

# Custom utility functions
util_dir = '/Users/GitHub/CopenhagenHack/Scripts/Utility Functions'
sys.path.append(util_dir)


print('When R application starts it creates an empty clicked coordinates file which can cause errors.')



class Watcher:
    DIRECTORY_TO_WATCH = working_dir

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print ("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print ("Received created event - %s." % event.src_path )
            
            google_places_path = os.path.join(working_dir, 'clean_google_places.csv')
            crowdiness_path = os.path.join(working_dir, 'crowdiness.csv')
            sample_loc_path = os.path.join(working_dir, 'sample_loc.csv')
            weather_path = os.path.join(working_dir, 'clean_weather_hist.csv')
            google_restaurants_path = os.path.join(working_dir, 'clean_google_restaurant.csv')
            r_path = os.path.join(working_dir, 'clicked_coordinates.csv')
            
            sample_loc_pdf = pd.read_csv(sample_loc_path, parse_dates=['date'])
            google_places_pdf = pd.read_csv(google_places_path)
            crowdiness_pdf = pd.read_csv(crowdiness_path)
            weather_pdf = pd.read_csv(weather_path)
            google_rest_pdf = pd.read_csv(google_restaurants_path)
            r_coordinates_df = pd.read_csv(r_path)

            
            # Location data
            sample_loc_pdf.loc[:, 'date'] = pd.to_datetime(sample_loc_pdf.date).dt.date
            crowdiness_pdf.loc[:, 'date'] = pd.to_datetime(crowdiness_pdf.date).dt.date
            
            # Weather data
            weather_pdf.loc[:, 'datetime'] = pd.to_datetime(weather_pdf.time_tuple)
            weather_pdf.loc[:, 'hour'] = weather_pdf.datetime.dt.hour
            weather_pdf.loc[:, 'date'] = weather_pdf.datetime.dt.date
            
            
            
            sample_loc_pdf_ = copy.deepcopy(sample_loc_pdf)
            try:
                latitude = float(r_coordinates_df['lat'][0])
                longitude = float(r_coordinates_df['lng'][0])
             
            
                # =============================================================================
                #  Generation
                # =============================================================================
                            
                sample_loc_pdf_.loc[:, 'closeness'] = list(map(lambda x: hav_dist(x[0], x[1], longitude, latitude), np.array(sample_loc_pdf_[['longitude', 'latitude']])))
                closest_person_loc = sample_loc_pdf_.sort_values('closeness').iloc[0]
                
                np.random.seed(int(np.floor(longitude * 2298 * np.pi)))
                segment_list = ['Family Person', 'Businessman', 
                                'Highly Active Instagramer', 
                                'Teenager (on school trip)',
                                'Couple',
                                'Wealthy Traveler',
                                'Local',
                                'Businesswoman']
                segment = np.random.choice(segment_list)
                segment
                date = closest_person_loc.date
                hour = closest_person_loc.hour
                
                datetime_ = closest_person_loc.datetime
                past_locs_pdf = sample_loc_pdf[(sample_loc_pdf['unique_id'] == closest_person_loc['unique_id']) &
                                               (sample_loc_pdf['datetime'] < datetime_)]
                
                visited_places = set([])
                for idx, row in past_locs_pdf.iterrows():
                    longitude_ = row['longitude']
                    latitude_ = row['latitude']
                    google_places_pdf_ = copy.deepcopy(google_places_pdf)
                    google_places_pdf_.loc[:, 'proximity'] = list(map(lambda x: hav_dist(x[0], x[1], longitude_, latitude_), np.array(google_places_pdf_[['lng', 'lat']])))
                    visited_places = visited_places.union(set(google_places_pdf_[google_places_pdf_['proximity'] < 10]['name'].values))
                visited_places = list(visited_places)
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
            
            except(KeyError):
                print('Check if the clicked coordinates file is empty.')
                pass
            
            
        elif (event.event_type == 'modified') and (event.src_path == working_dir+'/clicked_coordinates.csv'):
            
            # Taken any action here when a file is modified.
            print ("Received modified event - %s." % event.src_path)
            google_places_path = os.path.join(working_dir, 'clean_google_places.csv')
            crowdiness_path = os.path.join(working_dir, 'crowdiness.csv')
            sample_loc_path = os.path.join(working_dir, 'sample_loc.csv')
            weather_path = os.path.join(working_dir, 'clean_weather_hist.csv')
            google_restaurants_path = os.path.join(working_dir, 'clean_google_restaurant.csv')
            r_path = os.path.join(working_dir, 'clicked_coordinates.csv')
            
            sample_loc_pdf = pd.read_csv(sample_loc_path, parse_dates=['date'])
            google_places_pdf = pd.read_csv(google_places_path)
            crowdiness_pdf = pd.read_csv(crowdiness_path)
            weather_pdf = pd.read_csv(weather_path)
            google_rest_pdf = pd.read_csv(google_restaurants_path)
            r_coordinates_df = pd.read_csv(r_path)

            
            # Location data
            sample_loc_pdf.loc[:, 'date'] = pd.to_datetime(sample_loc_pdf.date).dt.date
            crowdiness_pdf.loc[:, 'date'] = pd.to_datetime(crowdiness_pdf.date).dt.date
            
            # Weather data
            weather_pdf.loc[:, 'datetime'] = pd.to_datetime(weather_pdf.time_tuple)
            weather_pdf.loc[:, 'hour'] = weather_pdf.datetime.dt.hour
            weather_pdf.loc[:, 'date'] = weather_pdf.datetime.dt.date
            
            
            
            sample_loc_pdf_ = copy.deepcopy(sample_loc_pdf)
            try:
                latitude = float(r_coordinates_df['lat'][0])
                longitude = float(r_coordinates_df['lng'][0])
             
            
                # =============================================================================
                #  Generation
                # =============================================================================
                            
                sample_loc_pdf_.loc[:, 'closeness'] = list(map(lambda x: hav_dist(x[0], x[1], longitude, latitude), np.array(sample_loc_pdf_[['longitude', 'latitude']])))
                closest_person_loc = sample_loc_pdf_.sort_values('closeness').iloc[0]
                
                np.random.seed(int(np.floor(longitude * 2298 * np.pi)))
                segment_list = ['Family Person', 'Businessman', 
                                'Highly Active Instagramer', 
                                'Teenager (on school trip)',
                                'Couple',
                                'Wealthy Traveler',
                                'Local',
                                'Businesswoman']
                segment = np.random.choice(segment_list)
                segment
                date = closest_person_loc.date
                hour = closest_person_loc.hour
                
                datetime_ = closest_person_loc.datetime
                past_locs_pdf = sample_loc_pdf[(sample_loc_pdf['unique_id'] == closest_person_loc['unique_id']) &
                                               (sample_loc_pdf['datetime'] < datetime_)]
                
                visited_places = set([])
                for idx, row in past_locs_pdf.iterrows():
                    longitude_ = row['longitude']
                    latitude_ = row['latitude']
                    google_places_pdf_ = copy.deepcopy(google_places_pdf)
                    google_places_pdf_.loc[:, 'proximity'] = list(map(lambda x: hav_dist(x[0], x[1], longitude_, latitude_), np.array(google_places_pdf_[['lng', 'lat']])))
                    visited_places = visited_places.union(set(google_places_pdf_[google_places_pdf_['proximity'] < 10]['name'].values))
                visited_places = list(visited_places)
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
            
            except(KeyError):
                print('Check if the clicked coordinates file is empty.')
                pass
            
        else:
            pass
            


if __name__ == '__main__':
    w = Watcher()
    w.run()