# ==============================================================================
# 📖 BIGNAMI SUI SET (INSIEMI) PER L'ESAME DI PYTHON/NETWORKX
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. CREAZIONE
# ------------------------------------------------------------------------------
# Crea un Set vuoto (Attenzione: NON usare {}, quello crea un dizionario vuoto!)
nodi_visitati = set()

# Creare un Set partendo da una lista (Elimina i doppioni istantaneamente!)
lista_con_doppioni = [1, 2, 2, 3, 3, 3, 4]
set_pulito = set(lista_con_doppioni)  # Risultato: {1, 2, 3, 4}

# ------------------------------------------------------------------------------
# 2. AGGIUNGERE E RIMUOVERE
# ------------------------------------------------------------------------------
# Aggiungere un elemento
# nodi_visitati.add(nodo_partenza)

# Rimuovere un elemento
# nodi_visitati.remove(nodo_partenza) # Crasha se non c'è
# nodi_visitati.discard(nodo_partenza) # Sicuro: non crasha se non c'è

# ------------------------------------------------------------------------------
# 3. CONTROLLARE L'ESISTENZA (Estremamente Veloce!)
# ------------------------------------------------------------------------------
# if nodo_corrente in nodi_visitati:
#     print("Ci sono già passato, evito il ciclo infinito!")

# ==============================================================================
# 🎯 SCENARIO TIPICO DELL'ESAME (RICERCA RICORSIVA / DFS)
# ==============================================================================
# Quando la traccia chiede: "Trova tutti i nodi raggiungibili partendo da A"

"""
def trova_raggiungibili(self, nodo_partenza):
    visitati = set()           # Uso il set per i nodi già visti
    da_visitare = [nodo_partenza] # Uso la lista come "coda" delle cose da fare

    while len(da_visitare) > 0:
        nodo_corrente = da_visitare.pop(0) # Prendo il primo elemento

        if nodo_corrente not in visitati:
            visitati.add(nodo_corrente)    # Lo segno come visitato

            # Prendo i vicini dal grafo e li aggiungo alle cose da fare
            vicini = self.grafo.neighbors(nodo_corrente)
            da_visitare.extend(vicini)

    return list(visitati) # Alla fine, converto il set in lista per restituirlo
"""