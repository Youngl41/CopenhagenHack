#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 11:51:29 2018

@author: Young
"""


# Import general modules
import os
import sys
import numpy as np
import pandas as pd
from pprint import pprint
from datetime import datetime
from datetime import timedelta
from collections import Counter

# Custom utility functions
util_dir = '/Users/Hackathon/CopenhagenHack/Scripts/Utility Functions'
sys.path.append(util_dir)
from gen_util import save_data
from gen_util import load_data
from geo_util import plot_shapes
from geo_util import convert2shape
from geo_util import map_pipe_props_to_pandas
from munge_util import chunk_items


# =============================================================================
# Data Paths
# =============================================================================
data_dir = '/Users/Hackathon/CopenhagenHack/Data'
woco_location_path = os.path.join(data_dir, 'woco_location_data.csv')
woco_weather_path = os.path.join(data_dir, 'woco_weather_data.csv')

# Save data
loc_save_path = os.path.join(data_dir, 'clean_loc.csv')
customer_save_path = os.path.join(data_dir, 'clean_customer.csv')
weather_hist_save_path = os.path.join(data_dir, 'clean_weather_hist.csv')


# =============================================================================
# # Location Data
# =============================================================================
# Load data
loc_pdf = pd.read_csv(woco_location_path)

# Select correct columns
loc_pdf = loc_pdf[['timestamp', 'longitude', 'latitude', 'country',
       'language', 'unique_id']]

# Drop duplicates
loc_pdf = loc_pdf.drop_duplicates()

# Convert time string into datetime time tuple
#t = loc_pdf.timestamp.iloc[0]
loc_pdf.loc[:, 'time_tuple'] = list(map(lambda time_str: datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.000Z"), loc_pdf.loc[:, 'timestamp']))
#loc_pdf['language'].value_counts()

# Sort values
loc_pdf = loc_pdf.sort_values(['unique_id', 'time_tuple'])

# Customer language
latest_customer_lang_pdf = loc_pdf[['unique_id', 'country', 'language']].drop_duplicates(subset=['unique_id'], keep='last')
latest_customer_lang_pdf = latest_customer_lang_pdf.reset_index(drop=True)

# Remove language
loc_pdf = loc_pdf[['unique_id', 'time_tuple', 'longitude', 'latitude']]
loc_pdf = loc_pdf.reset_index(drop=True)

# Save data
loc_pdf.to_csv(loc_save_path, index=False)
latest_customer_lang_pdf.to_csv(customer_save_path, index=False)
loc_pdf.iloc[:500].to_csv(os.path.join(data_dir, 'clean_sample_loc.csv'), index=False)

# =============================================================================
# Weather Data
# =============================================================================
# Load data
weather_hist_pdf = pd.read_csv(woco_weather_path)

# Drop duplicates
weather_hist_pdf = weather_hist_pdf.drop_duplicates()

# Convert time string into datetime time tuple
#t = loc_pdf.timestamp.iloc[0]
weather_hist_pdf.loc[:, 'time_tuple'] = list(map(lambda time_str: datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.000Z"), weather_hist_pdf.loc[:, 'timestamp']))

# Select correct columns
weather_hist_pdf = weather_hist_pdf[['time_tuple', 'weather_summary', 'temperature', 'pressure', 'humidity',
       'visibility', 'wind_speed', 'wind_direction', 'cloud_coverage']]

# Sort by date
weather_hist_pdf = weather_hist_pdf.sort_values('time_tuple')

# Weather forecast (faked)
weather_forecast_pdf = 

weather_hist_pdf['time_tuple'].iloc[0] + timedelta(days=1)

# Save data
weather_hist_pdf.to_csv(weather_hist_save_path, index=False)

