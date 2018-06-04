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

def results_nearby_search_wrapper(circle_centres, api_keys, type_list = ['museum', 'amusement_park', 'art_gallery', 'aquarium', 'park']):
    
    results_nearby_search = []
    
    for place_type in type_list:
        
        j = 0
        
        # API key update
        API_KEY = api_keys[j]
        
        # Nearby Search URL
        url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=%0.7f,%0.7f&radius=%d&type=%s&key=%s' % (circle_centres[1],circle_centres[0],radius_google*1000, place_type, API_KEY)
       
        headers = {'Content-Type':'json'}
        
        # Send request to Google Places Nearby Search API
        r = requests.request('GET', url, headers = headers)
        
        # Format response
        parsed = json.loads(r.text)
        
        while parsed['status'] != 'OK':
            
            j = j + 1
            
            # API key update
            API_KEY = api_keys[j]
            
            
            # Place Details URL
            url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=%0.7f,%0.7f&radius=%d&type=%s&key=%s' % (circle_centres[1],circle_centres[0],radius_google*1000, place_type, API_KEY)
           
            headers = {'Content-Type':'json'}
            
            # Send request to Google Places Nearby Search API
            r = requests.request('GET', url, headers = headers)
        
            # Format response
            parsed = json.loads(r.text)
            
        # API key update
        API_KEY = api_keys[j]
        
        # Place Details URL
        url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=%0.7f,%0.7f&radius=%d&type=%s&key=%s' % (circle_centres[1],circle_centres[0],radius_google*1000, place_type, API_KEY)
        headers = {'Content-Type':'json'}
        
        # Send request to Google Places Nearby Search API
        r = requests.request('GET', url, headers = headers)
        
        # Format response
        parsed = json.loads(r.text)
        
        for item in parsed['results']:
            results_nearby_search.append(item['place_id'])
            
    #    print('%d operators appended to list.' % len(parsed['results']))
    
    return results_nearby_search



#==============================================================================
# Place Id Search
#==============================================================================


