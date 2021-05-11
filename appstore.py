#module with all functions we need

import pandas as pd
import numpy as np
import os.path
import matplotlib.pyplot as plt

def top_categories_weighted(data,store_type = None):
    frame = data.copy()
    frame['interactions'].dropna(inplace = True)#remove all rows in 'interaction' and 'rating' column with NaN values
    frame['rating'].dropna(inplace = True)
    frame['weighted_rating'] = frame['interactions'] * frame['rating'] # multiply the rating * number of interaction and divide by the total number of interactions

    if store_type is None: #check whether the store type was passed as a variable or not
        pass
    else:
        frame = frame[frame['store'] == store_type] #select only the rows with the store type that was called

    frame = frame[frame['category'].notnull()] #get only the rows with non- NaN values
    categories = set(frame['category'].tolist())  # getting all category types
    category_rating_dic = {} # dict to contain the rating for each category type
    for category in categories:  # filling the dictionary
        cat = frame.loc[frame['category'] == category]  # choosing the single category
        rating = cat['weighted_rating'].sum() / cat['interactions'].sum() # calculating the mean weighted rating for the category
        category_rating_dic[category] = rating  # adding the new key:value to the dictionary
    return (category_rating_dic)

'''def bar_chart(category_rating_dic):
    # making a bar char with the top 5 categories
'''

'''import re

def clean_column (df, column):
    df[column] = df[column].str.replace(r'\D', '')
    df[column].isna = 0.0
    return df[column]
'''
def grafic_rating(data):
    categories = data.keys()
    ratings = data.values()
    y_pos = np.arange(len(categories))

    plt.barh(y_pos, ratings, align='center', alpha=0.5, log=True)
    plt.yticks(y_pos, categories)
    plt.xlabel('rating')
    plt.ylabel('categories')
    plt.title('Statistic correlation between rating and category')
    plt.show()
    return()

def dictionary_top(frame, column):
    list = (frame[column].tolist())  # getting all category types
    dic = {}  # dict to contain the rating for each category type
    for e in list:  # filling the dictionary
        if e not in dic:
            dic[e] = 1
        else:
            dic[e] += 1
    return (dic)
