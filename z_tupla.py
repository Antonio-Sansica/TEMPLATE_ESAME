# ==============================================================================
# 📖 BIGNAMI SULLE TUPLE PER L'ESAME DI PYTHON/NETWORKX
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. CREAZIONE E SPACCHETTAMENTO (UNPACKING)
# ------------------------------------------------------------------------------
# Si creano con le parentesi tonde (o anche senza, separando con virgole)
mio_arco = (115, 200, 45)

# L'UNPACKING (Il trucco più usato): Assegnare la tupla a più variabili in un colpo solo
nodo_partenza, nodo_arrivo, peso = mio_arco

# ------------------------------------------------------------------------------
# 2. RESTITUIRE PIÙ VALORI DA UNA FUNZIONE (Spessissimo nel Model)
# ------------------------------------------------------------------------------
"""
# Nel Model:
def get_dettagli_grafo(self):
    n = self.grafo.number_of_nodes()
    m = self.grafo.number_of_edges()
    return n, m   # Restituisce una tupla implicitamente

# Nel Controller:
nodi, archi = self._model.get_dettagli_grafo() # Spacchetto la tupla
"""

# ==============================================================================
# 🎯 SCENARIO TIPICO DELL'ESAME (GLI ARCHI NEL DAO)
# ==============================================================================

# Invece di usare una @dataclass per l'Arco (se la traccia non lo richiede),
# usa una tupla per essere più veloce e non avere errori di KeyError.

"""
# Nel DAO:
def getArchi():
    result = []
    # ... execute query ...
    for row in cursor:
        # Aggiungo una tupla (id1, id2, peso) alla lista
        result.append( (row["id1"], row["id2"], row["peso"]) )
    return result

# Nel Model (build_graph):
archi_grezzi = DAO.getArchi()

for id1, id2, peso in archi_grezzi: # Spacchetto la tupla direttamente nel FOR!
    if id1 in self.mappa_nodi and id2 in self.mappa_nodi:
        # ... aggiungo l'arco ...
"""