#module with all functions we need

import pandas as pd
import numpy as np
import os.path
import matplotlib.pyplot as plt

def top_categories_weighted(data,store_type = None): #create a dictionaries with category : rating 
    frame = data.copy()
    frame['weighted_rating'] = frame['interactions'] * frame['rating'] # multiply the ratign * number of interaction and divide by the total number of interactions

    if store_type is None: #check whether the store type was passed as a variable or not
        pass
    else:
        frame = frame[frame['store'] == store_type] #select only the rows with the store type that was called

    frame = frame[frame['category'].notnull()]
    categories = set(frame['category'].tolist())  # getting all category types
    category_rating_dic = {} # dict to contain the rating for each category type
    for category in categories:  # filling the dictionary
        cat = frame.loc[frame['category'] == category]  # choosing the single category
        rating = cat['weighted_rating'].sum() / cat['interactions'].sum() # calculating the mean weighted rating for the category
        category_rating_dic[category] = rating  # adding the new key:value to the dictionary
    return (category_rating_dic)
