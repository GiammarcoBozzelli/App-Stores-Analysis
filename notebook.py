#%%
import csv
import pandas as pd
import os
import os.path

#%%
#Get file 'playstore.csv' and remove all columns not useful in answering the first research question

frame = pd.read_csv(os.path.join( os.getcwd(), 'playstore.csv')) #open as DataFrame the file
frame.columns #checking all columns' labels
playstore = frame.drop(columns=['id']) #removing all columns we do not need
playstore.drop(playstore.loc[:,'rate_5_pc':'updated'], inplace = True, axis = 1)
playstore.drop(playstore.loc[:,'current_version':'in_app_products'], inplace = True, axis = 1)
#playstore.info
playstore

#%%
#group all data per category and visualize how many apps are in each category 
grouped = playstore.groupby('category')#group data by 'category'
print(grouped.agg(np.size)) #print the number of apps per category
