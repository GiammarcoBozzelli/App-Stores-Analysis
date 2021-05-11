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

#%% md

<h2>Research Question 2</h2>
<p>For which App Category are users willing to pay more?<br>

1) For each app with same category we compute the price mean<p>
2) Then we represent it graphically <p>

#%%

#Creating a copy to work safely
df = alldata.copy()

#Selecting the essential columns for our research question
df = df[['category', 'price']]
df

#%% md

- It appears that there are some app with Nan values in the interested columns: price, categories
- They both will be removed, in order to procced with the research question

#%%

#Checking how many Nan values per columns
df.isnull().sum()

#%%

#dropping the Nan values of the price and category columns
df.dropna(subset=['price','category'], inplace=True)

#%%

#checking the results
df.isnull().sum()

#%% md

We can now work on the research question:<p>
- For each category a mean will be computed
- The mean will be displayed and sorted in a new dataframe

#%%

#Finding all the categories and storing them in a list
price_mean_dict= {}

categories = (df['category'].tolist())  # getting all category types
category_list = [] # dict to contain all the categories
for category in categories:  # filling the dictionary
   if category not in category_list:
       category_list.append(category)
   else:
       continue
category_list


#%%

#Use the previous list to create a dictionary with the price mean of each category
for x in category_list:
    a = df[df['category']==x]
    price_mean_dict[x]=a['price'].mean(axis=0)

price_mean_dict


#%%

#Visualising the dictionary in a series

df_mean_price = pd.Series(price_mean_dict).rename_axis('category').reset_index(name='mean price')
df_mean_price

#%%

#sorting values in ascending order
df_mean_price.sort_values(by=['mean price'], inplace=True)
df_mean_price

#%% md

As we can clearly see from the data, the categories: Education and Tool & Utilities are the ones with highest prices.

#%% md

<h4>Graphical representation </h4>

- We are now going to display the results trough a bar chart


#%%

df_mean_price.plot.barh(x='category', y='mean price', rot=0, color=['orange','blue'])

#%%

#Computing summary statistic
df_mean_price.describe()

#%% md

<h4> Conclusion <h4>

#%% md

The catgories below categories are the most expensive among all the stores
- Education
- tools & Utilities
- Health & Fitness

#%%

#QUESTION N. 5

frame = alldata.sort_values(by = ['rating', 'interactions'], ascending = False)
frame.head(10)
#to select the first 50 popular apps
top_50 = frame.iloc[:50,:]

#%%

#to drop rows with size = 0
top_50 = top_50.drop(top_50[(top_50['size (MB)'] == 0)].index)
top_50

#%%

category_rating_dic = app.dictionary_top(top_50,'category')
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

top_50.plot.bar(x="name", y="size (MB)", rot=70, title="Size (MB) in the top 50", figsize = (15,8))
plt.show()

#%%

#remove the 5 applications with largest size
for i in range(7):
    top_50.drop(top_50['size (MB)'].idxmax(), inplace = True)

#%%

top_50.plot.bar(x="name", y="size (MB)", rot=70, title="Size (MB) in the top 50")
plt.show(block=True)

#%%

#trovare mean e standard deviation del grafico
print('Mean =',top_50['size (MB)'].mean())
print('Standard Deviation =',top_50['size (MB)'].std())
#conviene fare un applicazione di max 78 + 48 MB

#%%

#PRICE - Free
price_top = frame.iloc[:50,:]
price_dic = app.dictionary_top(price_top,'price')
prices = (price_top['price'].tolist())  # getting all category types
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
price_dic = app.dictionary_top(price_top,'price')
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
store_dic = app.dictionary_top(store_top,'store')
store_dic

#%%

#plot a pie chart
plt.pie(list(store_dic.values()),labels = list(store_dic.keys()), explode = (0.2,0))

#%%

#let's now put together all the most common characteristics to find apps that ahve them all
top_50 = top_50[top_50['category'] == 'Games']
top_50 = top_50.loc[(top_50['size (MB)'] >= 29) & (top_50['size (MB)'] <= 127)]
top_50 = top_50.loc[top_50['price'] == 0]
top_50 = top_50.loc[top_50['store'] == 'appstore']

top_50
