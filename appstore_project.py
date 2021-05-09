#%%

import csv
import json
import numpy as np
import pandas as pd
import os.path
import appstore as app
import seaborn as sb
import matplotlib.pyplot as plt

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
        alldata['category'].replace(x, k, inplace = True)

alldata

#%%

print(app.top_categories_weighted(alldata))

#%%

print(app.top_categories_weighted(alldata,'playstore'))

#%%

print(app.top_categories_weighted(alldata,'appstore'))

#%%

print(app.top_categories_weighted(alldata,'windows_store'))

#%%

#figure, axis = plt.subplots(3)

#%%

print(app.top_categories_weighted(alldata))

allcateg_dict= app.top_categories_weighted(alldata)

app.grafic_rating(allcateg_dict)

#%%

print(app.top_categories_weighted(alldata,'playstore'))

pscateg_dict=app.top_categories_weighted(alldata,'playstore')

app.grafic_rating(pscateg_dict)

#%%

print(app.top_categories_weighted(alldata,'appstore'))

ascateg_dict=app.top_categories_weighted(alldata,'appstore')

app.grafic_rating(ascateg_dict)

#%%

print(app.top_categories_weighted(alldata,'windows_store'))

wscateg_dict=app.top_categories_weighted(alldata,'windows_store')

app.grafic_rating(wscateg_dict)

#%%

#QUESTION N. 5

frame=alldata.sort_values(by = ['rating', 'interactions'], ascending = False)
frame.head(10)
#to select the first 100 popular apps
top_50=frame.iloc[:50,:]

#%%

#to drop rows with size = 0
top_50 = top_50.drop(top_50[(top_50['size (MB)'] == 0)].index)
top_50

#%%

categories = (top_50['category'].tolist())  # getting all category types
category_rating_dic = {} # dict to contain the rating for each category type
for category in categories:  # filling the dictionary
   if category not in category_rating_dic:
       category_rating_dic[category]=1
   else:
       category_rating_dic[category]+=1
category_rating_dic

#%%

categories = category_rating_dic.keys()
ratings = category_rating_dic.values()
y_pos = np.arange(len(categories))

plt.barh(y_pos, ratings, align='center', alpha=0.5)
plt.yticks(y_pos, categories)
plt.xlabel('rating')
plt.ylabel('categories')
plt.title('which is the most common category in the top 50 apps?')
plt.show()

#%%

top_50.plot.bar(x="name", y="size (MB)", rot=70, title="Size (MB) in the top 50")
plt.show(block=True)

#%%

#remove the 5 applications with largest size
for i in range(7):
    top_50.drop(top_50['size (MB)'].idxmax(), inplace = True)

#%%

top_50.plot.bar(x="name", y="size (MB)", rot=70, title="Size (MB) in the top 50")
plt.show(block=True)

#%%

#trovare mean e standard deviation del grafico
print('Mean = ',top_50['size (MB)'].mean())
print('Standard Deviation = ',top_50['size (MB)'].std())
#conviene fare un applicazione di max 78 + 48 MB

#%%

#PRICE - Free
price_top = frame.iloc[:50,:]
prices = (price_top['price'].tolist())  # getting all category types
price_dic = {} # dict to contain the rating for each category type
for price in prices:  # filling the dictionary
   if price not in price_dic:
       price_dic[price]=1
   else:
       price_dic[price]+=1
price_dic

#%%

categories = price_dic.keys()
ratings = price_dic.values()
y_pos = np.arange(len(categories))

plt.barh(y_pos, ratings, align='center', alpha=0.5)
plt.yticks(y_pos, categories)
plt.xlabel('rating')
plt.ylabel('categories')
plt.title('which is the most common category in the top 50 apps?')
plt.show()

#%%

#Price - Big money
price_top = frame.iloc[:100,:]
price_top = price_top.drop(price_top[(price_top['price'] == 0.0)].index)
prices = (price_top['price'].tolist())  # getting all category types
price_dic = {} # dict to contain the rating for each category type
for price in prices:  # filling the dictionary
   if price not in price_dic:
       price_dic[price]=1
   else:
       price_dic[price]+=1
price_dic

#%%

categories = price_dic.keys()
ratings = price_dic.values()
y_pos = np.arange(len(categories))

plt.barh(y_pos, ratings, align='center', alpha=0.5)
plt.yticks(y_pos, categories)
plt.xlabel('rating')
plt.ylabel('categories')
plt.title('which is the most common category in the top 50 apps?')
plt.show()

#%%

'''#Price - Big money
price_top = frame.iloc[:500,:] #aumento numero app per vedere che prezzo conviene siccome 1$ e 4.99 uguali
price_top = price_top.drop(price_top[(price_top['price'] == 0.0)].index)
prices = (price_top['price'].tolist())  # getting all category types
price_dic = {} # dict to contain the rating for each category type
for price in prices:  # filling the dictionary
   if price not in price_dic:
       price_dic[price]=1
   else:
       price_dic[price]+=1
price_dic
'''

#%%

#STORE
#Price - Big money
store_top = frame.iloc[:50,:]
prices = (store_top['store'].tolist())  # getting all category types
price_dic = {} # dict to contain the rating for each category type
for price in prices:  # filling the dictionary
   if price not in price_dic:
       price_dic[price]=1
   else:
       price_dic[price]+=1
price_dic

#%%

#Grafico??
