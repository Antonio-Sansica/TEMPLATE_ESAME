# ==============================================================================
# 📖 BIGNAMI SULLE LISTE PER L'ESAME DI PYTHON/NETWORKX
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. CREAZIONE E PULIZIA
# ------------------------------------------------------------------------------
# Crea una lista vuota (Usata spessissimo all'inizio dei metodi del DAO)
mia_lista = []

# Svuota completamente una lista esistente (VITALE per resettare la grafica o i percorsi)
# mia_lista.clear()

# ------------------------------------------------------------------------------
# 2. AGGIUNGERE ELEMENTI
# ------------------------------------------------------------------------------
# Aggiunge UN singolo elemento in coda alla lista
# mia_lista.append(oggetto_nodo)

# Aggiunge PIÙ elementi (o un'altra lista) in un colpo solo
# mia_lista.extend([nodo1, nodo2, nodo3])

# ------------------------------------------------------------------------------
# 3. ACCESSO E RICERCA (Attenzione alle differenze coi dizionari!)
# ------------------------------------------------------------------------------
# Accesso tramite INDICE (0 è il primo, -1 è l'ultimo)
# primo_elemento = mia_lista[0]
# ultimo_elemento = mia_lista[-1]

# Tagliare la lista (Slicing) -> Utile per le richieste "Stampa solo i primi 5"
# top_cinque = mia_lista[:5]

# Ricerca (ATTENZIONE: Nelle liste la ricerca è LENTA, evita di usarla per mappare il grafo)
# if oggetto in mia_lista:
#     print("Trovato!")

# ------------------------------------------------------------------------------
# 4. ORDINAMENTO (FONDAMENTALE ALL'ESAME!)
# ------------------------------------------------------------------------------
# Spesso ti chiedono: "Ordina gli aeroporti per numero di voli decrescente"
# Si usa .sort() abbinato a una funzione lambda (x rappresenta il singolo elemento)

# Esempio: Ordinare una lista di oggetti in base al loro attributo PESO (Decrescente)
# mia_lista.sort(key=lambda x: x.PESO, reverse=True)

# Esempio: Ordinare una lista di TUPLE in base al secondo elemento della tupla (indice 1)
# lista_tuple.sort(key=lambda x: x[1], reverse=False) # False = Crescente (default)

# per il return
# return sorted(result, key=len, reverse=True)

# ==============================================================================
# 🎯 I 3 SCENARI TIPICI DELL'ESAME (QUANDO USARLE)
# ==============================================================================

# ---> SCENARIO A: Il "Raccoglitore" nel DAO
"""
def getNodiValidi():
    result = []                  # 1. Creo la lista vuota
    cursor.execute(query)
    for row in cursor:
        nodo = Airport(**row)
        result.append(nodo)      # 2. Aggiungo riga per riga
    return result                # 3. Ritorno la lista piena
"""

# ---> SCENARIO B: Ordinare e stampare una "Top K" nel Model o Controller
"""
# NetworkX mi dà tutti i vicini, io li metto in una lista di tuple (vicino, peso)
lista_vicini = []
for vicino in self.grafo.neighbors(partenza):
    peso = self.grafo[partenza][vicino]['weight']
    lista_vicini.append((vicino, peso))

# La traccia chiede i primi 5 in ordine di peso decrescente
lista_vicini.sort(key=lambda x: x[1], reverse=True)
top_5 = lista_vicini[:5]
"""

# ---> SCENARIO C: Gestione della Grafica (View/Controller in Flet)
"""
# Quando l'utente preme "Crea Grafo", devi pulire lo schermo prima di stampare
self._view.txt_result.controls.clear()  # Pulisce la lista dei testi a schermo

# E poi aggiungi i nuovi risultati
self._view.txt_result.controls.append(ft.Text("Grafo creato!"))
"""

# ------------------------------------------------------------------------------
# 🚨 REGOLA D'ORO DELLE LISTE VS DIZIONARI
# ------------------------------------------------------------------------------
# Usa le LISTE quando l'ordine è importante e devi ORDINARE i dati (.sort).
# Usa i DIZIONARI quando devi CERCARE velocemente un elemento tramite il suo ID.