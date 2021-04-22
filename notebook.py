#%%

import csv
import pandas as pd
import os
import os.path

#%%

print(os.getcwd())
frame = pd.read_csv(os.path.join( os.getcwd(), 'playstore.csv'))
frame = frame.drop(columns=['id'])
frame.drop(frame.loc[:,'rate_5_pc':'updated'], inplace = True, axis = 1)
frame.drop(frame.loc[:,'current_version':'in_app_products'], inplace = True, axis = 1)
#frame.info
frame
