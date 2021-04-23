#%%

import csv
import numpy as np
import pandas
import pandas as pd
import os
import os.path

#%%

frame = pd.read_csv(os.path.join( os.getcwd(), 'playstore.csv')) #open as DataFrame the file
print(frame.columns) #checking all columns' labels
playstore = frame.loc[:, ['name', 'category', 'rating', 'installs' ]]
playstore.info()


#%%

print('\n Number of NaN values in each column \n', playstore.isna().sum()) #number of cells with NAN values per each column
playstore.dropna(axis=0, how='any', inplace=True) #deleting all rows with at least one NaN
playstore.info()

#%%
#Replace each ',' in the 'installs' column with '' in order to convert it in float64
playstore['installs'] = np.int64(playstore['installs'].str.replace(',',''))
playstore['installs']

#add a column ['weighted_rating'] that will be useful in dentifying a more precise mean rating per each category
playstore.loc[:,'weighted_rating'] = playstore['rating'] * playstore['installs']
playstore


#%%
#Calculating the actual rating for each category
categories = set(playstore['category'].tolist()) #getting all category types
category_rating_dic = {} #dict to contain the rating for each category type
for category in categories: #filling the dictionary
    cat = playstore.loc[playstore['category'] == category] #choosing the single category
    rating = cat['weighted_rating'].sum() / cat['installs'].sum() #calculating the rating wrt n. of installs
    category_rating_dic[category] = rating #adding the new key:value to the dictionary
print(category_rating_dic)

#%%
# making a bar char with the top 5 categories
import matplotlib.pyplot as plt
d = sorted(category_rating_dic.items(), key=lambda xy:xy[1], reverse = True)[:6]
plt.bar([x[0] for x in d], [x[1] for x in d],log = True) # use log = True to make the graph more evident
plt.show()
