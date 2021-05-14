#%% md

# Group 1
# Are different Appstores so different?
<ul><b>
<li> Bozzelli Giammarco</li>
<li>Cavaliere Marco</li>
<li>Lupi Isaac</li>
<li>Parigi Michele</li>
<li>Sibilia Beatrice</li>
</ul><b>

#%% md

## Link to the Google Drive folder containing the datasets

__[group-1-project](https://drive.google.com/drive/folders/1WpJfuIUlIh2z5hbM_b9GL8sOLfwKgE_n?usp=sharing)__

#%% md

## Data Loading and Cleaning
**<i>(Beatrice Sibilia, Giammarco Bozzelli</i> and <i> Marco Cavaliere)**</i>

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

First fo all we need to make sure that the file path is always correct no matter the operating system, to do this we decided to use the 'os.getcwd()' function, and also we print the list of the files in the folder path

#%%

data_folder = os.getcwd() #get the current working directory that we will use as path
file_dir_names = os.listdir(data_folder) #list of all files in the directory
print(data_folder,'\n', file_dir_names)

#%% md

Then we import the dataset from <i> 'playstore.csv' </i> directly as a DataFrame using the Pandas' function <i> '.read_csv' </i>

#%%

playstore = pd.read_csv(os.path.join(data_folder,'playstore.csv'))# open playstore.csv as a Pandas DataFrame
playstore

#%% md

Now we keep only the columns we will need to use and rename them

#%%

playstore = playstore.loc[:,["app_name","genre","rating","reviews","cost_label","size","installs"]] #get only the columns we need
playstore.columns = ["name","category","rating","reviews","price","size (MB)","installs"] #renaming all columns

#%% md

Time to start cleaning the <b>playstore</b> DataFrame!

First thing first we remove from the **_'price'_** column all unnecessary characters by replacing them with an empty string. We noted that in the
dataframe free applications were marked with the label _'Install'_ so we replaced it with _zero (0)_ , also some
apps had an historical report of price changes ( _Was X now is Y_ ) so what we did was change this string into a list
(_split(' ')_) to then select the last item _str[-1]_. Lastly we convert the column from _str_ to _numpy.float32_ type and
convert the price from Vietnamese Dong to USD

#%%

bad = [",","₫"," Buy"] #list of all things to remove
for s in bad:
    playstore["price"] = playstore["price"].str.replace(s,"")

playstore['price'] = playstore['price'].str.replace('Install', '0')
playstore['price'] = playstore['price'].str.split(' ').str[-1] #was 200 now is 7
playstore['price'] = np.float32(playstore['price'])*0.000043

#%% md

We go on cleaning the **_'size'_** column by removing unwanted characters, replacing NaN values with 0
(that we will later on remove) and converting the column into _numpy.float32_

#%%

bad = ['M',',','k']
for s in bad:
    playstore["size (MB)"] = playstore["size (MB)"].str.replace(s,"")

playstore['size (MB)'] = playstore['size (MB)'].str.replace('Varies with device','0')
playstore['size (MB)']= playstore['size (MB)'].fillna(0)
playstore['size (MB)'] = np.float32(playstore['size (MB)'])

#%% md

Now is time to clean the **_'installs'_** and the **_'reviews'_** columns

#%%

playstore['installs'] = playstore['installs'].str.strip('+')
playstore['installs'] = playstore['installs'].str.replace(',', '')
playstore['installs'] = np.float32(playstore['installs'])

#%%

playstore['reviews'] = playstore['reviews'].str.replace(' total', '')
playstore['reviews'] = playstore['reviews'].str.replace(',', '')
playstore['reviews']=np.float32(playstore['reviews'])

#%% md

The last thing we need to do now is add a column **_'store' _** that specifies to store, this well be useful when we will merge all datasets together

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

#microsoft_store['price'] = microsoft_store['price'].astype(str)
microsoft_store['price'] = microsoft_store['price'].str.strip('+, ')#remove leading and trailing single characters

#convert the 'price' column to float64 and from Indian rupee to USD
microsoft_store['price'] = np.float32(microsoft_store['price'].str.replace(',', '')) * 0.013

#%%

#add the 'store' column
microsoft_store["store"] = "microsoft_store"

#%%

microsoft_store['No of people Rated']=np.float32(microsoft_store['No of people Rated'])
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
**<i>(Giammarco Bozzelli</i> and <i>Marco Cavaliere)**</i>

Since we want to find the category that users prefer we need to give applications a more _realistic_ rating,
this is becasue one app may have a **5 stars rating** but just **few interactions**, so we have to give a **_weight_**
to each rating. To do this we have built the **top_categories_weighted** function in the _appstore_ module that takes as
input a Dataframe and _optionally_ the store name that we want to study, and return a dictionary with categories as keys
and the _weighted ratings_ as values.

We also created another function called **_graphic rating_** to create and print the dictionary coming
from the **top_categories_weighted** function to visualize results

#%% md

We first analyze each store differently, so we:
- Use the _top categories weighted_ function to get the dictionary
- Use the _praphic rating_ function to represent results

We start from  **Playstore**

#%%


pscateg_dict=app.top_categories_weighted(alldata,'playstore')

app.grafic_rating(pscateg_dict)

#%% md

As we can see by the graph above the **_Health & Fitness_** category is the highest rated in the _Playstore_.

We then move on analyzing the **_Applestore_**

#%%


ascateg_dict=app.top_categories_weighted(alldata,'appstore')

app.grafic_rating(ascateg_dict)

#%% md

And the **_Lifestyle_** category results as the prefered one in the _Appstore_.

Now it is turn for the **_Microsoftstore_**

#%%

mccateg_dict=app.top_categories_weighted(alldata,'microsoft_store')

app.grafic_rating(mccateg_dict)

#%% md

In the _Microsoftstore_ the most liked category is **_Education_**.

### What will happen if we use all appstores together?

#%%

allcateg_dict= app.top_categories_weighted(alldata)

app.grafic_rating(allcateg_dict)

#%% md

### Results
The prefered category is different for eache store:
- **Playstore** --> _Health & Fitness_
- **Appstore** --> _Lifestyle_
- **Microsoft** --> _Education_

But if we use the whole DataFrame we found that the highest rated category is: **Health & Fitness**

#%% md

## Question N.2
### For which App Category are users willing to pay more?
<i>**(Isaac Lupi)**</i>
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
plt.ylabel('Category', fontsize = 13)
plt.title('Mean Application Revenue per Category', fontsize = 15)


#%% md

#### Analytical conclusion

We can clearly see from the sorted dataframe and the graph that the categories for which users are willing to pay more are:
1. Photos & Videos
1. Social
1. Games



#%% md

## Question N.3
### Does users’ rating depend upon price?
<i>**(Michele Parigi)**</i>

#%% md

We make a prediction: there will be higher ratings for apps that cost more because they should be at an higher quality.

First, we try to make the analysis with prices below 100$ because there are not many data over that digit.

#%%

# we modify the dataset to have only prices below 100$
df = alldata[alldata.price < 100]

# we set the size of the graph
fig, ax = plt.subplots()
fig.set_size_inches(8, 5)
# we create the regression line through seaborn
sns.regplot(x='price', y='rating', data=df,
            fit_reg= True, color='g', dropna=True, line_kws={'color':'red'})

#%% md

It seems that there is no correlation between price and users' rating. Now we try setting 60$ as limit of price to see if there are any changes.

#%%

# we modify the dataset to have only prices below 60$
df = alldata[alldata.price < 60]

# we set the size of the graph
fig, ax = plt.subplots()
fig.set_size_inches(8, 5)

# we create the regression line through seaborn
sns.regplot(x='price', y='rating', data=df,
            fit_reg= True, color='b', dropna=True, line_kws={'color':'red'})

#%% md

Even with this graph, we can see that the regression line is quite flat. This means there isn't a strong correlation between users' rating and price: our prediction is wrong according to these datasets.

#%% md

## Question N.4
### Do ratings, popularity and prices depend on applications' size?
<i> **(Beatrice Sibilia)** </i>

#%%

def linear_regression(x, y):
    N = len(x)
    x_mean = x.mean()
    y_mean = y.mean()

    slope_num = ((x - x_mean) * (y - y_mean)).sum()
    slope_den = ((x - x_mean)**2).sum()
    slope = slope_num / slope_den

    intercept = y_mean - (slope*x_mean)

    reg_line = 'y = {} + {}x'.format(round(intercept,3), round(slope,3))
#The format() method formats the specified value(s) and insert them inside the string's placeholder ( {} )
#The round() function returns a floating point number that is a rounded version of the specified number, with the specified number of decimals.

    return (intercept, slope, reg_line)

#%%

def corr_coef(x, y):
    N = len(x)

    num = (N * (x*y).sum()) - (x.sum() * y.sum())
    den = np.sqrt((N * (x**2).sum() - x.sum()**2) * (N * (y**2).sum() - y.sum()**2))
    r = num / den
    return r

#%%

#SIZE AND PRICE

x=alldata["size (MB)"]
y=alldata['price']

intercept, slope, reg_line = linear_regression(x, y)
print('Regression Line: ', reg_line)
r = corr_coef(x, y)
print('Correlation Coef.: ', round(r,3))
print('"Goodness of Fit": ', round(r**2,3))

fig, ax = plt.subplots()
fig.set_size_inches(8, 5)
sns.regplot(x=x, y=y, data= alldata,
            fit_reg= True, color='b', dropna=True, line_kws={'color':'red'})


#%%

data60 = alldata[alldata.price < 60]
x=data60["size (MB)"]
y=data60['price']

intercept, slope, reg_line = linear_regression(x, y)
print('Regression Line: ', reg_line)
r = corr_coef(x, y)
print('Correlation Coef.: ', round(r,3))
print('"Goodness of Fit": ', round(r**2,3))

fig, ax = plt.subplots()
fig.set_size_inches(8, 5)
# we create the regression line through seaborn
sns.regplot(x=x, y=y, data= data60,
            fit_reg= True, color='b', dropna=True, line_kws={'color':'red'})

#%%

#SIZE AND INTERACTIONS

x=alldata["size (MB)"]
y=alldata['interactions']

intercept, slope, reg_line = linear_regression(x, y)
print('Regression Line: ', reg_line)
r = corr_coef(x, y)
print('Correlation Coef.: ', round(r,3))
print('"Goodness of Fit": ', round(r**2,3))

fig, ax = plt.subplots()
fig.set_size_inches(8, 5)
# we create the regression line through seaborn
sns.regplot(x=x, y=y, data= alldata,
            fit_reg= True, color='magenta', dropna=True, line_kws={'color':'blue'})

#%%

#SIZE AND RATING

x=alldata["size (MB)"]
y=alldata['rating']

intercept, slope, reg_line = linear_regression(x, y)
print('Regression Line: ', reg_line)
r = corr_coef(x, y)
print('Correlation Coef.: ', round(r,3))
print('"Goodness of Fit": ', round(r**2,3))

fig, ax = plt.subplots()
fig.set_size_inches(8, 5)
# we create the regression line through seaborn
sns.regplot(x=x, y=y, data= alldata,
            fit_reg= True, color='g', dropna=True, line_kws={'color':'orange'})

#%% md

## Question 5
### Do most popular Apps have some characteristics in common?
<i>**(Giammarco Bozzelli</i> and <i>Marco Cavaliere)**</i>

First we need to find which are the most successful applications; to do so we sort the dataframe by the
**_'rating'_** and **_'interactions'_** columns.
#%%
alldata.sort_values(by = ['rating','interactions'], ascending = False, inplace = True)
alldata.head(10)
#%% md
We now drop each row with NaN values in the
**_'size (MB)'_** column so that we will have no problem plotting the graphs and select the first 50 apps.

#%%
frame = alldata.drop(alldata[(alldata['size (MB)'] == 0)].index)
top_50 = frame.iloc[:50,:]
top_50.head(10)

#%%

category_dic = app.dictionary_top(top_50,'category')
app.top_50_catplot(category_dic)


#%%

app.top_50_sizeplot(top_50)

#%%

#remove the 5 applications with largest size
for i in range(7):
    top_50.drop(top_50['size (MB)'].idxmax(), inplace = True)

#%%

app.top_50_sizeplot(top_50)

#%%

#trovare mean e standard deviation del grafico
print('Mean =',top_50['size (MB)'].mean())
print('Standard Deviation =',top_50['size (MB)'].std())
#conviene fare un applicazione di max 78 + 48 MB

#%%

#PRICE - Free
price_top = frame.iloc[:50,:]
price_dic = app.dictionary_top(price_top,'price')  # getting all category types
price_dic

#%%

app.top_50_priceplot(price_dic)

#%%

#Price - Big money
price_top = frame.iloc[:100,:]
price_top = price_top.drop(price_top[(price_top['price'] == 0.0)].index)
price_dic = app.dictionary_top(price_top,'price')
price_dic

#%%

app.top_50_priceplot(price_dic)


#%%

#STORE
#Which Appstore is more frequent in the top 50
store_top = frame.iloc[:50,:]
store_dic = app.dictionary_top(store_top,'store')
store_dic

#%%

#plot a pie chart
plt.figure(figsize = (6,6))
plt.pie(list(store_dic.values()),labels = list(store_dic.keys()), textprops={'fontsize': 15})

#%%

#let's now put together all the most common characteristics to find apps that them them all
top_50 = top_50[top_50['category'] == 'Games']
top_50 = top_50.loc[(top_50['size (MB)'] <= 105.320389392)]
top_50 = top_50.loc[top_50['price'] == 0]
top_50 = top_50.loc[top_50['store'] == 'playstore']

top_50

#%% md

Observing this table we see that interactions are not that high...
We know try to sort apps first by 'interaction'

#%%

alldata.sort_values(by = ['interactions','rating'], ascending = False, inplace = True)
a = alldata.drop(alldata[(alldata['size (MB)'] == 0)].index)#to select the first 50 popular apps
top_interactions = a.iloc[:50,:]
top_interactions.head(10)

#%% md

As we can see now the top applications have changed.

#%%

category_dic = app.dictionary_top(top_interactions,'category')
app.top_50_catplot(category_dic)

#%%

app.top_50_sizeplot(top_interactions)

#%%

print('Mean =',top_interactions['size (MB)'].mean())
print('Standard Deviation =',top_interactions['size (MB)'].std())

#%%

price_top = a.iloc[:50,:]
price_dic = app.dictionary_top(price_top,'price')
price_dic

#%% md

As we can see now there is only one price for the apps in the top 50. This is something they have in common.

#%%

#Which Appstore is more frequent in the top 50
store_top = a.iloc[:50,:]
store_dic = app.dictionary_top(store_top,'store')
store_dic

#%% md

All Applications also come from the same store: **Playstore**

#%%

#let's now put together all the most common characteristics to find apps that them them all
top_interactions = top_interactions[top_interactions['category'] == 'Games']
top_interactions = top_interactions.loc[(top_interactions['size (MB)'] >= 20.463256986) & (top_interactions['size (MB)'] <= 105.72074301)]
top_interactions
