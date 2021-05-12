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

[group-1-project](www.link.com)

#%% md

## Data Loading and Cleaning


#%% md
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

alldata
pie = app.pie_chart(alldata)

#%% md

<h2> Question N.1 <h2>

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

print(app.top_categories_weighted(alldata,'microsoft_store'))

mccateg_dict=app.top_categories_weighted(alldata,'microsoft_store')

app.grafic_rating(mccateg_dict)

#%% md

<h2>Research Question 2</h2>
<p><Which category are the most expensive for the users?<br>

1) For each app with same category we compute the price mean<p>
2) Then we represent it graphically <p>

#%%

#Creating a copy to work safely
df = alldata.copy()

#Selecting the essential columns for our research question
df = df[['category', 'price','store']]
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
price_mean_dict= {}
for x in category_list:
    a = df[df['category']==x]
    price_mean_dict[x]=a['price'].mean()

price_mean_dict


#%%

#Visualising the dictionary in a dataframe

df_mean_price = pd.Series(price_mean_dict).rename_axis('category').reset_index(name='mean price')
df_mean_price

#%%

#sorting values in ascending order
df_mean_price.sort_values(by=['mean price'], inplace=True, ascending = False)
df_mean_price

#%% md

As we can clearly see from the data, the categories: Education and Tool & Utilities are the ones with highest prices.

#%% md

<h4>Graphical representation </h4>

- We are now going to display the results trough a bar chart


#%%

df_mean_price.plot.barh(x='category', y='mean price', rot=0, color=['orange','blue'])

#%% md

<h4> Conclusion <h4>

#%% md

The categories below are the most expensive among all stores
- Education
- tools & Utilities
- Health & Fitness

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

# Import matplotlib and seaborn libraries to visualize the data

data = alldata.drop(alldata[(alldata['price'] >= 60)].index)
#alldata=sns.load_dataset(alldata)
g = sns.regplot(x="size (MB)", y="price",data=alldata, color="g")
g= sns.jointplot(x="size (MB)", y="price",data=alldata, kind="reg")
regline = g.ax_joint.get_lines()[0]
regline.set_color("red")

#%%

# Using pairplot we'll visualize the data for correlation
sns.pairplot(data, x_vars="size (MB)",
             y_vars="price", size=4, aspect=1, kind='scatter')
plt.show()

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

#%%
