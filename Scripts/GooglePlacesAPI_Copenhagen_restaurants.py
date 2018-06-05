#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 13:19:19 2017

@author: mia

"""


#==============================================================================
# Import libraries
#==============================================================================


import requests
import json
import pandas as pd
import math

from joblib import Parallel, delayed
import multiprocessing



#==============================================================================
# Nearby Search for Google
#==============================================================================

def results_nearby_search_wrapper(circle_centres, api_keys, type_list = ['restaurant', 'cafe']):
    
    results_nearby_search = []
    
    for place_type in type_list:
        
        # API key update
        API_KEY = api_keys[0]
        
        # Nearby Search URL
        url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=%0.7f,%0.7f&radius=%d&type=%s&key=%s' % (circle_centres[1],circle_centres[0],radius_google*1000, place_type, API_KEY)
       
        headers = {'Content-Type':'json'}
        
        # Send request to Google Places Nearby Search API
        r = requests.request('GET', url, headers = headers)
        
        # Format response
        parsed = json.loads(r.text)
        
        
        for item in parsed['results']:
            results_nearby_search.append(item['place_id'])
#            print(item['place_id'])
            
#        print('%d operators appended to list.' % len(parsed['results']))
    
    return results_nearby_search



#==============================================================================
# Place Id Search
#==============================================================================


def results_details_wrapper(results_nearby_search_duplicates_removed, api_keys):
    
    
    # API key update
    API_KEY = api_keys[0]
    
    # Place Details URL
    url = 'https://maps.googleapis.com/maps/api/place/details/json?placeid=%s&key=%s' % (results_nearby_search_duplicates_removed, API_KEY)
   
    headers = {'Content-Type':'json'}
    
    # Send request to Google Places Nearby Search API
    r = requests.request('GET', url, headers = headers)

    # Format response
    parsed = json.loads(r.text)
    
#    print(parsed['status'])
    
   
    file_path = '/Users/Hackathon/CopenhagenHack/Data/GoogleMaps/'
    file_name = str(results_nearby_search_duplicates_removed)
        
    with open(file_path+file_name+'.json', 'w', encoding='utf-8') as f:
        json.dump(parsed, f)
       
#    print(parsed)
    
    return parsed



# m = results_details_wrapper(results_nearby_search_duplicates_removed[1], api_keys)



if __name__ == '__main__':
    
    # Set number of cores and local directory
    ncores         = multiprocessing.cpu_count() - 7
    
    
    #==============================================================================
    # Initiate latitude and longitude for London
    #==============================================================================

    lat = 12.5683372
    long = 55.6760968
    
    radius_google = 0.5 #km
    
    api_keys = ['AIzaSyCRrRx8NsObpfFmwmZJNzMn7tOj5AiIHj4']
    
    #==============================================================================
    # Set search radius for Google
    #==============================================================================
    
    r = radius_google
    
    circle_centres = []
    
    step_total = math.ceil((10)/r) # km, London = 16-24km diameter
    
    
    lat_conversion = 360/(2*math.pi * 6372 * math.cos(long/180*math.pi))
    long_conversion = 360/(2*math.pi * 6356)
    
    
    for m in range(int(-step_total/2),int(step_total/2)):
        for n in range(int(-step_total/2),int(step_total/2)):
            lat_new = lat + math.sqrt(2) * r * m * lat_conversion
            long_new = long + math.sqrt(2) * r * n * long_conversion
            coordinates_new = [lat_new,long_new]
            circle_centres.append(coordinates_new)
    
#    # Check for duplicates
#    len(set(tuple(i) for i in circle_centres))

    # Put circle centre coordinates into dataframe
    circles = pd.DataFrame(circle_centres)
    circles.to_csv('/Users/Hackathon/CopenhagenHack/Data/circles.csv')
    

    
#    # Request place IDs
    results_nearby_search = Parallel(n_jobs = ncores)(delayed(results_nearby_search_wrapper)(circles.iloc[i], api_keys, type_list = ['restaurant', 'cafe']) for i in range(len(circles)))
    
    results_nearby_search_flat = [item for sublist in results_nearby_search for item in sublist]
    
    #Remove duplicates
    results_nearby_search_duplicates_removed = list(set(results_nearby_search_flat))
    
    # Request place details
    results_place_details = Parallel(n_jobs = ncores)(
            delayed(results_details_wrapper)(results_nearby_search_duplicates_removed[i], api_keys) for i in range(len(results_nearby_search_duplicates_removed)))
    
    
    #==============================================================================
    # Store output in CSV
    #==============================================================================
    
    google_operator_df = pd.DataFrame(results_place_details)
    
    google_operator_df = pd.concat([google_operator_df.drop(['result'], axis=1), google_operator_df['result'].apply(pd.Series)], axis=1)


    google_operator_df.to_csv('/Users/Hackathon/CopenhagenHack/Data/google_places_details.csv')

















