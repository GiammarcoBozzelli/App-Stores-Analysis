#module with all functions we need

import pandas as pd
import numpy as np
import os.path
import matplotlib.pyplot as plt

def top_categories_weighted(data,store_type = None): #Giammarco
    frame = data.copy()
    frame['interactions'].dropna(inplace = True)#remove all rows in 'interaction' and 'rating' column with NaN values
    frame['rating'].dropna(inplace = True)
    frame['weighted_rating'] = frame['interactions'] * frame['rating'] # multiply the rating * number of interaction

    if store_type is None: #check whether the store type was passed as a variable or not
        pass
    else:
        frame = frame[frame['store'] == store_type] #select only the rows with the store type that was called

    frame = frame[frame['category'].notnull()] #get only the rows with non- NaN values
    categories = set(frame['category'].tolist())  # getting all category types without repetitions
    category_rating_dic = {} # dict to contain the rating for each category type

    for category in categories:  # filling the dictionary
        cat = frame.loc[frame['category'] == category]  # creating a frame by choosing the single category
        rating = cat['weighted_rating'].sum() / cat['interactions'].sum() #calculating the weighted rating for the category
        category_rating_dic[category] = rating  # adding the new key:value to the dictionary

    print ('The highest rated category is: ',max(category_rating_dic, key=lambda k: category_rating_dic[k]))
    return (category_rating_dic)

def pie_chart(data,store_type = None): #Giammarco
    frame = data.copy()
    if store_type is None: #check whether the store type was passed as a variable or not
        pass
    else:
        frame = frame[frame['store'] == store_type] #select only the rows with the store type that was called

    frame = frame[frame['category'].notnull()] #get only the rows with non- NaN values
    categories = frame['category'].tolist()# getting a list with categories
    category_dic = {} # dict to contain the rating for each category type
    for category in categories:  # filling the dictionary
        if category not in category_dic:
            category_dic[category] = 1
        else:
            category_dic[category] += 1# adding the new key:value to the dictionary

    plt.figure(figsize = (8,8))
    plt.pie(list(category_dic.values()), labels=list(category_dic.keys()),rotatelabels = 30 ,
            autopct='%1.1f%%', explode = (0.1,0,0,0,0,0,0,0,0,0,0,0,0), textprops={'fontsize': 12})

    return (category_dic)

def grafic_rating(dict): #Marco
    categories = dict.keys()
    ratings = dict.values()
    y_pos = np.arange(len(categories))

    plt.figure(figsize = (8,6))
    plt.barh(y_pos, ratings, align='center', alpha=0.5, log=True, ) #add log = True to make the graph clearer
    plt.yticks(y_pos, categories)
    plt.xlabel('Rating', fontsize = 12)
    plt.ylabel('Categories', fontsize = 12)
    plt.title('Statistic correlation between rating and category', fontsize = 15)
    plt.show()
    return

def dictionary_top(frame, column): #Marco
    list = (frame[column].tolist())  # getting all category types
    dic = {}  # dict to contain the number of apps for each category type
    for e in list:  # filling the dictionary
        if e not in dic:
            dic[e] = 1
        else:
            dic[e] += 1
    return (dic)

def top_50_catplot(dic):
    categories = dic.keys()
    ratings = dic.values()
    y_pos = np.arange(len(categories))
    plt.figure(figsize=(9, 6))
    plt.barh(y_pos, ratings, align='center', alpha=0.5)
    plt.yticks(y_pos, categories)
    plt.xlabel('Number of Apps', fontsize=12)
    plt.ylabel('Categories', fontsize=12)
    plt.title('Which is the most common category in the top 50 apps?', fontsize=15)
    plt.show()
    return

def top_50_sizeplot(data):
    data.plot.bar(x="name", y="size (MB)", figsize = (15,8))
    plt.title("Size (MB) in the top 50", fontsize = 18)
    plt.xticks([]) # Disable xticks.
    plt.xlabel('Applications', fontsize = 15)
    plt.ylabel('Size in MB', fontsize = 15)
    plt.show()
    return

def top_50_priceplot(dic):
    price = dic.keys()
    freq = dic.values()
    y_pos = np.arange(len(price))
    plt.figure(figsize = (9,6))
    plt.barh(y_pos, freq, align='center', alpha=0.5)
    plt.yticks(y_pos, price)
    plt.xlabel('Frequency', fontsize = 12)
    plt.ylabel('Prices', fontsize = 12)
    plt.title('which is the most common category in the top 50 apps?', fontsize = 15)
    plt.show()
    return
