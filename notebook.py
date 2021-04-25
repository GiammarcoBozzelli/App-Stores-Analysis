
'''
#%%
#Alternative Version using appstore.py as module
import csv
import json
import numpy as np
import pandas as pd
import os.path
import appstore as app

#%%
app.bar_chart(app.top_categories('playstore.csv'))

#%%
app.bar_chart(app.top_categories('windows_store.csv'))

#%%
app.bar_chart(app.top_categories('AppleStore.csv'))'''

#%%
#Present Version
import csv
import numpy as np
import pandas as pd
import os
import os.path
#%%
#PLAYSTORE -> Giammarco
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

#%%
#MICROSOFT STORE -> Marco
frame2 = pd.read_csv(os.path.join(os.getcwd(), 'windows_store.csv')) #open as DataFrame the file
print(frame2.columns) #checking all columns' labels
windowstore = frame.loc[:, ['name', 'category', 'rating', 'reviews' ]]
windowstore.info()

#%%
print('\n Number of NaN values in each column \n', windowstore.isna().sum()) #number of cells with NAN values per each column
windowstore.dropna(axis=0, how='any', inplace = True) #deleting all rows with at least one NaN
windowstore.info()
#%%

#add a column ['weighted_rating'] that will be useful in dentifying a more precise mean rating per each category
windowstore['reviews'] = np.int64(windowstore['reviews'].str.replace(',',''))
windowstore.loc[:,'weighted_rating'] = windowstore['rating'] * windowstore['reviews']
windowstore

#%%
#Calculating the actual rating for each category
categories = set(windowstore['category'].tolist()) #getting all category types
category_rating_dic2 = {} #dict to contain the rating for each category type
for category in categories: #filling the dictionary
    cat = windowstore.loc[windowstore['category'] == category] #choosing the single category
    rating = cat['weighted_rating'].sum() / cat['reviews'].sum() #calculating the rating wrt n. of installs
    category_rating_dic2[category] = rating #adding the new key:value to the dictionary
print(category_rating_dic2)
#%%

# making a bar char with the top 5 categories
import matplotlib.pyplot as plt
d = sorted(category_rating_dic2.items(), key=lambda xy:xy[1], reverse = True)[:6]
plt.bar([x[0] for x in d], [x[1] for x in d],log = True) # use log = True to make the graph more evident
plt.show()

#%%
#%%
#APPSTORE
frame3 = pd.read_csv(os.path.join(os.getcwd(), 'AppleStore.csv')) #open as DataFrame the file
print(frame3.columns) #checking all columns' labels
appstore = frame3.loc[:, ['name', 'category', 'user_rating', 'rating_count_tot' ]]
appstore.info()
#%%
appstore.loc[:,'weighted_rating'] = appstore['user_rating'] * appstore['rating_count_tot']
appstore


#%%

#Calculating the actual rating for each category
categories = set(appstore['category'].tolist()) #getting all category types
category_rating_dic3 = {} #dict to contain the rating for each category type
for category in categories: #filling the dictionary
    cat = appstore.loc[appstore['category'] == category] #choosing the single category
    rating = cat['weighted_rating'].sum() / cat['rating_count_tot'].sum() #calculating the rating wrt n. of installs
    category_rating_dic3[category] = rating #adding the new key:value to the dictionary
print(category_rating_dic3)

#%%

# making a bar char with the top 5 categories
import matplotlib.pyplot as plt
d = sorted(category_rating_dic3.items(), key=lambda xy:xy[1], reverse = True)[:6]
plt.bar([x[0] for x in d], [x[1] for x in d],log = True) # use log = True to make the graph more evident
plt.show()
