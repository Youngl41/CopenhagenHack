#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 11:35:04 2018

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
data_dir = '/Users/Hackathon/CopenhagenHack/Data'
working_dir = '/Users/Hackathon/CopenhagenHack/Working'

loc_path = os.path.join(data_dir, 'clean_loc.csv')
google_rest_path = os.path.join(working_dir, 'clean_google_restaurant.csv')

# Load data
loc_pdf = pd.read_csv(loc_path, parse_dates=['date'])
google_rest_pdf = pd.read_csv(google_rest_path)

# Location data
loc_pdf.loc[:, 'date'] = pd.to_datetime(loc_pdf.date).dt.date

# Historical timestamps
hist_time_pdf = loc_pdf[['date', 'hour']].drop_duplicates().sort_values(['date', 'hour'])
hist_time_pdf = hist_time_pdf.iloc[1:]
hist_time_pdf = hist_time_pdf[(hist_time_pdf['date'] >= datetime.date(2018, 5, 1)) & 
              (hist_time_pdf['date'] < datetime.date(2018, 5, 4))].reset_index(drop=True)

# Get crowdiness level
google_rest_pdf.loc[:, 'tmp'] = 1
hist_time_pdf.loc[:, 'tmp'] = 1

places_by_hour_pdf = pd.merge(google_rest_pdf, hist_time_pdf, on='tmp')

places_by_hour_people_pdf = pd.merge(places_by_hour_pdf, loc_pdf[(loc_pdf['date'] >= datetime.date(2018, 5, 1)) & 
              (loc_pdf['date'] < datetime.date(2018, 5, 4))][['unique_id', 'date', 'hour', 'longitude', 'latitude']], on=['date','hour'], how='inner')

# Haversine dist
places_by_hour_people_pdf.loc[:, 'hav_dist'] = list(map(lambda x: hav_dist(x[0], x[1], x[2], x[3]), np.array(places_by_hour_people_pdf[['longitude', 'latitude', 'lng', 'lat']])))
places_by_hour_people_pdf = places_by_hour_people_pdf[places_by_hour_people_pdf['hav_dist'] < 100]

places_by_hour_people_pdf = places_by_hour_people_pdf[['name', 'date', 'hour', 'unique_id']].groupby(['name', 'date', 'hour'])['unique_id'].nunique().reset_index()

places_by_hour_people_pdf.columns = ['name', 'date', 'hour', 'num_users']

places_by_hour_pdf = pd.merge(places_by_hour_pdf, places_by_hour_people_pdf, on=['name', 'date', 'hour'], how = 'left')
places_by_hour_pdf.loc[:, 'num_users'] = places_by_hour_pdf.loc[:, 'num_users'].fillna(0)
place_capacity_pdf = places_by_hour_pdf.groupby(['name'])['num_users'].agg('max').reset_index()
place_capacity_pdf.columns = ['name', 'capacity']

crowdy_pdf = pd.merge(place_capacity_pdf, places_by_hour_pdf, on='name', how='inner')

def map_crowdy_calc(value):
    if value < 0.1:
        return 'Completely free'
    elif value < 0.5:
        return 'Free'
    elif value < 0.8:
        return 'Getting busy'
    else:
        return 'Busy'
    
crowdy_pdf.loc[:, 'traffic'] = crowdy_pdf.loc[:, 'num_users'] / crowdy_pdf.loc[:, 'capacity']
crowdy_pdf.loc[:, 'traffic_class'] = list(map(lambda x: map_crowdy_calc(x), crowdy_pdf.loc[:, 'traffic']))

working_dir = '/Users/Hackathon/CopenhagenHack/Working'
crowdy_pdf.to_csv(os.path.join(working_dir, 'crowdiness_rest.csv'), index=False)



