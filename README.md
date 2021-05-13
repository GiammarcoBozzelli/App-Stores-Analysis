**appstore_icdm2**
# App stores analysis :smiley:
Databases:
[Appstore_coding - Google Drive](https://drive.google.com/drive/folders/1WpJfuIUlIh2z5hbM_b9GL8sOLfwKgE_n?usp=sharing)
___

- [x] Which App Category do users prefer? Does it change between different stores?
- [x] For which App Category are users willing to pay more?
- [x] Does users’ rating depend on price?
- [x] Do ratings, popularity and prices depend on applications' size?
- [x#module with all functions we need

import pandas as pd
import numpy as np
import os.path
import matplotlib.pyplot as plt

def top_categories_weighted(data,store_type = None): #Giammarco
    frame = data.copy()
    frame['interactions'].dropna(inplace = True)#remove all rows in 'interaction' and 'rating' column with NaN values
    frame['rating'].dropna(inplace = True)
    frame['weighted_rating'] = frame['interactions'] * frame['rating'] # multiply the rating * number of interaction

    if store_type is None: #check whether the store type was passed as a variable or not
        pass
    else:
        frame = frame[frame['store'] == store_type] #select only the rows with the store type that was called

    frame = frame[frame['category'].notnull()] #get only the rows with non- NaN values
    categories = set(frame['category'].tolist())  # getting all category types without repetitions
    category_rating_dic = {} # dict to contain the rating for each category type

    for category in categories:  # filling the dictionary
        cat = frame.loc[frame['category'] == category]  # creating a frame by choosing the single category
        rating = cat['weighted_rating'].sum() / cat['interactions'].sum() #calculating the weighted rating for the category
        category_rating_dic[category] = rating  # adding the new key:value to the dictionary

    print ('The highest rated category is: ',max(category_rating_dic, key=lambda k: category_rating_dic[k]))
    return (category_rating_dic)

def pie_chart(data,store_type = None): #Giammarco
    frame = data.copy()
    if store_type is None: #check whether the store type was passed as a variable or not
        pass
    else:
        frame = frame[frame['store'] == store_type] #select only the rows with the store type that was called

    frame = frame[frame['category'].notnull()] #get only the rows with non- NaN values
    categories = frame['category'].tolist()# getting a list with categories
    category_dic = {} # dict to contain the rating for each category type
    for category in categories:  # filling the dictionary
        if category not in category_dic:
            category_dic[category] = 1
        else:
            category_dic[category] += 1# adding the new key:value to the dictionary

    plt.figure(figsize = (8,8))
    plt.pie(list(category_dic.values()), labels=list(category_dic.keys()),rotatelabels = 30 ,
            autopct='%1.1f%%', explode = (0.1,0,0,0,0,0,0,0,0,0,0,0,0), textprops={'fontsize': 12})

    return (category_dic)

def grafic_rating(dict): #Marco
    categories = dict.keys()
    ratings = dict.values()
    y_pos = np.arange(len(categories))

    plt.figure(figsize = (8,6))
    plt.barh(y_pos, ratings, align='center', alpha=0.5, log=True, ) #add log = True to make the graph clearer
    plt.yticks(y_pos, categories)
    plt.xlabel('Rating', fontsize = 12)
    plt.ylabel('Categories', fontsize = 12)
    plt.title('Statistic correlation between rating and category', fontsize = 15)
    plt.show()
    return

def dictionary_top(frame, column): #Marco
    list = (frame[column].tolist())  # getting all category types
    dic = {}  # dict to contain the number of apps for each category type
    for e in list:  # filling the dictionary
        if e not in dic:
            dic[e] = 1
        else:
            dic[e] += 1
    return (dic)


] Do most popular apps have some characteristics in common?

## ⚠️ What to do? ⚠️
- Do **not** modify the notebook.py file directly
- Copy the content of notebook.py in a new notebook in PyCharm and work from there
- Remember to rename the file with extension '.ipynb' before opening it
- Modify the notebook in GitHub **only** when things work in PyCharm
- Remember to comment the lines of code (this will help for the exam)

___
  
## Question n. 1
### Which App Category do users prefer?

categoria preferita ->per le categorie, i rating più alti
Selezionare le categorie, per app nella categoria fare la media dei ratings. Ordinare i valori dal più alto al più basso in relazione alla categoria

groupby(*category*) -> all apps grouped by category
Media ponderata (in base al n°reviews) per rating, sostituendo list of tuples con media ponderata.

Confrontare i risultati in base agli stores
### Does it change between different stores?

___
## Question n. 2
### For which App Category are users willing to pay more?

Stessa risoluzione del punto 1 con:
-dati relativi soltanto alle applicazioni a pagamento (escludere app gratis)
-unire i risultati ottenuti dai vari dataset per ottenere un valore definitivo in base alla CATEGORIA 

Problema: alcuni dataset presentano valute diverse -> convertire tutto sotto la stessa valuta.
___
## Question n. 3
### Does users’ rating depend on price?

Unione tra risposta alla domanda 1 e domanda 2.
Prima di determinare l'effettiva risposta ci aspettiamo che il grafico sia una funzione che vada verso l’alto (più spendo, meglio valuto l’app)
Una volta risolta la domanda vediamo se il pronostico è corretto o no.

___
## Question n. 4
### Do ratings, popularity and prices depend on applications' size?

___
## Question n. 5
### Do most popular apps have some characteristics in common?

Bel problema





