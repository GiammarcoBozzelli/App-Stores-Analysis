#%%

import csv
import json
import numpy as np
import pandas as pd
import os.path
import appstore as app

#%%

data_folder = os.getcwd()
file_dir_names = os.listdir(data_folder)
print(data_folder,'\n', file_dir_names)

#%%

#PLAYSTORE

#Importare il dataframe
playstore = pd.read_csv(os.path.join(data_folder,'playstore.csv'))

#%%

#pulire le colonne
playstore = playstore.loc[:,["app_name","genre","rating","reviews","cost_label","size","installs","offered_by"]]

playstore.columns = ["name","category","rating","reviews","price","size","installs","offered_by"]
playstore

#%%

#pulire la colonna del prezzo
import string
playstore['price'] = playstore['price'].astype(str)

bad = [",","₫"," Buy"]
for s in bad:
    playstore["price"] = playstore["price"].str.replace(s,"")

playstore['price'] = playstore['price'].str.replace('Install', '0')
playstore['price'] = playstore['price'].str.split(' ').str[-1]

#convertire la colonna del prezzo in numero decimale e convertire in USD
playstore['price'] = np.float32(playstore['price'])*0.000043


#%%

#aggiungere una nuova colonna che specifica lo store

playstore["store"] = "playstore"
playstore


#%%

#WINDOWS
#Importare il dataframe

windows_store = pd.read_csv(os.path.join(data_folder,'msft.csv'))

#%%

#pulire le colonne
windows_store = windows_store.loc[:,["Name","Rating","No of people Rated","Category","Price"]]
windows_store.columns = ["name","rating","No of people Rated","category","price"]

#%%

#pulire la colonna del prezzo
windows_store['price'] = windows_store['price'].str.replace('Free', '0')
windows_store['price'] = windows_store['price'].str.replace('₹ ', '')

windows_store['price'] = windows_store['price'].astype(str)
windows_store['price'] = windows_store['price'].str.strip('+, ')

#convertire la colonna del prezzo in numero decimale e convertire in USD
windows_store['price'] = np.float64(windows_store['price'].str.replace(',', ''))*0.013
windows_store

#%%

#aggiungere una nuova colonna che specifica lo store

windows_store["store"] = "windows_store"
windows_store


#%%

#APPLESTORE

#Importare il dataframe
appstore = pd.read_csv(os.path.join(data_folder,'AppleStore.csv'))
appstore

#%%

#pulire le colonne

appstore = appstore.loc[:,["name","size_bytes","price","installs","rating","category", "rating_count_ver"]]

appstore.columns = ["name","size","price","installs","rating","category","No of people Rated"]
appstore

#%%

#aggiungere una nuova colonna che specifica lo store

appstore["store"] = "appstore"
appstore



#%%

#UNISCO I DATAFRAME
alldata = pd.DataFrame()
alldata = pd.concat([playstore,appstore,windows_store])
alldata


#%%

dict_categories = {'Health & Fitness':['Beauty','Health & Fitness','Medical','Health and Fitness'],
                       'Photos & Videos':['Video Players & Editors','Art & Design','Photography', 'Multimedia Design', 'Photo & Video'],
                       'News':['Weather', 'News & Magazines', 'Sports','News and Weather', 'Weather', 'News'],
                       'Games':['Puzzle', 'Adventure', 'Action', 'Arcade', 'Trivia', 'Word', 'Music', 'Casual', 'Card', 'Simulation', 'Role Playing', 'Strategy', 'Casino', 'Comics', 'Board', 'Educational', 'Racing'],
                       'Music':['Music & Audio', 'Music'],
                       'Business': ['Finance', 'Government and Politics', 'Business'],
                       'Social' : ['Communication', 'Dating', 'Entertainment', 'Social', 'Events', 'Social Networking'],
                       'Lifestyle' : ['Personalization', 'Shopping', 'Lifestyle'],
                       'Tools & Utilities' : ['Productivity', 'Tools', 'Libraries & Demo','House & Home', 'Catalogs', 'Utilities','Developer Tools'],
                       'Food & Drink' : ['Food & Drink', 'Food and Dining'],
                       'Maps & Navigation' : ['Auto & Vehicles', 'Maps & Navigation', 'Travel', 'Travel & Local', 'Navigation and Maps', 'Navigation'],
                       'Books & Reference' : ['Books & Reference', 'Books', 'Book', 'Reference'],
                       'Education' : ['Education', 'Parenting', 'Kids and Family']}


for k,v in dict_categories.items():
    for x in k,v:
        alldata['category'].replace(x,k, inplace = True)

alldata

#%%

print(set(alldata['category'].tolist()))
