# SG-Library
![cooltext434012326534274](https://user-images.githubusercontent.com/26288496/233116778-228c7070-2ec7-464f-bd70-9fcd04125d16.png)



Concept di un algoritmo di predizione delle preferenze basato su K-Means, inserito nel contesto di un e-commerce di Libri.


## SCOPO DEL SISTEMA

L’obiettivo è quello di realizzare un algoritmo suggeritore per gli utenti di una piattaforma e-commerce di
libri. L’algoritmo si occupa di realizzare una lista di suggerimenti per gli acquisti futuri, attraverso un
modulo di intelligenza artificiale, capace di apprendere le preferenze degli utenti in funzione delle loro
interazioni con i prodotti della piattaforma.
Lo scopo del sistema è quello di comprendere come determinare l’insieme di libri da consigliare all’utente,
elaborando le informazioni degli ordini effettuati dallo stesso. Volendo generalizzare: se un utente è solito
acquistare libri di un certo autore/genere/categoria, l’algoritmo dovrà apprendere le sue preferenze e
suggerirgli i libri che più si avvicinano ad esse.

## DEFINIZIONE DATASET

Considerando che gli algoritmi di apprendimento si basano sui dati, ci siamo concentrati su di essi sin dalle
prime fasi dello sviluppo, inizialmente individuando due possibili approcci alla realizzazione:

· utilizzare dataset di grandi dimensioni reperiti online;

· utilizzare un dataset ridotto creato su misura per l’e-commerce.

Analizzando l’eventualità del primo approccio ne abbiamo subito notato l’estrema inefficacia, in quanto
analizzando il dataset vi erano molti valori nulli, e l’eliminazione dei datapoint incompleti ne riduceva le
dimensioni di circa il 10%, caratterizzando dunque una pessima qualità dei dati. Altra questione da
prendere in seria considerazione, è quella della suddivisione dei libri in categorie non sempre rilevanti, in
quanto la maggior parte delle categorie individuate avevano cardinalità compresa tra 1 e 5 libri ciascuna; è
dunque subito evidente come su un dataset di considerevoli dimensioni, una informazione come la
categoria non sia di fatto utilizzabile data la sua scarsa efficacia.

In seguito a questa attenta analisi si è deciso di procedere con il secondo approccio, e dunque di realizzare
da zero un dataset ad-hoc per la piattaforma, composto da:

· ISBN (intero)

· Titolo (stringa)

· Autore (stringa)

· Editore (stringa)

· Prezzo (float)

· Anno di pubblicazione (intero)

· Categoria (stringa)

· Basato su storia vera (booleano)

· Edizione illustrata (booleano)

· Appartenente a una saga (booleano)

· Numero pagine (intero)

Per la realizzazione del dataset abbiamo utilizzato uno script Python “create_dataset.py” che, dopo aver
importato il file .csv (libri) frutto di un dump del database di sistema (query SQL) è stato ottimizzato,
eliminando le colonne non rilevati (titolo, descrizione) al fine dell’operazione. Successivamente, applicando
una tecnica di scaling (scaler), abbiamo sostituito tutti i dati testuali in numeri interi al fine di migliorare le
prestazioni di processabilità dell’algoritmo.Conclusivamente per dettagliare al meglio i suggerimenti per l’utente, si è scelto di aggiungere le seguenti
informazioni relative al:

· numero di recensioni positive ricevute dal sistema (intero),

· numero di acquisti avvenuti nel sistema (intero);

(Informazioni contenute nel file user*_dataset.txt)

Nell’ambito dei dati utenti è stato eseguito un dump dal DB (query SQL), degli ISBN dei libri con i quali
l’utente ha interagito, per scopi dimostrativi ne è stato simulato il funzionamento con l’inserimento di
quattro utenti fittizi, creati ad-hoc per testare ogni funzionalità dell’algoritmo. I dati dei singoli utenti sono
contenuti nei file del tipo _user_X.txt_. Nello script create_dataset.py si è inserita una colonna al dataset
precedentemente ottenuto contenente un booleano, vero se l’utente inserito in input ha interagito con un
determinato titolo, falso altrimenti, i risultati sono invece contenuti nel file user_X_dataset.txt.
Lo script ha inoltre il compito di generare il file ISBN_index.txt, che associa ogni ISBN all’indice del dataset
risultante, e verrà utilizzato per ricostruire le informazioni relative al titolo e l’autore.

## SCELTA DELL’ALGORITMO

Per quanto riguarda la scelta dell’algoritmo di apprendimento sono stati presi in considerazione sia gli
algoritmi di apprendimento supervisionato(classificazione), che gli algoritmi di apprendimento non
supervisionato(clustering). Alla fine si è scelto di utilizzare un algoritmo di clustering, dal momento che la
struttura dei dati sarebbe stata difficilmente gestibile da un algoritmo di classificazione per via di una
mancata definizione chiara delle etichette. Il clustering permette dunque di raggruppare i singoli datapoint
in insiemi di elementi simili in base a dei pattern ritrovati nei dati. Un’ipotesi di come consigliare una lista di
libri in output all’utente è quello di selezionare il cluster contenente il maggior numero di libri con cui
l’utente ha già interagito. L’algoritmo di base da cui si è pensato di iniziare è il k-means. Per poter operare
su un qualsiasi algoritmo di clustering bisogna scalare le features più grandi che possono avere più peso
rispetto ad altre più piccole ma più rilevanti. Per scalare i dati è stato utilizzato il package
sklearn.preprocessing. Il metodo di scaling utilizzato è lo StandardScaler(). Esso è un metodo di
standardizzazione delle feature che si ottiene rimuovendo la media e dividendo per la deviazione standard.
Questo serve per ridistribuire i dati in una distribuzione normale standardizzata. Si è utilizzata la PCA, ossia
l’analisi delle componenti principali, che permette di ridurre le dimensioni del dataset, cercando un nuovo
insieme di variabili con dimensione minore ma senza perdere il contenuto informativo del dataset iniziale.
L’implementazione di questo metodo è stata effettuata utilizzando il package sklearn.decomposition. Il k-
means, dal package sklearn.cluster, ha come problema la scelta del numero iniziale dei cluster. Per questo
motivo sono state effettuate varie prove per trovare il k più adatto, e si è cercato di analizzare quanto una
diversa inizializzazione dei centroidi potesse influire sulla scelta dei dati. Per stimare la qualità dei cluster
risultanti abbiamo utilizzato le seguenti metriche di valutazione:

- silhouette coefficient
- ARI (Adjusted Rand Index)

Il numero di cluster risultante il migliore nella maggior parte dei casi è compreso tra 2 e 3, quindi la
versione finale ha k = 3.

![Immagine 2023-04-19 172323](https://user-images.githubusercontent.com/26288496/233123575-061248b8-d541-4feb-a568-624b07134c29.png)

Questo tipo di grafico mostra l’andamento delle due metriche scelte precedentemente in base al numero di
cluster. Il primo, che rappresenta il Silhouette Coefficient, decresce linearmente poiché dipende dalla
distanza tra i datapoint. La seconda, ossia la ARI, non migliora significativamente al crescere dei cluster; ciò
significa che dal primo risulta essere il k migliore il numero 2 mentre il secondo dà un piccolo
miglioramento (seppur impercettibile) con il valore 3. Come si evince anche dal grafico, la purezza dei
cluster non è eccellente, dal momento che questi numeri dovrebbero tendere a 1. Purtroppo, questo è
dovuto alla piccola quantità di dati su cui è stato testato l’algoritmo, il quale con altre accortezze potrebbe
essere sicuramente migliore. Il progetto, infatti, si presta molto all’espansione per via della struttura
tramite pipeline e della semplicità di utilizzo degli algoritmi già implementati in sklearn.

# CONSIDERAZIONI FINALI

Allo stato attuale, il livello di sviluppo generale del progetto è ancora in stato embrionale e lascia un ampio
margine per futuri miglioramenti ed un considerevole ingrandimento della base dati.



