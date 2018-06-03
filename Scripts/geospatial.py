#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  3 23:16:36 2018

@author: Young
"""

# Import general modules
import os
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
from shapely.geometry import Polygon, MultiPolygon, shape


# =============================================================================
# Utility Functions
# =============================================================================
# Save data
def save_data(data, path):
    cPickle.dump(data, open(path, 'wb'))

# Load data
def load_data(file_path):
    return cPickle.load(open(file_path, 'rb'))
    
# Convert geometries to shapes
def convert2shape(geom):
    if geom['type']=='Polygon':
        return Polygon(geom['coordinates'][0])
    elif geom['type']=='MultiPolygon':
        poly_list = [Polygon(coords[0]) for coords in geom['coordinates']]
        return MultiPolygon(poly_list)
    elif geom['type']=='LineString':
        return shape(geom)
    elif geom['type']=='MultiLineString':
        return shape(geom)
    else:
        assert False, 'geom must be of type Polygon, MultiPolygon, LineString or MultiLineString'
        
# Plot shapes
def plot_shapes(dict_of_multi_polygons, figsize):
    # Define plot
    fig = plt.figure(figsize = figsize)
    ax = fig.add_subplot(111)

    # Settings
    number_of_polygon_groups = len(dict_of_multi_polygons.keys())
    transparency = max(0.3, 0.3+ 0.7/number_of_polygon_groups)
    title_string = 'Plot showing polygons of:\n' + ', '.join(dict_of_multi_polygons.keys())

    # Find the boundaries of plot
    minx, miny, maxx, maxy = (np.NaN,np.NaN,np.NaN,np.NaN)
    for key in dict_of_multi_polygons.keys():
        multi_polygons = dict_of_multi_polygons[key]
        
        for polygon in multi_polygons:
            minx_temp, miny_temp, maxx_temp, maxy_temp = polygon.bounds
            minx, miny, maxx, maxy = (np.nanmin([minx, minx_temp]), np.nanmin([miny, miny_temp]), np.nanmax([maxx, maxx_temp]), np.nanmax([maxy, maxy_temp]))

    # Set boundaries
    w, h = maxx - minx, maxy - miny
    ax.set_xlim(minx - 0.2 * w, maxx + 0.2 * w)
    ax.set_ylim(miny - 0.2 * h, maxy + 0.2 * h)
    ax.set_aspect(1)

    # Plot polygons
    patches = []
    list_of_list_of_lines = []
    for key in dict_of_multi_polygons.keys():
        multi_polygons = dict_of_multi_polygons[key]
        if (multi_polygons[0].type == 'LineString') or (multi_polygons[0].type == 'MultiLineString'):
            list_of_list_of_lines.append(multi_polygons)
            continue
        else:
            mp = MultiPolygon(multi_polygons)

        # Colourmap
        cm = plt.get_cmap('RdBu')
        num_colours = len(mp)

        for idx, p in enumerate(mp):
            colour = cm(1. * idx / num_colours)
            patches.append(PolygonPatch(p, fc=colour, ec='#555555', alpha=transparency, zorder=1))

    # Plot lines
    for list_of_lines in list_of_list_of_lines:
        for line in list_of_lines:
            x,y = line.xy
            ax.plot(x, y, color='green', linewidth=1, zorder=1, solid_capstyle='round')
    
    # Complete plot
    ax.add_collection(PatchCollection(patches, match_original=True))
    ax.set_xticks([])
    ax.set_yticks([])
    plt.title(title_string)
    plt.show()
    
# Chunking function
def chunk_items(items, chunk_size, do_stuff_to_chunk=None, save_dir=None):
    chunks = []
    number_of_chunks = int(np.ceil(len(items)/float(chunk_size)))
    
    # Chunk it!
    for idx in range(number_of_chunks):
        st = datetime.now()
        chunk_l = idx * chunk_size
        chunk_u = chunk_l + chunk_size
        
        if do_stuff_to_chunk:
            chunk = do_stuff_to_chunk(items[chunk_l : chunk_u])
        else:
            chunk = items[chunk_l : chunk_u]
            
        if save_dir:
            file_name = os.path.join(save_dir, 'chunk_'+str(idx)+'.pkl')
            save_data(chunk, file_name)
            
        chunks.append(chunk)
        
        # Verbose
        et = datetime.now()
        print ('Chunk\t', idx + 1, '/', number_of_chunks, '\tcomplete in:', et-st)
    
    return chunks

# Map job for loading data
def map_pipe_props_to_pandas(pipe_shp_chunk):
    pipe_props = [pol['properties'] for pol in pipe_shp_chunk]
    pipe_props = pd.DataFrame(pipe_props)
    pipe_props = pipe_props[[u'TAG', u'ID_DMA1']]
    pipe_props.columns = ['tag', 'dma']
    return pipe_props


# =============================================================================
# Load Data
# =============================================================================
# Paths
main_dir = '/Users/Young/Documents/Capgemini/Learning/AI/Copenhagen Hackathon/Data/Copenhagen-shp/shape/'
roads_shp_path = os.path.join(main_dir, 'roads.shp')
buildings_shp_path = os.path.join(main_dir, 'buildings.shp')
natural_shp_path = os.path.join(main_dir, 'natural.shp')
landuse_shp_path = os.path.join(main_dir, 'landuse.shp')
railways_shp_path = os.path.join(main_dir, 'railways.shp')

# Load data
roads_shp = fiona.open(roads_shp_path)
buildings_shp = fiona.open(buildings_shp_path)
natural_shp = fiona.open(natural_shp_path)
landuse_shp = fiona.open(landuse_shp_path)
railways_shp = fiona.open(railways_shp_path)

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
plot_shapes(dict_of_multi_polygons=dict_of_multi_polygons, figsize=(20,15))
