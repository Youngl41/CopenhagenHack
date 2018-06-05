#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 09:25:35 2018

@author: mia
"""
# Import nlp modules
from nltk.sentiment import vader
from nltk.corpus import stopwords

# Import pandas
import pandas as pd
import numpy as np
import os

# Import parallelisation modules
import multiprocessing
from joblib import Parallel, delayed



#==============================================================================
# Extract text
#==============================================================================


def avg_sentiment(reviews_dict, sentiment_analyser_class):
    scores = []
    for i in range(len(reviews_dict)):
        scores.append(list(map_sentiment_vader(reviews_dict[i]['text'], sentiment_analyser_class)))
    
    scores = pd.DataFrame(scores)
    
    scores.columns = ['neg', 'neu', 'pos', 'compound']
    avg_neg = scores.mean(axis = 0)['neg']
    avg_neu = scores.mean(axis = 0)['neu']
    avg_pos = scores.mean(axis = 0)['pos']
    avg_compound = scores.mean(axis = 0)['compound']
    
    return avg_neg, avg_neu, avg_pos, avg_compound


#==============================================================================
# Map Job For Sentimental Features
#==============================================================================
def map_sentiment_vader(text,sentiment_analyser_class):
    score = sentiment_analyser_class.polarity_scores(text)
    return score['neg'], score['neu'], score['pos'], score['compound']

# =============================================================================
# Main
# =============================================================================
if __name__ == '__main__':
    
    input_file = '/Users/Hackathon/CopenhagenHack/Data/google_places_details.csv'

    google_df = pd.read_csv(input_file)
    
    # Google places
    google_df = google_df[google_df['status']=='OK']
    google_df = google_df[['status', 'address_components',
                                           'formatted_address', 'formatted_phone_number',
                                           'geometry', 'icon', 'international_phone_number', 'name',
                                           'opening_hours', 'photos', 'rating', 'reviews', 
                                           'types', 'url', 'vicinity', 'website']]
    google_df = google_df[google_df['reviews'].notnull()]
    google_df.loc[:, 'geometry'] = google_df.loc[:, 'geometry'].apply(eval)
    google_df.loc[:,'lng'] = list(map(lambda x: x['location']['lng'], google_df.loc[:,'geometry']))
    google_df.loc[:,'lat'] = list(map(lambda x: x['location']['lat'], google_df.loc[:,'geometry']))
    google_df = google_df.reset_index(drop = True)
    
    
    google_df = google_df.reset_index(drop = True)
    
    

    # Set cores
    ncores = multiprocessing.cpu_count() - 1
    
    # Set sentiment analyser
    sentiment_analyser = vader.SentimentIntensityAnalyzer()
    
    
    
    # Clean text
    google_df['reviews'] = google_df['reviews'].apply(eval)

    
    # Run code
    output = Parallel(n_jobs = ncores)(delayed(avg_sentiment)(review, sentiment_analyser) for review in google_df['reviews'].tolist())
    
    # Store in dataframe
    output = pd.DataFrame(output)
    output.columns = ['neg', 'neu', 'pos', 'compound']
    output = output.reset_index(drop = True)

    # Concatenate with twitter dataframe
    sentiment_df_google = pd.concat([google_df, output], axis = 1)
    
    
    sentiment_df_google.to_csv('/Users/Hackathon/CopenhagenHack/Data/'+os.path.basename(input_file).split('_')[0] + '_sentiment_google.csv')
