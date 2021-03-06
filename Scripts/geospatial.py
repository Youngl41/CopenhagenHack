#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  3 23:16:36 2018

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
roads_shp_path = os.path.join(main_dir, 'roads.shp')
buildings_shp_path = os.path.join(main_dir, 'buildings.shp')
natural_shp_path = os.path.join(main_dir, 'natural.shp')
landuse_shp_path = os.path.join(main_dir, 'landuse.shp')
railways_shp_path = os.path.join(main_dir, 'railways.shp')
loc_path = os.path.join(data_dir, 'clean_loc.csv')
google_places_path = os.path.join(data_dir, 'google_places_details.csv')

# Load data
roads_shp = fiona.open(roads_shp_path)
buildings_shp = fiona.open(buildings_shp_path)
natural_shp = fiona.open(natural_shp_path)
landuse_shp = fiona.open(landuse_shp_path)
railways_shp = fiona.open(railways_shp_path)
loc_pdf = pd.read_csv(loc_path)
google_places_pdf = pd.read_csv(google_places_path)

# Properties
roads_props = [pol['properties'] for pol in roads_shp]
roads_props = pd.DataFrame(roads_props)
roads_props.head()
print(len(roads_props))

# Copenhagen shape
geom = {'coordinates': [[(12.4529, 55.6150),
                        (12.6507, 55.6150),
                        (12.6507, 55.7326),
                        (12.4529, 55.7326),
                        (12.4529, 55.6150)]],
                      'type': 'Polygon'}
copenhagen_shp = convert2shape(geom)

# Polygons
roads_polys = []
for idx in range(len(roads_shp[:1000])):
    poly = convert2shape(roads_shp[idx]['geometry'])
    if poly.intersects(copenhagen_shp):
        roads_polys.append(poly)
print('Num roads\t:', len(roads_polys))

buildings_polys = []
for idx in range(len(buildings_shp[:1000])):
    poly = convert2shape(buildings_shp[idx]['geometry'])
    if poly.intersects(copenhagen_shp):
        buildings_polys.append(poly)
print('Num buildings\t:', len(buildings_polys))

natural_polys = []
for idx in range(len(natural_shp)):
    poly = convert2shape(natural_shp[idx]['geometry'])
    if poly.intersects(copenhagen_shp):
        natural_polys.append(poly)
print('Num natural\t:', len(natural_polys))

landuse_polys = []
for idx in range(len(landuse_shp)):
    poly = convert2shape(landuse_shp[idx]['geometry'])
    if poly.intersects(copenhagen_shp):
        landuse_polys.append(poly)
print('Num landuse\t:', len(landuse_polys))
    
railways_polys = []
for idx in range(len(railways_shp)):
    poly = convert2shape(railways_shp[idx]['geometry'])
    if poly.intersects(copenhagen_shp):
        railways_polys.append(poly)
print('Num railway\t:', len(railways_polys))

loc_polys = list(map(lambda x: Point(x[0], x[1]), np.array(loc_pdf[['longitude', 'latitude']])))

# Plot intersecting tiles with copenhagen
dict_of_multi_polygons = {'Roads': roads_polys,
                          'Buildings': buildings_polys,
                          'Natural': natural_polys,
                          'Landuse': landuse_polys,
                          'Railways': railways_polys,
                          'Locations': loc_polys[:1000],
                          }
plot_shapes(dict_of_multi_polygons=dict_of_multi_polygons, figsize=(11,15))


google_places_pdf = google_places_pdf[google_places_pdf['status']=='OK']
google_places_pdf = google_places_pdf[['status', 'address_components',
                                       'formatted_address', 'formatted_phone_number',
                                       'geometry', 'icon', 'international_phone_number', 'name',
                                       'opening_hours', 'photos', 'rating', 'reviews', 
                                       'types', 'url', 'vicinity', 'website']]
google_places_pdf = google_places_pdf[google_places_pdf['reviews'].notnull()]
google_places_pdf.loc[:, 'geometry'] = google_places_pdf.loc[:, 'geometry'].apply(eval)
google_places_pdf.loc[:,'lng'] = list(map(lambda x: x['location']['lng'], google_places_pdf.loc[:,'geometry']))
google_places_pdf.loc[:,'lat'] = list(map(lambda x: x['location']['lat'], google_places_pdf.loc[:,'geometry']))
google_places_pdf = google_places_pdf.reset_index(drop = True)

# Historical timestamps
hist_time_pdf = loc_pdf[['date', 'hour']].drop_duplicates().sort_values(['date', 'hour'])
hist_time_pdf = hist_time_pdf.iloc[1:]
hist_time_pdf = hist_time_pdf[(hist_time_pdf['date'] >= datetime.date(2018, 5, 1)) & 
              (hist_time_pdf['date'] < datetime.date(2018, 6, 1))].reset_index(drop=True)

# Get crowdiness level
google_places_pdf.loc[:, 'tmp'] = 1
hist_time_pdf.loc[:, 'tmp'] = 1

places_by_hour_pdf = pd.merge(google_places_pdf, hist_time_pdf, on='tmp')

places_by_hour_people_pdf = pd.merge(places_by_hour_pdf, loc_pdf[(loc_pdf['date'] >= datetime.date(2018, 5, 1)) & 
              (loc_pdf['date'] < datetime.date(2018, 6, 1))][['unique_id', 'date', 'hour', 'longitude', 'latitude']], on=['date','hour'], how='inner')

# Haversine dist
places_by_hour_people_pdf.loc[:, 'hav_dist'] = list(map(lambda x: hav_dist(x[0], x[1], x[2], x[3]), np.array(places_by_hour_people_pdf[['longitude', 'latitude', 'lng', 'lat']])))
places_by_hour_people_pdf = places_by_hour_people_pdf[places_by_hour_people_pdf['hav_dist'] < 100]
places_by_hour_people_pdf['name', 'unique_id', 'date', 'hour']
dict_of_multi_polygons = {'Locations': loc_polys[:1],
                          }
plot_shapes(dict_of_multi_polygons=dict_of_multi_polygons, figsize=(10,15))


loc_pdf
loc_pdf[(loc_pdf['date'] == datetime.date(2018, 1, 3)) & (loc_pdf['hour'] == 16)]

for idx, row in loc_pdf[['date', 'hour']].drop_duplicates().sort_values(['date', 'hour']).iterrows():
    loc_pdf[(loc_pdf['date'] == row['date']) & 
            (loc_pdf['hour'] == row['hour'])]
    
pd.to_datetime(loc_pdf.iloc[0].time_tuple).date()

# Plot a person's visits
person_idx = 12
person_polys = [loc_polys[i] for i in loc_pdf[loc_pdf['unique_id'] == loc_pdf['unique_id'].unique()[person_idx]].index.values]
dict_of_multi_polygons = {'Roads': roads_polys,
                          'Buildings': buildings_polys,
                          'Natural': natural_polys,
                          'Landuse': landuse_polys,
                          'Railways': railways_polys,
                          'Locations': person_polys,
                          }
plot_shapes(dict_of_multi_polygons=dict_of_multi_polygons, figsize=(11,15))