# ==============================================================================
# 📖 BIGNAMI SUI DIZIONARI (MAPPE) PER L'ESAME DI PYTHON/NETWORKX
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. CREAZIONE
# ------------------------------------------------------------------------------
# Crea un dizionario vuoto (Da fare sempre nel __init__ o all'inizio di build_graph)
mappa_nodi = {}

# ------------------------------------------------------------------------------
# 2. AGGIUNGERE O MODIFICARE
# ------------------------------------------------------------------------------
# Sintassi: dizionario[CHIAVE_UNIVOCA] = VALORE_OGGETTO
# Se la chiave non esiste, viene creata. Se esiste, il valore viene sovrascritto.
# Esempio: mappa_nodi[nodo.ID] = nodo

# ------------------------------------------------------------------------------
# 3. ACCEDERE AI DATI (LETTURA)
# ------------------------------------------------------------------------------
# METODO A: Diretto (ATTENZIONE: Crasha con KeyError se la chiave non esiste)
# nodo_estratto = mappa_nodi[115]

# METODO B: Sicuro tramite .get() (Restituisce None se la chiave non esiste)
# nodo_estratto_sicuro = mappa_nodi.get(115, None)

# ------------------------------------------------------------------------------
# 4. CONTROLLARE L'ESISTENZA (IL FILTRO SALVA-ESAME)
# ------------------------------------------------------------------------------
# Operazione ISTANTANEA, fondamentale per verificare se i nodi dell'arco esistono.
# if arco.ID in mappa_nodi:
#     print("Il nodo è valido e presente nel dizionario!")

# ------------------------------------------------------------------------------
# 5. I TRE MODI PER ITERARE (CICLI FOR)
# ------------------------------------------------------------------------------
# MODO 1: Solo sulle Chiavi
# for chiave_id in mappa_nodi:
#     pass

# MODO 2: Solo sui Valori (Ideale per aggiungere i nodi al grafo in blocco)
# self.grafo.add_nodes_from(mappa_nodi.values())

# MODO 3: Su Chiavi e Valori contemporaneamente
# for chiave, oggetto in mappa_nodi.items():
#     pass

# ==============================================================================
# 🎯 I 3 SCENARI TIPICI DELL'ESAME (QUANDO USARLI)
# ==============================================================================

# ---> SCENARIO A: Filtrare e collegare gli archi nel Model
"""
for arco in archi_grezzi:
    # 1. Controllo se ENTRAMBI gli ID dell'arco sono nelle chiavi del dizionario
    if arco.ID in self.mappa_nodi and arco.ID2 in self.mappa_nodi:

        # 2. Uso l'ID come chiave per pescare l'oggetto intero
        n1 = self.mappa_nodi[arco.ID]
        n2 = self.mappa_nodi[arco.ID2]

        # 3. Aggiungo l'arco usando gli oggetti veri e propri
        self.grafo.add_edge(n1, n2, weight=arco.PESO)
"""

# ---> SCENARIO B: Leggere i pesi degli archi da NetworkX
"""
# NetworkX salva gli attributi dell'arco (come il peso) in un dizionario chiamato 'data'
for nodo_partenza, nodo_arrivo, data in self.grafo.edges(data=True):
    # Estraggo il peso usando la chiave testuale
    peso_arco = data['weight'] 
"""

# ---> SCENARIO C: Mappare i risultati del Database nel DAO
"""
# Con cursor(dictionary=True), ogni riga SQL (row) diventa un dizionario
for row in cursor:
    nodo = Airport(
        ID=row["ORIGIN_AIRPORT_ID"], # Uso il nome della colonna SQL come chiave
        AIRPORT=row["AIRPORT_NAME"]
    )
"""