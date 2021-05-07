#%%

import csv
import json
import numpy as np
import pandas as pd
import os.path
import appstore as app
import seaborn as sb


#%%

#DATA LOADING - CLEANING
data_folder = os.getcwd()
file_dir_names = os.listdir(data_folder)
print(data_folder,'\n', file_dir_names)

#%%

#PLAYSTORE
#Importare il dataframe
playstore = pd.read_csv(os.path.join(data_folder,'playstore.csv'))

#%%

#pulire le colonne
playstore = playstore.loc[:,["app_name","genre","rating","reviews","cost_label","size","installs"]]

playstore.columns = ["name","category","rating","reviews","price","size (MB)","installs"]
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

playstore['size (MB)'] = playstore['size (MB)'].astype(str)
bad = ['M',',','k']
for s in bad:
    playstore["size (MB)"] = playstore["size (MB)"].str.replace(s,"")

playstore['size (MB)'] = playstore['size (MB)'].str.replace('Varies with device','0')
playstore['size (MB)']= playstore['size (MB)'].fillna(0)

playstore['installs'] = playstore['installs'].str.strip('+')
playstore['installs'] = playstore['installs'].str.replace(',', '')
playstore['reviews'] = playstore['reviews'].str.replace(' total', '')
playstore['reviews'] = playstore['reviews'].str.replace(',', '')
playstore

#%%

playstore['size (MB)'] = np.float64(playstore['size (MB)'])

#%%

#aggiungere una nuova colonna che specifica lo store
playstore["store"] = "playstore"

#%%

playstore['reviews']=np.float64(playstore['reviews'])
playstore

#%%

#WINDOWS
#Importare il dataframe
windows_store = pd.read_csv(os.path.join(data_folder,'msft.csv'))

#%%

#pulire le colonne
windows_store = windows_store.loc[:,["Name","Rating","No of people Rated","Category","Price"]]
windows_store.columns = ["name","rating","No of people Rated","category","price"]
windows_store['size (MB)'] = 0.0

#%%

#pulire la colonna del prezzo
windows_store['price'] = windows_store['price'].str.replace('Free', '0')
windows_store['price'] = windows_store['price'].str.replace('₹ ', '')

windows_store['price'] = windows_store['price'].astype(str)
windows_store['price'] = windows_store['price'].str.strip('+, ')

#convertire la colonna del prezzo in numero decimale e convertire in USD
windows_store['price'] = np.float64(windows_store['price'].str.replace(',', ''))*0.013

#%%

#aggiungere una nuova colonna che specifica lo store
windows_store["store"] = "windows_store"

#%%

windows_store['No of people Rated']=np.float64(windows_store['No of people Rated'])
windows_store

#%%

#APPLESTORE
#Importare il dataframe
appstore = pd.read_csv(os.path.join(data_folder,'AppleStore.csv'))
appstore

#%%

#pulire le colonne
appstore = appstore.loc[:,["name","size_bytes","price","installs","rating","category", "rating_count_ver"]]
appstore.columns = ["name","size (MB)","price","installs","rating","category","No of people Rated"]
appstore['size (MB)'] = np.float64(appstore['size (MB)'])/1000000

#%%

#aggiungere una nuova colonna che specifica lo store
appstore["store"] = "appstore"
appstore['No of people Rated']= np.float64(appstore['No of people Rated'])
appstore

#%%

#UNISCO I DATAFRAME
alldata = pd.DataFrame()
alldata = pd.concat([playstore,appstore,windows_store])
alldata

#%%

#UNISCO LE COLONNE
alldata['No of people Rated'] = alldata['No of people Rated'].fillna(0)
alldata['reviews'] = alldata['reviews'].fillna(0)

alldata['interactions'] = alldata['reviews'] + alldata['No of people Rated']
alldata = alldata.loc[:,['name','price','interactions','category', 'store', 'rating', 'size (MB)']]

alldata = alldata.dropna(thresh=4)

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

#QUESTION N. 1


for k,v in dict_categories.items():
    for x in v:
        alldata['category'] = alldata['category'].str.replace(x,k)

alldata

#%%

print(app.top_categories_weighted(alldata))

#%%

print(app.top_categories_weighted(alldata,'playstore'))

#%%

print(app.top_categories_weighted(alldata,'appstore'))

#%%

print(app.top_categories_weighted(alldata,'windows_store'))
