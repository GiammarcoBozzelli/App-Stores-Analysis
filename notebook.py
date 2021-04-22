#%%
import csv
import pandas as pd
import os
import os.path

#%%
#Get file 'playstore.csv' and remove all columns not useful in answering the first research question

frame = pd.read_csv(os.path.join( os.getcwd(), 'playstore.csv')) #open as DataFrame the file
print(frame.columns) #checking all columns' labels
frame = frame.drop(columns=['id'])
frame.drop(frame.loc[:,'rate_5_pc':'updated'], inplace = True, axis = 1)
frame.drop(frame.loc[:,'current_version':'in_app_products'], inplace = True, axis = 1)
#frame.info
frame
