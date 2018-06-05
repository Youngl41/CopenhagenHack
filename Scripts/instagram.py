#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 12:18:42 2018

@author: mia
"""


import requests
import json
import pandas as pd
import math

from joblib import Parallel, delayed
import multiprocessing



consumer_id = 'fe9a63dbca234afeb57a8edc84b37ee7'
consumer_secret = '7ce74794524f4a4eae59b4f0666326f8'

"""
# STEP 1

https://api.instagram.com/oauth/authorize/?client_id=fe9a63dbca234afeb57a8edc84b37ee7&redirect_uri=https://www.sites.google.com/site/interestcluster/&response_type=code&scope=public_content

"""


"""

# STEP 2

https://www.sites.google.com/site/interestcluster/?code=489392218c22462495a9c595f9147954

"""

"""

# STEP 3

curl -F 'client_id=fe9a63dbca234afeb57a8edc84b37ee7' -F 'client_secret=7ce74794524f4a4eae59b4f0666326f8' -F 'grant_type=authorization_code' -F 'redirect_uri=https://www.sites.google.com/site/interestcluster/' -F 'code=489392218c22462495a9c595f9147954' https://api.instagram.com/oauth/access_token
"""

493031619.1677ed0.635dc6810fe5484395556b2a9d72cbe3


insta_token = '493031619.fe9a63d.d933d3dedb8b4ffa8240cb73c703ef74'
lat = 12.5683372
long = 55.6760968
url = 'https://api.instagram.com/v1/media/search?lat=12.5683372&lng=55.6760968&access_token=493031619.fe9a63d.d933d3dedb8b4ffa8240cb73c703ef74'


#% (lat, long, insta_token)
   
# Send request to Google Places Nearby Search API
r = requests.request('GET', url, headers = headers)

# Format response
parsed = json.loads(r.text)
    
    
    

{"access_token": "493031619.fe9a63d.d933d3dedb8b4ffa8240cb73c703ef74", "user": {"id": "493031619", "username": "mia.carina", "profile_picture": "https://scontent.cdninstagram.com/vp/76bac8b682fcc05dfcdaf3567f1e7658/5BA84B8F/t51.2885-19/11925829_1423133861036735_1253640080_a.jpg", "full_name": "Mia Carina", "bio": "", "website": "", "is_business": false}}
    
    
    
    
    
    