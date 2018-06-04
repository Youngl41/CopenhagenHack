#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 10 22:26:15 2018

@author: Young
"""

# Import modules
import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelBinarizer


# =============================================================================
# Data Pre-Processing Functions
# =============================================================================
def normalise(pandas_df):
    mean_col_wise = np.mean(pandas_df)
    standard_dev_col_wise = np.std(np.array(pandas_df),0)
    standardised_df = (pandas_df - mean_col_wise)/standard_dev_col_wise
    return standardised_df

# Convert labels
def binarize_labels(labels):
    lb = LabelBinarizer()
    lb.fit(labels)
    binary_labels = lb.transform(labels)
    binary_names = lb.classes_
    binary_labels_df = pd.DataFrame(binary_labels)
    binary_labels_df.columns = binary_names
    return binary_labels_df

# Chunking function
def chunk_items(items, chunk_size, do_stuff_to_chunk=None, save_dir=None):
    import pickle
    def save_data(feature_matrix, save_file):
        # Define output file
        pickle.dump(feature_matrix, open(save_file, 'wb')) 
        
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
