**appstore_icdm2**
# App stores analysis :smiley:
Databases:
[Appstore_coding - Google Drive](https://drive.google.com/drive/folders/1WpJfuIUlIh2z5hbM_b9GL8sOLfwKgE_n?usp=sharing)

- [ ] Which App Category do users prefer? Does it change between different stores?
- [ ] For which App Category are users willing to pay more?
- [ ] Does users’ rating depend on price?
- [ ] Does users’ rating depend on price?
- [ ] Do most popular apps have some characteristics in common?


  
## Question n. 1
### Which App Category do users prefer?

categoria preferita ->per le categorie, i rating più alti
Selezionare le categorie, per app nella categoria fare la media dei ratings. Ordinare i valori dal più alto al più basso in relazione alla categoria

Dizionari per diverso store:
key = ‘Categoria’, 
values =[(rating,n°reviews),(rating,n°reviews),(rating,n°reviews),(rating,n°reviews)...]
Media ponderata (in base al n°reviews) per rating, sostituendo list of tuples con media ponderata.

Problema: fare le tuples!
Una volta pronte basta sostituire i valori e otteniamo i risultati.
Confrontare i risultati in base agli stores
### Does it change between different stores?


##Question n. 2
###For which App Category are users willing to pay more?

Stessa risoluzione del punto 1 con:
-dati relativi soltanto alle applicazioni a pagamento (escludere app gratis)
-unire i risultati ottenuti dai vari dataset per ottenere un valore definitivo in base alla CATEGORIA 

Problema: alcuni dataset presentano valute diverse -> convertire tutto sotto la stessa valuta.

## Question n. 3
### Does users’ rating depend on price?

Unione tra risposta alla domanda 1 e domanda 2.
Prima di determinare l'effettiva risposta ci aspettiamo che il grafico sia una funzione che vada verso l’alto (più spendo, meglio valuto l’app)
Una volta risolta la domanda vediamo se il pronostico è corretto o no.


                                                              ?


## Question n. 4
### Does users’ rating depend on price?

## Question n. 5
### Do most popular apps have some characteristics in common?

Bel problema





