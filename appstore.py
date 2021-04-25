#module with all functions we need

import pandas as pd
import numpy as np
import os.path
import matplotlib.pyplot as plt

def top_categories (file): #returns the
    try: # open as DataFrame the file depending from the extension
        frame = pd.read_csv(os.path.join(os.getcwd(), file))
    except:
        frame = pd.read_json(os.path.join(os.getcwd(), file))


    file_name = frame.loc[:, ['name', 'category', 'rating', 'installs']] #selecting the columns we will need
    file_name.dropna(axis=0, how='any', inplace=True)  # deleting all rows with at least one NaN

    # Replace each ',' in the 'installs' column with '' in order to convert it in float64
    file_name['installs'] = file_name['installs'].astype(str)
    file_name['installs'] = file_name['installs'].str.strip('+,. ')
    file_name['installs'] = np.float64(file_name['installs'].str.replace(',', ''))

    # add a column ['weighted_rating'] that will be useful in dentifying a more precise mean rating per each category
    file_name.loc[:, 'weighted_rating'] = file_name['rating'] * file_name['installs']

    # %%
    # Calculating the actual rating for each category
    categories = set(file_name['category'].tolist())  # getting all category types
    category_rating_dic = {}  # dict to contain the rating for each category type
    for category in categories:  # filling the dictionary
        cat = file_name.loc[file_name['category'] == category]  # choosing the single category
        rating = cat['weighted_rating'].sum() / cat['installs'].sum()  # calculating the rating wrt n. of installs
        category_rating_dic[category] = rating  # adding the new key:value to the dictionary
    print( f'The top 5 categories for {file} are: ', sorted(category_rating_dic.items(), key=lambda xy: xy[1], reverse=True)[:5])
    return(category_rating_dic)

def bar_chart (category_rating_dic):
    # making a bar char with the top 5 categories
    d = sorted(category_rating_dic.items(), key=lambda xy: xy[1], reverse=True)[:5]
    plt.bar([x[0] for x in d], [x[1] for x in d], log=True)# use log = True to make the graph more evident
    plt.show()