#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 09:22:04 2018

@author: Young
"""


# Import general modules
import os
import sys
import json
import numpy as np
import pandas as pd
import datetime
from pprint import pprint
from collections import Counter

# Import geospatial modules
import fiona
import PIL.Image as im
import matplotlib.pyplot as plt

from fiona import collection
from descartes import PolygonPatch

from matplotlib.collections import PatchCollection
from shapely.geometry import Polygon, MultiPolygon, shape, Point

# Custom utility functions
util_dir = '/Users/Hackathon/CopenhagenHack/Scripts/Utility Functions'
sys.path.append(util_dir)
from gen_util import save_data
from gen_util import load_data
from geo_util import hav_dist
from geo_util import plot_shapes
from geo_util import convert2shape
from geo_util import map_pipe_props_to_pandas
from munge_util import chunk_items
    

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

sample_loc_pdf = pd.read_csv(sample_loc_path, parse_dates=['date'])
#loc_pdf = pd.read_csv(loc_path, parse_dates=['date'])
google_places_pdf = pd.read_csv(google_places_path)
crowdiness_pdf = pd.read_csv(crowdiness_path)
weather_pdf = pd.read_csv(weather_path)

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

# Calculate close places
google_places_pdf.loc[:, 'proximity'] = list(map(lambda x: hav_dist(x[0], x[1], longitude, latitude), np.array(google_places_pdf[['lng', 'lat']])))
closest_places_pdf = google_places_pdf[google_places_pdf['proximity'] < 400]
filtered_crowdiness_pdf = crowdiness_pdf[(crowdiness_pdf['date'] == date) & 
                                            (crowdiness_pdf['hour'] == hour)][['name', 'capacity', 'num_users', 'traffic', 'traffic_class']]
nearby_places_now_pdf = pd.merge(closest_places_pdf, filtered_crowdiness_pdf, on=['name'], how='inner')
nearby_places_now_pdf = nearby_places_now_pdf[['formatted_address',
       'formatted_phone_number', 'icon',
       'international_phone_number', 'name', 'opening_hours', 'photos',
       'rating', 'reviews', 'types', 'url', 'vicinity', 'website', 'lng',
       'lat', 'proximity', 'capacity', 'num_users', 'traffic',
       'traffic_class']]
nearby_places_now_pdf

weather_now_pdf = weather_pdf[(weather_pdf['date'] == date) &
            (weather_pdf['hour'] == hour)].iloc[0]
weather_now_pdf


# =============================================================================
# Randomly Generate New Coordinates
# =============================================================================
import random
#sample_loc_pdf = loc_pdf[(loc_pdf['date'] >= datetime.date(2018, 5, 1)) & 
#              (loc_pdf['date'] < datetime.date(2018, 5, 4))]
#sample_loc_pdf = sample_loc_pdf.reset_index(drop = True)
#sample_loc_pdf.to_csv(sample_loc_path, index=False)
random_idx = random.sample(list(sample_loc_pdf.index.values), 1)[0]

longitude = sample_loc_pdf.iloc[random_idx].longitude
latitude = sample_loc_pdf.iloc[random_idx].latitude
date = sample_loc_pdf.iloc[random_idx].date
hour = sample_loc_pdf.iloc[random_idx].hour

# Calculate close places
google_places_pdf.loc[:, 'proximity'] = list(map(lambda x: hav_dist(x[0], x[1], longitude, latitude), np.array(google_places_pdf[['lng', 'lat']])))
google_places_pdf[google_places_pdf['proximity'] < 400]


