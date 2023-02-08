import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans

def find_cluster_max():
    group_by_cluster = data.groupby(by="cluster").sum()
    return group_by_cluster[12].idxmax()


N_CLUSTERS = 3
DATASET = "./data/user_dataset_3.txt"
RISULTATI_UTENTE = "./data/result_user_3.txt"

data = pd.read_csv(DATASET,header=None)
features = data
labels = data[12]

preprocessor = Pipeline(
    [
        ("scaler", StandardScaler()),
        ("pca", PCA(n_components=2, random_state=4)),
    ]
)

clusterer = Pipeline(
   [
       (
           "kmeans",
           KMeans(
               n_clusters=N_CLUSTERS,
               init="random",
               n_init=50,
               max_iter=300,
               random_state=0,
           ),
       ),
   ]
)

pipe = Pipeline(
    [
        ("preprocessor", preprocessor),
        ("clusterer", clusterer)
    ]
)

pipe.fit(features)
## fine pipeline

preprocessed_data = pipe["preprocessor"].transform(features)
predicted_labels = pipe["clusterer"]["kmeans"].labels_



###solo per la stampa
pcadf = pd.DataFrame(
    pipe["preprocessor"].transform(features),
    columns=["component_1", "component_2"],
)
pcadf["predicted_cluster"] = pipe["clusterer"]["kmeans"].labels_
pcadf["true_label"] = labels

result = data
result['cluster'] = pcadf["predicted_cluster"]

cluster_max = result[result['cluster'] == find_cluster_max()]

libri = pd.read_csv('./data/libri.csv')
consigli = libri[libri.index.isin(cluster_max.index)]

consigli = consigli.join(result)
consigli = consigli[consigli[12] == 0]

consigli.ISBN.to_csv(RISULTATI_UTENTE, header=None)
print(consigli.Titolo)