def results_details_wrapper(results_nearby_search_duplicates_removed, api_keys):
    
    
    j = 0
    
    # API key update
    API_KEY = api_keys[j]
    
    # Place Details URL
    url = 'https://maps.googleapis.com/maps/api/place/details/json?placeid=%s&key=%s' % (results_nearby_search_duplicates_removed, API_KEY)
   
    headers = {'Content-Type':'json'}
    
    # Send request to Google Places Nearby Search API
    r = requests.request('GET', url, headers = headers)

    # Format response
    parsed = json.loads(r.text)
    
    print(parsed['status'])
    
    while parsed['status'] != 'OK':
        
        print(j)
        
        j = j + 1
        
        # API key update
        API_KEY = api_keys[j]
        
        
        # Place Details URL
        url = 'https://maps.googleapis.com/maps/api/place/details/json?placeid=%s&key=%s' % (results_nearby_search_duplicates_removed, API_KEY)
       
        headers = {'Content-Type':'json'}
        
        # Send request to Google Places Nearby Search API
        r = requests.request('GET', url, headers = headers)
    
        # Format response
        parsed = json.loads(r.text)
        
    
    # API key update
    API_KEY = api_keys[j]
    
    # Place Details URL
    url = 'https://maps.googleapis.com/maps/api/place/details/json?placeid=%s&key=%s' % (results_nearby_search_duplicates_removed, API_KEY)
   
    headers = {'Content-Type':'json'}
    
    # Send request to Google Places Nearby Search API
    r = requests.request('GET', url, headers = headers)

    # Format response
    parsed = json.loads(r.text)
    
    file_path = '/Users/Hackathon/CopenhagenHack/Data/GoogleMaps/'
    file_name = str(results_nearby_search_duplicates_removed)
        
    with open(file_path+file_name+'.json', 'w', encoding='utf-8') as f:
        json.dump(parsed, f)
       
    print(parsed)
    
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
    
    radius_google = 0.1 #km
    
    api_keys = ['AIzaSyBGm5NvDNaTNvzYRxBL8YHxO0umVAZvlY4',
                'AIzaSyCrvD8raAfNRZSpSVt71rpkAWs0UAgu_8A',
                'AIzaSyDCvsdzXyzpQfOwdwOlJYtNIL0_41-mdaY',
                'AIzaSyDhcNayTq_NGNXiOrquXkD4UwIJThVkiyo',
                'AIzaSyBz-5nyFTGzAGhVt2R9gKXUHH2qrViODYg',
                'AIzaSyC8JHKanGG8I8JgPPsnskFdWpptPwMQkjs',
                'AIzaSyBjoQmIEkq0vn1eNF9haeIO955Wibrq3Ik',
                'AIzaSyC23HFzd2ButKX89kTgESLRipW1hxSSF0g',
                'AIzaSyDWhE5eZkkORknSxyWtmu7J28wHwMZvAFk',
                'AIzaSyAzwD3xEzGX3UOnDkmp2Aac7NZHe9Fyu9Q',
                'AIzaSyCDuEUyGiUbDST_tBIaCkuCKELUDlfEgM8',
                'AIzaSyBXo_1YlL54HLbKqgyb_ye2GpfT-aBsLpk',
                'AIzaSyACGBpLLgq--R33tqHt1tuv2hcLGphmoTE',
                'AIzaSyDjnhMUbD-Qm21Lbd7iku-K4U8dyBTN3RY',
                'AIzaSyD3NQAHv__EQ5kKKKZi3EJZSV6MQyxbqiQ',
                'AIzaSyDW9GMpr2I7yaPUH49DZC2XkrnkyBjN81Y',
                'AIzaSyCLRILm0H5U0MhV3VUnIyWSS76tbfnsonQ',
                'AIzaSyBJo7f8AYzHAMqLwBEsc276KmKDFCAnxxs',
                'AIzaSyD6vf9Es6zi-S18AgPEc9suxA06BsaSUIE',
                'AIzaSyCzabLa2pAfy4ook_-eeDXSOgNIyc7vV6s',
                'AIzaSyDdJLHZTh5WB7gppqfJqSyUam45FashI_g',
                'AIzaSyCg6qn64xuUC9F-RKFVQqPm97gDV3YPSXQ',
                'AIzaSyAkQe121kP2fvguWyXY_QfTwQasxif9bgU',
                'AIzaSyBu5zFT557oiYbdlBWlHW4H0eqyI7bI2iw']
    
    #==============================================================================
    # Set search radius for Google
    #==============================================================================
    
    r = radius_google
    
    circle_centres = []
    
    step_total = math.ceil((5)/r) # km, London = 16-24km diameter
    
    
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
    
    #circles.to_csv('/Users/Mia/Desktop/circles.csv')
    
    """
    results_nearby_search = pd.read_csv('/Users/mia/Desktop/nearby_still_missing_22.csv')
    results_nearby_search = results_nearby_search['0'].tolist()
    results_nearby_search_duplicates_removed  = list(set(results_nearby_search))
    """
    
#    # Request place IDs
    results_nearby_search = Parallel(n_jobs = ncores)(delayed(results_nearby_search_wrapper)(circles[i], api_keys, type_list = ['museum', 'amusement_park', 'art_gallery', 'aquarium', 'park']) for i in range(len(circles)))
    
    #Remove duplicates
    results_nearby_search_duplicates_removed = list(set(results_nearby_search))
    
    # Request place details
    results_place_details = Parallel(n_jobs = ncores)(
            delayed(results_details_wrapper)(results_nearby_search_duplicates_removed[i], api_keys) for i in range(len(results_nearby_search_duplicates_removed)))
    
    
    #==============================================================================
    # Store output in CSV
    #==============================================================================
    
    google_operator_df = pd.DataFrame(results_place_details)
    
    google_operator_df = pd.concat([google_operator_df.drop(['result'], axis=1), google_operator_df['result'].apply(pd.Series)], axis=1)


    google_operator_df.to_csv('/Users/mia/Desktop/google_places_details.csv')

















