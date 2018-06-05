#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 11:49:44 2018

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
# Load Data
# =============================================================================
main_dir = '/Users/Hackathon/CopenhagenHack/Data/Copenhagen-shp/shape'
working_dir = '/Users/Hackathon/CopenhagenHack/Working'
data_dir = '/Users/Hackathon/CopenhagenHack/Data'

#loc_path = os.path.join(data_dir, 'clean_loc.csv')
google_places_path = os.path.join(working_dir, 'clean_google_places.csv')
google_sentiment_path = os.path.join(data_dir, 'google_sentiment_google.csv')

google_places_pdf = pd.read_csv(google_places_path)
google_sentiment_pdf = pd.read_csv(google_sentiment_path)[['name', 'neg', 'neu', 'pos', 'compound']]

google_places_pdf = pd.merge(google_places_pdf, google_sentiment_pdf, on='name', how='inner')
google_places_pdf.columns = ['status', 'address_components', 'formatted_address',
       'formatted_phone_number', 'geometry', 'icon',
       'international_phone_number', 'name', 'opening_hours', 'photos',
       'rating', 'reviews', 'types', 'url', 'vicinity', 'website', 'lng',
       'lat', 'neg_sentiment', 'neu_sentiment', 'pos_sentiment', 'overall_sentiment_score']

google_places_pdf.to_csv(google_places_path, index=False)