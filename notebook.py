#%%
import csv
import pandas as pd
import os
import os.path

#%%
#Get file 'playstore.csv' and remove all columns not useful in answering the first research question

frame = pd.read_csv(os.path.join( os.getcwd(), 'playstore.csv')) #open as DataFrame the file
frame.columns #checking all columns' labels
playstore = frame.loc[:,['name','category','rating','reviews','price','size','installs']]
playstore.info
#playstore
#%%
#Removing all rows with null values
print('\n Number of NaN values in each column \n', playstore.isna().sum()) #number of cells with NAN values per each column
playstore.dropna(axis=0, how='any', inplace=True) #deleting all rows with at least one NaN
playstore.isna().sum() #checking if there are Nan left
playstore.info()
#%%
#Group all data per category and visualize how many apps are in each category 

grouped = playstore.groupby('category')#group data by 'category'
print(grouped.agg(np.size)['name']) #print the number of apps per category

#%%
#Replace each ',' in the 'installs' column with '' in order to convert it in float64
playstore['installs'] = np.int64(playstore['installs'].str.replace(',',''))
playstore['installs']

#add a column ['weighted_rating'] that will be useful in dentifying a more precise mean rating per each category
playstore.loc[:,'weghted_rating'] = playstore['rating'] * playstore['installs']
playstore
