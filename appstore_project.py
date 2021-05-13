#%% md

# Group 1
# Are different Appstores so different?
<ul><b>
<li> Bozzelli Giammarco</li>
<li>Cavalieri Marco</li>
<li>Lupi Isaac</li>
<li>Parigi Michele</li>
<li>Sibilia Beatrice</li>
</ul><b>

#%% md

## Link to the Google Drive folder containing the datasets

__[group-1-project](https://drive.google.com/drive/folders/1WpJfuIUlIh2z5hbM_b9GL8sOLfwKgE_n?usp=sharing)__
#%% md

## Data Loading and Cleaning

Before starting we import all the modules we will need troughout the project

#%%

import os.path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import appstore as app #import as app the module we created to store functions in

#%% md

We decided to <b> load </b> and <b> clean </b> one dataset at the time starting from the file <i> 'playstore.csv' </i>
### Playstore.csv

#%% md

First fo all we need to make sure that the file path is always correct no matter the operating system to do this we decided to use the 'os.getcwd()' function, and also we print the list of the files in the folder path

#%%

data_folder = os.getcwd() #get the current working directory that we will use as path
file_dir_names = os.listdir(data_folder) #list of all files in the directory
print(data_folder,'\n', file_dir_names)

#%% md

Then we import the dataset from <i> 'playstore.csv' </i> directly as a DataFrame using the Pandas' funciton <i> '.read_csv' </i>

#%%

playstore = pd.read_csv(os.path.join(data_folder,'playstore.csv'))# open playstore.csv as a Pandas DataFrame
playstore

#%% md

Now we keep only the columns we will need to use and we rename them

#%%

playstore = playstore.loc[:,["app_name","genre","rating","reviews","cost_label","size","installs"]] #get only the columns we need
playstore.columns = ["name","category","rating","reviews","price","size (MB)","installs"] #renaming all columns

#%% md

Time to start cleaning the <b>playstore</b> DataFrame!

#%%

playstore['price'] = playstore['price'].astype(str) #convert all cells in the columns into strings

bad = [",","₫"," Buy"] #list of all things to remove
for s in bad:
    playstore["price"] = playstore["price"].str.replace(s,"")

playstore['price'] = playstore['price'].str.replace('Install', '0')
playstore['price'] = playstore['price'].str.split(' ').str[-1] #was 200 now is 7

#convert the 'price' column to np.float32 and from vietnamese dong to USD
playstore['price'] = np.float32(playstore['price'])*0.000043

#%%

playstore['size (MB)'] = playstore['size (MB)'].astype(str)
bad = ['M',',','k']
for s in bad:
    playstore["size (MB)"] = playstore["size (MB)"].str.replace(s,"")

playstore['size (MB)'] = playstore['size (MB)'].str.replace('Varies with device','0')
playstore['size (MB)']= playstore['size (MB)'].fillna(0)
playstore['size (MB)'] = np.float64(playstore['size (MB)'])

#%%

playstore['installs'] = playstore['installs'].str.strip('+')
playstore['installs'] = playstore['installs'].str.replace(',', '')

#%%

playstore['reviews'] = playstore['reviews'].str.replace(' total', '')
playstore['reviews'] = playstore['reviews'].str.replace(',', '')
playstore['reviews']=np.float64(playstore['reviews'])

#%% md

The last thing we need to do now is add a column <i><b> 'store' </b></i> that specifies to store, this well be useful when we will merge together all datasets

#%%

playstore["store"] = "playstore" #add a column to specify the store
playstore

#%% md

## Msft.csv -> microsoft store
As we did before we import the dataset as a DataFrame using the Pandas' funciton '.read_csv'

#%%

microsoft_store = pd.read_csv(os.path.join(data_folder, 'msft.csv'))
microsoft_store

#%% md

We then procede selecting only the columns we need and renaming them.
This time we replace

#%%

#clean columns
microsoft_store = microsoft_store.loc[:, ["Name", "Rating", "No of people Rated", "Category", "Price"]] #get only the columns we nee
microsoft_store.columns = ["name", "rating", "No of people Rated", "category", "price"]#renaming the columns
microsoft_store['size (MB)'] = 0.0 #add 0 because we do not want nan in this columns when we merge all datasets

#%%

#clean the 'price' column
microsoft_store['price'] = microsoft_store['price'].str.replace('Free', '0')
microsoft_store['price'] = microsoft_store['price'].str.replace('₹ ', '')

microsoft_store['price'] = microsoft_store['price'].astype(str)
microsoft_store['price'] = microsoft_store['price'].str.strip('+, ')#remove leading and trailing single characters

#convert the 'price' column to float64 and from Indian rupee to USD
microsoft_store['price'] = np.float64(microsoft_store['price'].str.replace(',', '')) * 0.013

#%%

#add the 'store' column
microsoft_store["store"] = "microsoft_store"

#%%

microsoft_store['No of people Rated']=np.float64(microsoft_store['No of people Rated'])
microsoft_store

#%%

#APPLESTORE
#import the dataset
appstore = pd.read_csv(os.path.join(data_folder,'AppleStore.csv'))
appstore

#%%

#clean columns
appstore = appstore.loc[:,["name","size_bytes","price","installs","rating","category", "rating_count_ver"]]
appstore.columns = ["name","size (MB)","price","installs","rating","category","No of people Rated"]
appstore['size (MB)'] = np.float64(appstore['size (MB)'])/1000000 #convert from bytes to megabytes

#%%

#aggiungere una nuova colonna che specifica lo store
appstore["store"] = "appstore"
appstore['No of people Rated']= np.float64(appstore['No of people Rated'])
appstore

#%%

#Merge Dataframes
alldata = pd.concat([playstore, appstore, microsoft_store])
alldata

#%%

#Clean columns
alldata['No of people Rated'] = alldata['No of people Rated'].fillna(0)
alldata['reviews'] = alldata['reviews'].fillna(0)

alldata['interactions'] = alldata['reviews'] + alldata['No of people Rated'] #merge 'reviews' and 'No of people rated' into 'interaction'
alldata = alldata.loc[:,['name','price','interactions','category', 'store', 'rating', 'size (MB)']] #select only comuns we want

alldata = alldata.dropna(thresh=4) #remove rows with more than 4 NaN values

#%%

dict_categories = {'Health & Fitness':['Beauty','Medical','Health and Fitness'],
                       'Photos & Videos':['Video Players & Editors','Art & Design','Photography', 'Multimedia Design', 'Photo & Video'],
                       'News':['Weather', 'News & Magazines', 'Sports','News and Weather', 'Weather'],
                       'Games':['Puzzle', 'Adventure', 'Action', 'Arcade', 'Trivia', 'Word', 'Music', 'Casual', 'Card', 'Simulation', 'Role Playing', 'Strategy', 'Casino', 'Comics', 'Board', 'Educational', 'Racing'],
                       'Music':['Music & Audio'],
                       'Business': ['Finance', 'Government and Politics'],
                       'Social' : ['Communication', 'Dating', 'Entertainment', 'Events', 'Social Networking'],
                       'Lifestyle' : ['Personalization', 'Shopping'],
                       'Tools & Utilities' : ['Productivity', 'Tools', 'Libraries & Demo','House & Home', 'Catalogs', 'Utilities','Developer Tools'],
                       'Food & Drink' : ['Food and Dining'],
                       'Maps & Navigation' : ['Auto & Vehicles', 'Travel', 'Travel & Local', 'Navigation and Maps', 'Navigation'],
                       'Books & Reference' : ['Books', 'Book', 'Reference'],
                       'Education' : ['Parenting', 'Kids and Family']}


for k,v in dict_categories.items():
    for x in v:
        alldata['category'].replace(x, k, inplace = True) #replace sub categories with the categories we want

#%%
pie = app.pie_chart(alldata)

#%% md

## Question N.1
### Which App Category do users prefer?
#%%

print(app.top_categories_weighted(alldata))

#%%

print(app.top_categories_weighted(alldata,'playstore'))

#%%

print(app.top_categories_weighted(alldata,'appstore'))

#%%

print(app.top_categories_weighted(alldata,'microsoft_store'))

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

print(app.top_categories_weighted(alldata,'microsoft_store'))

mccateg_dict=app.top_categories_weighted(alldata,'microsoft_store')

app.grafic_rating(mccateg_dict)

#%% md

## Question N.2
### For which App Category are users willing to pay more?

1. For each app with same category we compute the price mean<p>
1. Then we compute the mean of interactions per category <p>
1. Then we find a relation between the two and sort it in a new dataframe <p>
1. Finally we represent it graphically <p>


#%%

#Creating a copy to work safely
df = alldata.copy()

#Selecting the essential columns for our research question
df = df[['category', 'price','interactions','store']]
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
- For each category the sum of interactions will be computed
- The mean and the interactions will be displayed and sorted in a new dataframe

#%%

#Finding all the categories and storing them in a list

categories = (df['category'].tolist())  # getting all category types
category_list = [] # dict to contain all the categories
for category in categories:  # filling the dictionary
   if category not in category_list:
       category_list.append(category)
   else:
       continue
category_list

#%% md

Note: we are computing the mean of interactions since it is a liable indicator of how many people downloaded the app.

#%%

#Use the previous list to create a dictionary with the price mean of each category
price_mean_dict= {}  #creating an empty list to store the key=category and values=means
interaction_list= [] #creating an empty list just to store the sum of interactions for each category
for x in category_list:
    a = df[df['category']==x] #acceding the right rows for each category
    price_mean_dict[x]=a['price'].mean() #computing the mean over the columns for the series a['price'] of that specific category
    interaction_list.append(a['interactions'].mean()) #computing the mean over the columns for the series a['interactions'] of that specific category
print(price_mean_dict)
print(interaction_list)

#%%

#Visualising the dictionary in a dataframe and the list in a series

df_mean_price = pd.Series(price_mean_dict).rename_axis('category').reset_index(name='mean price ($)')
print(df_mean_price)
df_interaction = pd.Series(interaction_list).rename_axis('mean of interactions')
print(df_interaction)

#%%

#Merging the series with the dataframe
frames = [df_mean_price,df_interaction]
merged_frame = pd.concat(frames, axis=1)
merged_frame.rename(columns = {0:'mean of interactions'}, inplace = True) #renaming the column
merged_frame['mean of interactions'] = merged_frame['mean of interactions'].astype(int) #changint the type of the column, in order to make it more comprehensible
merged_frame

#%% md

- Now we have to understand what's the mean revenue for each app of the category in order to answer our research question <p>
- to compute it we just need to multuply the last two columns

#%%

#creating a new column
merged_frame['mean revenues per app ($)']=merged_frame['mean price ($)']*merged_frame['mean of interactions']
merged_frame

#%%

#Sorting values by mean revenues per app
merged_frame.sort_values(by= ['mean revenues per app ($)'], ignore_index=True, inplace=True ,ascending=False)
merged_frame
#%% md

<h4>Graphical representation </h4>

- We are now going to display the mean revenue per application trough a **bar chart**


#%%

merged_frame.plot.barh(x='category', y='mean revenues per app ($)', color=['orange','blue'], figsize = (8,5))
plt.ylabel('Category', fontsize = 12)
plt.title('Revenue per Application', fontsize = 15)


#%% md

#### Analytical conclusion

We can clearly see from the sorted dataframe and the graph that the categories for which users are willing to pay more are:
1. Photos & Videos
1. Social
1. Games



#%% md
## Question N.3
### Does users’ rating depend on price?
#%%
df = alldata[alldata.price < 100]
fig, ax = plt.subplots()
fig.set_size_inches(8, 5)
sns.regplot(x='price', y='rating',data=df,
            fit_reg= True, color = 'g',dropna=True, line_kws={'color' :'red'})
#%%
df = df[df['price'] < 60]
fig, ax = plt.subplots()
fig.set_size_inches(8, 5)
sns.regplot(x='price', y='rating',data=df, color = 'b',dropna=True,  line_kws={'color' : 'r'})
#%% md
## Question N.4
### Do ratings, popularity and prices depend on applications' size?
#%%
x=alldata["size (MB)"]
y=alldata['price']

#%%

def linear_regression(x, y):
    N = len(x)
    x_mean = x.mean()
    y_mean = y.mean()

    B1_num = ((x - x_mean) * (y - y_mean)).sum()
    B1_den = ((x - x_mean)**2).sum()
    B1 = B1_num / B1_den

    B0 = y_mean - (B1*x_mean)

    reg_line = 'y = {} + {}β'.format(B0, round(B1, 3))

    return (B0, B1, reg_line)

#%%

def corr_coef(x, y):
    N = len(x)

    num = (N * (x*y).sum()) - (x.sum() * y.sum())
    den = np.sqrt((N * (x**2).sum() - x.sum()**2) * (N * (y**2).sum() - y.sum()**2))
    R = num / den
    return R

#%%

B0, B1, reg_line = linear_regression(x, y)
print('Regression Line: ', reg_line)
R = corr_coef(x, y)
print('Correlation Coef.: ', R)
print('"Goodness of Fit": ', R**2)

#%%
sns.regplot(x="size (MB)", y="price",data=alldata,
            fit_reg= True, color = 'g',dropna=True, line_kws={'color' :'red'})


#%%
data = alldata.drop(alldata[(alldata['price'] >= 60)].index)
data = data.loc[(data['size (MB)'] > 0) & (data['size (MB)'] < 2000)]

sns.regplot(x="size (MB)", y="price",data=data,
            fit_reg= True, color = 'g', dropna=True,line_kws={'color' :'red'})
#%%
# Using pairplot we'll visualize the data for correlation
sns.pairplot(data, x_vars="size (MB)",
             y_vars="price", size=4, aspect=1, kind='scatter')
plt.show()

#%% md

## Question 5
#%%

frame = alldata.sort_values(by = ['rating', 'interactions'], ascending = False)
frame.head(10)
#to select the first 50 popular apps
top_50 = frame.iloc[:50,:]

#%%

#to drop rows with size = 0
top_50 = top_50.drop(top_50[(top_50['size (MB)'] == 0)].index)
top_50.head(10)

#%%

category_dic = app.dictionary_top(top_50,'category')
category_dic

#%%

categories = category_dic.keys()
ratings = category_dic.values()
y_pos = np.arange(len(categories))
plt.figure(figsize = (9,6))
plt.barh(y_pos, ratings, align='center', alpha=0.5)
plt.yticks(y_pos, categories)
plt.xlabel('Number of Apps',  fontsize = 12)
plt.ylabel('Categories', fontsize = 12)
plt.title('Which is the most common category in the top 50 apps?', fontsize = 15)
plt.show()

#%%

top_50.plot.bar(x="name", y="size (MB)", figsize = (15,8))
plt.title("Size (MB) in the top 50", fontsize = 18)
plt.xticks([]) # Disable xticks.
plt.xlabel('Applications', fontsize = 15)
plt.ylabel('Size in MB', fontsize = 15)
plt.show()

#%%

#remove the 5 applications with largest size
for i in range(7):
    top_50.drop(top_50['size (MB)'].idxmax(), inplace = True)

#%%

top_50.plot.bar(x="name", y="size (MB)", figsize = (15,8))
plt.title("Size (MB) in the top 50", fontsize = 18)
plt.xticks([]) # Disable xticks.
plt.xlabel('Applications', fontsize = 15)
plt.ylabel('Size in MB', fontsize = 15)
plt.show()

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
plt.figure(figsize = (9,6))
plt.barh(y_pos, ratings, align='center', alpha=0.5)
plt.yticks(y_pos, categories)
plt.xlabel('Rating', fontsize = 12)
plt.ylabel('Categories', fontsize = 12)
plt.title('which is the most common category in the top 50 apps?', fontsize = 15)
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
plt.figure(figsize = (9,6))
plt.barh(y_pos, ratings, align='center', alpha=0.5)
plt.yticks(y_pos, categories)
plt.xlabel('Rating', fontsize = 12)
plt.ylabel('Categories', fontsize = 12)
plt.title('Which is the most common category in the top 50 apps?', fontsize = 15)
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
plt.figure(figsize = (6,6))
plt.pie(list(store_dic.values()),labels = list(store_dic.keys()), explode = (0.2,0))

#%%

#let's now put together all the most common characteristics to find apps that ahve them all
top_50 = top_50[top_50['category'] == 'Games']
top_50 = top_50.loc[(top_50['size (MB)'] >= 29) & (top_50['size (MB)'] <= 127)]
top_50 = top_50.loc[top_50['price'] == 0]
top_50 = top_50.loc[top_50['store'] == 'appstore']

top_50

#%%

