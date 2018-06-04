#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  3 23:16:36 2018

@author: Young
"""

# Import general modules
import os
import sys
import numpy as np
import pandas as pd
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

# Load data
roads_shp = fiona.open(roads_shp_path)
buildings_shp = fiona.open(buildings_shp_path)
natural_shp = fiona.open(natural_shp_path)
landuse_shp = fiona.open(landuse_shp_path)
railways_shp = fiona.open(railways_shp_path)
loc_pdf = pd.read_csv(loc_path)

# DMA properties
roads_props = [pol['properties'] for pol in roads_shp]
roads_props = pd.DataFrame(roads_props)
roads_props.head()
print(len(roads_props))

# Polygons
roads_polys = []
for idx in range(len(roads_shp[:1000])):
    poly = convert2shape(roads_shp[idx]['geometry'])
    roads_polys.append(poly)

buildings_polys = []
for idx in range(len(buildings_shp[:1000])):
    poly = convert2shape(buildings_shp[idx]['geometry'])
    buildings_polys.append(poly)
    
natural_polys = []
for idx in range(len(natural_shp[:1000])):
    poly = convert2shape(natural_shp[idx]['geometry'])
    natural_polys.append(poly)
    
landuse_polys = []
for idx in range(len(landuse_shp[:1000])):
    poly = convert2shape(landuse_shp[idx]['geometry'])
    landuse_polys.append(poly)
    
railways_polys = []
for idx in range(len(railways_shp[:1000])):
    poly = convert2shape(railways_shp[idx]['geometry'])
    railways_polys.append(poly)

# Plot intersecting tiles with dma
dict_of_multi_polygons = {'Roads': roads_polys,
                          'Buildings': buildings_polys,
                          'Natural': natural_polys,
                          'Landuse': landuse_polys,
                          'Railways': railways_polys,
                          }
plot_shapes(dict_of_multi_polygons=dict_of_multi_polygons, figsize=(10,7))

loc_pdf.loc[:, 'point'] = list(map(lambda x: Point(x[0], x[1]), np.array(loc_pdf[['longitude', 'latitude']])))
loc_pdf

list(map(lambda x: Point(x[0], x[1]), np.array(loc_pdf[['longitude', 'latitude']].iloc[:2000])))

loc_pdf['longitude'].to
list(map(lambda x: float(x), loc_pdf['longitude']))
loc_pdf['latitude']

