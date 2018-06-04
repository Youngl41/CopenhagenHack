#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 00:54:55 2018

@author: Young
"""


# =============================================================================
# Geospatial Utility Functions
# =============================================================================
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
    
# Map job for loading data
def map_pipe_props_to_pandas(pipe_shp_chunk):
    pipe_props = [pol['properties'] for pol in pipe_shp_chunk]
    pipe_props = pd.DataFrame(pipe_props)
    pipe_props = pipe_props[[u'TAG', u'ID_DMA1']]
    pipe_props.columns = ['tag', 'dma']
    return pipe_props