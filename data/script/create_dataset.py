import pandas as pd 
import numpy as np

UTENTE = "../user_4.txt"
DATASET_FINALE = "../user_dataset_4.txt"

#leggo il file scaricato dal database di dodo.net
df = pd.read_csv("../libri.csv")
#tengo traccia a quale isbn si riferisce l'index
df.ISBN.to_csv(path_or_buf="../ISBN_index.txt",header=None)
#elimino le colonne che non ci interessano
df.drop(columns={"ISBN","Titolo"}, inplace=True)

df_ISBN = pd.read_csv("../ISBN_index.txt",header=None, index_col=0)
df_ISBN.rename(columns={1:"ISBN"}, inplace=True)

#creo il dizionario per gli autori
autori_list = df.Autore.unique().tolist()
num_list = []
for i in range(0, len(autori_list)):
    num_list.append(i)
autori_dict = dict(zip(autori_list, num_list))

#creo il dizionario per le categorie
categorie_list = df.Nome_Categoria.unique().tolist()
num_list = []
for i in range(0, len(categorie_list)):
    num_list.append(i)
categorie_dict = dict(zip(categorie_list, num_list))

#creo il dizionario per gli editori
editori_list = df.Editore.unique().tolist()
num_list = []
for i in range(0, len(editori_list)):
    num_list.append(i)
editori_dict = dict(zip(editori_list, num_list))

#replace
df.replace(to_replace=editori_dict, inplace=True)
df.replace(to_replace=autori_dict, inplace=True)
df.replace(to_replace=categorie_dict, inplace=True)

#dichiaro quali sono le nuove categorie
new_columns = "num_mi_piace", "num_acquisti"
for i in new_columns:
    df[i] = 0

#inserisco valori casuali
df.num_mi_piace = np.random.randint(0, 20, df.shape[0])
df.num_acquisti = np.random.randint(0, 50, df.shape[0])

user_df = pd.read_csv(UTENTE, header=None)
user_df.rename(columns={0:"ISBN"}, inplace=True)
user_df['recommended'] = 1

result = pd.merge(df_ISBN, user_df, how="outer", on=["ISBN", "ISBN"])
result.fillna(0,inplace=True)
result.recommended = result.recommended.astype('int32')

df = df.join(result)
df.drop(columns="ISBN",inplace=True)

df.to_csv(path_or_buf=DATASET_FINALE,header=None)