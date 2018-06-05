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
# Cleaning string
#==============================================================================


def normalize_string(snippet):
    """Function to clean and normalise a text string."""
    import re
    snippet = str(snippet)
    # Replace ' with unicode '
    normalizedText = '\'' + snippet.replace("'", r"''") + '\''
    # Remove all links
    normalizedText = re.sub('http\S+', ' ', normalizedText)
    normalizedText = re.sub('www\S+', ' ', normalizedText)
    # Remove all @ mentions
    normalizedText = re.sub('@\S+', ' ', normalizedText)
    # Remove all apart from symbols below 
    normalizedText = re.sub(r'[^\w.#\u0027\u02BC\-\s]+','', normalizedText)
    normalizedText = re.sub(r'\d+', '', normalizedText)
    # Replace symbols
    normalizedText = normalizedText.replace('.',' ')
    normalizedText = normalizedText.replace('  ',' ')
    normalizedText = normalizedText.replace('\'','')
    # Strip whitespaces
    normalizedText = normalizedText.rstrip()
    normalizedText = normalizedText.lstrip()
    return normalizedText

def create_clean_ls_from_string(words):
    """Function to create a clean list from a string."""
    words = words.replace('\\n',' ')
    words = words.replace('\“',' ')
    words = words.replace('//',' ')
    words = words.replace('-',' ')
    words = words.replace('\n',' ')
    words = words.replace('\xa0',' ')
    words = words.replace('\t', ' ')
    words = words.replace('_', ' ')
    words = words.replace('  ', ' ')
    words = words.replace('#', ' #')
    word_ls = words.split(' ')
    try:
        word_ls = [a for a in word_ls if a != '']
        word_ls = [a for a in word_ls if a != 'rt']
    except ValueError:
        pass
    return word_ls


def cleaner(df_column):
    """Cleaner function that combines normalisation and create clean list."""
    # Create long string from all snippets
    words = str(df_column).lower()
    
    # Create list from word string, apply cleaning and only keep unique values
    word_list = create_clean_ls_from_string(words)

    # Set up keyword list to remove
    keyword_ls = ['.ly','.com','.be', '.de', '.me', '.it', '.tt', '.net', '.bz', 'pic.twitter', 'm.youtube.com', '.gl', '.edu', '.htm']
    
    clean_ls = []
    for word in word_list:
        if not any(keyword in word for keyword in keyword_ls):
            clean_ls.append(normalize_string(str(word)))
    
#    # Remove stop words from clean list of words
#    stop_removed = [word for word in clean_ls if word not in stopwords.words('german')]
#    stop_removed = [word for word in stop_removed if word not in stopwords.words('english')]
#    
    # Join output string
    stop_removed = ' '.join(clean_ls)
    return stop_removed




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
    
    input_file = '/Users/Hackathon/CopenhagenHack/Data/2018-06-05_copenhagen.csv'
    twitter_df = pd.read_csv(input_file)
    
    # Clean text
    twitter_df['clean_text'] = twitter_df['tweet_text'].map(lambda x: cleaner(str(x)))
    
    # Drop data without geospatial coordinates
    twitter_df = twitter_df[(twitter_df['latitude'] != 0) & (twitter_df['latitude'] != np.NaN)]
    twitter_df = twitter_df.reset_index(drop = True)
    
    # Set cores
    ncores = multiprocessing.cpu_count() - 1
    
    # Set sentiment analyser
    sentiment_analyser = vader.SentimentIntensityAnalyzer()
    
    # Run code
    output = Parallel(n_jobs = ncores)(delayed(map_sentiment_vader)(str(tweet), sentiment_analyser) for tweet in twitter_df['clean_text'].tolist())
    
    # Store in dataframe
    output = pd.DataFrame(output)
    output.columns = ['neg', 'neu', 'pos', 'compound']
    output = output.reset_index(drop = True)

    # Concatenate with twitter dataframe
    sentiment_df_twitter = pd.concat([twitter_df, output], axis = 1)
    
    
    sentiment_df_twitter.to_csv('/Users/Hackathon/CopenhagenHack/Data/'+os.path.basename(input_file).split('_')[0] + '_sentiment_twitter.csv')
