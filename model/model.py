import networkx as nx
import copy
# import sys
# sys.setrecursionlimit(5000)  # Aumenta il limite a 5000 (o 10000)


# Sostituisci con le tue importazioni reali
from database.template_dao import DAO


class Model:
    def __init__(self):
        # =====================================================================
        # 1. STRUTTURE DATI BASE E GRAFI
        # =====================================================================
        self.mappa_oggetti = {}
        self.grafo = nx.Graph()  # nx.DiGraph() se orientato
        self.popola_mappa()

        # =====================================================================
        # 2. VARIABILI PER LA RICORSIONE DI OTTIMIZZAZIONE (Lo "Zaino")
        # =====================================================================
        self._soluzione_ottima = []
        self._punteggio_ottimo = 0  # o float('inf') se devi cercare il minimo!

    # =========================================================================
    # GESTIONE MEMORIA E MAPPA
    # =========================================================================
    def popola_mappa(self):
        # La chiami all'avvio o prima di fare il grafo
        self.mappa_oggetti.clear()
        lista_nodi = DAO.get_tutti_gli_oggetti()
        for nodo in lista_nodi:
            self.mappa_oggetti[nodo.id_oggetto] = nodo

    def get_oggetto_da_cache(self, id_cercato):
        return self.mappa_oggetti.get(int(id_cercato), None)

    # =========================================================================
    # CREAZIONE GRAFO E ANALISI
    # =========================================================================

    # 1 metodo build_graph

    def build_graph(self, parametro_utente):
        self.grafo.clear()

        # PASSO 2: Aggiunta Nodi (Scegli opzione Standard o Union dal DAO)
        # self.grafo.add_nodes_from(self.mappa_oggetti.values())

        # PASSO 3: Archi (Scegli Semplici o Ninja/Pesati dal DAO)
        archi_grezzi = DAO.get_archi_pesati_ninja(parametro_utente)

        # PASSO 4: Collega
        for id_1, id_2, peso in archi_grezzi:
            if id_1 in self.mappa_oggetti and id_2 in self.mappa_oggetti:
                n1 = self.mappa_oggetti[id_1]
                n2 = self.mappa_oggetti[id_2]
                self.grafo.add_edge(n1, n2, weight=peso)

    # =====================================================================
    # PASSO 4 - VARIANTE B: ARCHI ORIENTATI CON CONDIZIONE (Es. Esame Chinook)
    # === QUANDO USARLA ===
    # Quando la traccia dice: "Grafo Orientato: aggiungi un arco da A a B
    # SOLO SE il valore di A è maggiore del valore di B".
    # === ATTENZIONE ===
    # Il DAO in questo caso deve restituire solo le coppie grezze (id_1, id_2),
    # senza calcolare i pesi o l'ordine in SQL, perché lo facciamo qui in Python!
    # =====================================================================
    # for id_1, id_2 in archi_grezzi_senza_peso:
    #     if id_1 in self.mappa_oggetti and id_2 in self.mappa_oggetti:
    #         n1 = self.mappa_oggetti[id_1]
    #         n2 = self.mappa_oggetti[id_2]
    #
    #         # 1. Calcolo il peso richiesto dalla traccia (es. somma delle popolarità)
    #         peso_arco = n1.popolarita + n2.popolarita
    #
    #         # 2. Decido i versi in base alla condizione della traccia
    #         if n1.popolarita > n2.popolarita:
    #             self.grafo.add_edge(n1, n2, weight=peso_arco)
    #
    #         elif n2.popolarita > n1.popolarita:
    #             self.grafo.add_edge(n2, n1, weight=peso_arco)
    #
    #         else:
    #             # (Opzionale) Se la traccia chiede doppio arco in caso di pareggio:
    #             self.grafo.add_edge(n1, n2, weight=peso_arco)
    #             self.grafo.add_edge(n2, n1, weight=peso_arco)

    # 2 metodo build_graph

    def build_graph(self, rate1, rate2):
        """
        Costruisce il grafo gestendo la pulizia dei dati, l'accumulo dei pesi
        e i filtri di rimozione richiesti dalla traccia.
        """
        # 1. PULIZIA INIZIALE: Obbligatoria per evitare che i dati si sommino tra un click e l'altro
        self.grafo.clear()

        # 2. POPOLAMENTO NODI: Riempie la mappa filtrando per età valida
        self.popola_mappa(rate1, rate2)

        # SICUREZZA NETWORKX: Aggiungiamo i nodi usando le CHIAVI (gli ID interi).
        # Evita che NetworkX sdoppi i nodi se passiamo oggetti complessi.
        self.grafo.add_nodes_from(self.mappa_nodi.keys())

        # 3. ESTRAZIONE ARCHI: Prende la lista di tuple dal DAO
        archi_grezzi = DAO.get_archi_grafo_pesato()

        # 4. CICLO UNICO DI COSTRUZIONE: Più veloce ed efficiente dei cicli annidati
        for id_1, id_2, idF, pesoParziale in archi_grezzi:

            # Controllo che entrambi i nodi dell'arco facciano parte dei nodi validi accettati nel grafo
            if id_1 in self.mappa_nodi and id_2 in self.mappa_nodi:

                # -----------------------------------------------------------------
                # PARTE A: PULIZIA DEI DATI PROVENIENTI DAL DAO (Dollari, Spazi, None)
                # -----------------------------------------------------------------
                peso_pulito = 0
                if pesoParziale is not None:
                    try:
                        # Trasformo in stringa per sicurezza, rimuovo il '$' e cancello tutti gli spazi vuoti
                        stringa_pulita = str(pesoParziale).replace('$', '').replace(' ', '')
                        # Converto finalmente in numero intero
                        peso_pulito = int(stringa_pulita)
                    except ValueError:
                        # Se la stringa contiene caratteri strani non convertibili, imposto a 0 per non far crashare l'app
                        peso_pulito = 0

                # -----------------------------------------------------------------
                # PARTE B: LOGICA DI ACCUMULO DEI PESI (has_edge)
                # -----------------------------------------------------------------
                if self.grafo.has_edge(id_1, id_2):
                    # Se l'arco tra questi due attori esiste già, AGGIUNGO (+=) il peso del nuovo film
                    self.grafo[id_1][id_2]['weight'] += peso_pulito
                else:
                    # Se è la prima volta che incontro questa coppia, CREO l'arco da zero
                    self.grafo.add_edge(id_1, id_2, weight=peso_pulito)

        # =========================================================================
        # OPZIONE 1: ELIMINARE GLI ARCHI CON PESO PARI A 0
        # (Usa questo se la traccia dice: 'Non considerare relazioni con incasso nullo')
        # =========================================================================
        archi_da_rimuovere = []
        # Esploro tutti gli archi del grafo estraendo i dati (tra cui il dizionario dei pesi)
        for u, v, dati in self.grafo.edges(data=True):
            if dati['weight'] == 0:
                archi_da_rimuovere.append((u, v))  # Salvo la coppia di nodi

        # Elimino in un colpo solo tutti gli archi che sono rimasti a 0$
        self.grafo.remove_edges_from(archi_da_rimuovere)

        # =========================================================================
        # OPZIONE 2: ELIMINARE I NODI ISOLATI (DI GRADO 0)
        # (Usa questo se la traccia dice: 'Escludere i vertici senza collegamenti')
        # =========================================================================
        nodi_isolati = []
        # Esploro tutti i nodi presenti nel grafo
        for nodo in self.grafo.nodes:
            # self.grafo.degree(nodo) restituisce il numero di archi collegati a quel nodo
            if self.grafo.degree(nodo) == 0:
                nodi_isolati.append(nodo)  # È un nodo isolato, lo marco per l'eliminazione

        # Elimino dal grafo tutti i nodi rimasti orfani di archi
        self.grafo.remove_nodes_from(nodi_isolati)

    def get_dettagli_grafo(self):
        return self.grafo.number_of_nodes(), self.grafo.number_of_edges()

    def get_numero_componenti_connesse(self):
        if self.grafo.number_of_nodes() == 0: return 0
        return nx.number_connected_components(self.grafo)

    # =========================================================================
    # TRUCCO: I TOP 'N' ARCHI (OPZIONE a)
    # =========================================================================
    def get_top_archi_peso(self, n=3):
        # 1. Estraggo tutti gli archi e li trasformo in lista
        lista_archi = list(self.grafo.edges(data=True))

        # 2. Li ordino in base al valore 'weight' dentro il dizionario 'data', al contrario (decrescente)
        lista_archi.sort(key=lambda edge: edge[2]['weight'], reverse=True)

        # 3. Restituisco i primi N elementi
        return lista_archi[:n]

    # =========================================================================
    # TRUCCO: COMPONENTE CONNESSA MAGGIORE (OPZIONE b e c)
    # =========================================================================
    def get_componente_connessa_maggiore(self):
        # 1. Quante sono in totale?
        num_componenti = nx.number_connected_components(self.grafo)

        # 2. Ottengo una lista di "set" (insiemi) contenenti i nodi di ciascuna componente connessa
        componenti = list(nx.connected_components(self.grafo))

        # 3. Trovo quella più grande usando len() come chiave per la ricerca del massimo
        if not componenti:
            return 0, []
        comp_maggiore = max(componenti, key=len)

        return num_componenti, list(comp_maggiore)

    # =========================================================================
    # TRUCCO: ORDINARE PER GRADO DEL NODO (OPZIONE c)
    # =========================================================================
    def ordina_nodi_per_grado(self, lista_nodi):
        # lista_nodi è la componente connessa maggiore che hai trovato prima

        # Il grafo conosce il grado di tutti i nodi: grafo.degree(nodo)
        # Ordiniamo decrescente (reverse=True)
        lista_ordinata = sorted(lista_nodi, key=lambda nodo: self.grafo.degree(nodo), reverse=True)
        return lista_ordinata

    # =========================================================================
    # RICORSIONE 1: DFS (TUTTI I NODI RAGGIUNGIBILI)
    # === QUANDO USARLA === "Elenca tutti i nodi raggiungibili da A"
    # =========================================================================
    #import sys
    #sys.setrecursionlimit(5000)  # Aumenta il limite a 5000 (o 10000)

    def get_nodi_raggiungibili_dfs(self, id_partenza):
        partenza = self.get_oggetto_da_cache(id_partenza)
        if partenza is None or partenza not in self.grafo: return []
        visitati = []
        self._esplora_dfs(partenza, visitati)
        if partenza in visitati: visitati.remove(partenza)
        return visitati

    def _esplora_dfs(self, nodo_corrente, visitati):
        if nodo_corrente in visitati: return
        visitati.append(nodo_corrente)
        for vicino in self.grafo.neighbors(nodo_corrente):
            self._esplora_dfs(vicino, visitati)

    # =========================================================================
    # RICERCA COMPONENTE CONNESSA (Metodo Sicuro per Grafi Enormi)
    # === QUANDO USARLA ===
    # Quando ti chiedono quanti/quali nodi fanno parte dell'isola di un nodo X.
    # Sostituisce la DFS quando il database è troppo grande (evita il RecursionError).
    # =========================================================================
    def get_componente_connessa(self, id_partenza):
        partenza = self.get_oggetto_da_cache(id_partenza)
        if partenza is None or partenza not in self.grafo:
            return []

        try:
            # OPZIONE 1: Perfetta per Grafi NON Orientati (nx.Graph)
            # Restituisce un Set con tutti i nodi della componente connessa
            componente = nx.node_connected_component(self.grafo, partenza)
            return list(componente)

        except nx.NetworkXNotImplemented:
            # OPZIONE 2: Il salvavita per Grafi ORIENTATI (nx.DiGraph)
            # node_connected_component va in crash sui grafi orientati.
            # Se succede, catturiamo l'errore e usiamo la BFS di NetworkX!
            albero_bfs = nx.bfs_tree(self.grafo, partenza)
            return list(albero_bfs.nodes())

    # =========================================================================
    # RICERCA PERCORSO: DIJKSTRA / SHORTEST PATH
    # === QUANDO USARLA === "Trova il percorso più breve o con meno scali da A a B"
    # =========================================================================
    def get_percorso_piu_breve(self, id_partenza, id_arrivo):
        nA = self.get_oggetto_da_cache(id_partenza)
        nB = self.get_oggetto_da_cache(id_arrivo)
        if nA not in self.grafo or nB not in self.grafo: return None
        try:
            # Togli weight='weight' se il grafo NON è pesato
            return nx.shortest_path(self.grafo, source=nA, target=nB, weight='weight')
        except nx.NetworkXNoPath:
            return None

    # =========================================================================
    # RICORSIONE 2: OTTIMIZZAZIONE (IL PROBLEMA DELLO ZAINO / LAB 08)
    # === QUANDO USARLA === "Trova la combinazione o il percorso che massimizza X
    #                        rispettando i vincoli Y"
    # =========================================================================
    def calcola_percorso_ottimo(self, vincolo_1, vincolo_2):
        self._soluzione_ottima = []
        self._punteggio_ottimo = 0

        # Scegli da dove partire (es. tutti i nodi, o dal nodo scelto dall'utente)
        parziale = []
        self._ricorsione_ottimizzazione(parziale, vincolo_1, vincolo_2, 0)

        return self._soluzione_ottima, self._punteggio_ottimo

    def _ricorsione_ottimizzazione(self, parziale, v1, v2, pos):
        # 1. VALUTA SOLUZIONE (es. somma dei pesi, numero di nodi, ecc.)
        punteggio_attuale = len(parziale)  # <-- Cambia la formula in base alla traccia!

        if punteggio_attuale > self._punteggio_ottimo:
            self._punteggio_ottimo = punteggio_attuale
            self._soluzione_ottima = copy.deepcopy(parziale)

        # 2. GENERA NUOVE SOLUZIONI (Es. Ciclando sui vicini nel grafo, o su tutta la lista)
        # (Se stai esplorando un grafo usa: for vicino in self.grafo.neighbors(parziale[-1]): )
        # (Se stai esplorando una lista normale usa: for i in range(pos, len(lista)): )
        lista_elementi = list(self.grafo.nodes())
        for i in range(pos, len(lista_elementi)):
            elemento = lista_elementi[i]

            # Se è un percorso, non posso passare dove sono già stato!
            if elemento not in parziale:
                parziale.append(elemento)

                # 3. CONTROLLA VINCOLI E VAI IN PROFONDITA'
                if self._vincoli_rispettati(parziale, v1, v2):
                    self._ricorsione_ottimizzazione(parziale, v1, v2, i + 1)

                # 4. BACKTRACKING
                parziale.pop()

    def _vincoli_rispettati(self, parziale, v1, v2):
        # Inserisci qui gli "if" della traccia (es. peso max, numero di scali max)
        return True

    # =========================================================================
    # RICORSIONE 3: SOTTOINSIEMI / COMBINAZIONI (La "Scelta di K elementi")
    # === QUANDO USARLA ===
    # Quando la traccia dice: "Trova un SET di K nodi che massimizza/minimizza
    # un certo valore, rispettando dei vincoli" (Es. "nessuno dei K nodi deve
    # essere collegato agli altri").
    # === ATTENZIONE ===
    # Qui NON si usano gli archi (neighbors) per muoversi! Si pesca da una lista.
    # =========================================================================
    def calcola_sottoinsieme_ottimo(self, K):
        self._soluzione_ottima = []
        self._punteggio_ottimo = float('inf')  # Usa 0 se cerchi un MASSIMO, float('inf') se cerchi un MINIMO

        # 1. Definisci da quale "cesto" vuoi pescare. (Spesso sono tutti i nodi, o le componenti connesse)
        nodi_validi = list(self.grafo.nodes())

        parziale = []
        # Faccio partire la ricorsione da posizione 0
        self._ricorsione_sottoinsieme(parziale, nodi_validi, K, 0)

        return self._soluzione_ottima, self._punteggio_ottimo

    def _ricorsione_sottoinsieme(self, parziale, nodi_validi, K, pos):
        # 1. CONDIZIONE DI TERMINAZIONE (Ho pescato esattamente K elementi)
        if len(parziale) == K:
            # Calcolo il punteggio di questa squadra/set
            punteggio = self._calcola_punteggio_set(parziale)

            # Controllo se è il nuovo record (Usa < per MINIMO, > per MASSIMO)
            if punteggio < self._punteggio_ottimo:
                self._punteggio_ottimo = punteggio
                self._soluzione_ottima = copy.deepcopy(parziale)
            return

        # 2. TRUCCO "PRUNING" (Taglio dei rami morti) - FONDAMENTALE!
        # Se nel 'cesto' sono rimasti meno elementi di quanti me ne servono per arrivare a K,
        # è inutile continuare a cercare. Interrompo subito per non far crashare/freezare il PC.
        nodi_rimanenti_nel_cesto = len(nodi_validi) - pos
        if len(parziale) + nodi_rimanenti_nel_cesto < K:
            return

        # 3. ESPLORAZIONE
        # Parto da 'pos' (e non da 0) per NON generare permutazioni doppie (Es: A-B e B-A)
        for i in range(pos, len(nodi_validi)):
            nodo = nodi_validi[i]

            # Controllo se questo nodo può entrare in squadra
            if self._vincolo_sottoinsieme(nodo, parziale):
                parziale.append(nodo)

                # VADO IN PROFONDITÀ.
                # 🚨 PASSO i + 1: Questo mi vieta di ripescare lo stesso nodo!
                self._ricorsione_sottoinsieme(parziale, nodi_validi, K, i + 1)

                # BACKTRACKING
                parziale.pop()

    def _calcola_punteggio_set(self, parziale):
        # --- SOSTITUISCI CON LA MATEMATICA DELLA TRACCIA ---
        # Es. Se cerco la differenza tra il più giovane e il più vecchio:
        # date_nascita = [p.dob for p in parziale]
        # return (max(date_nascita) - min(date_nascita)).days
        return 0

    def _vincolo_sottoinsieme(self, nodo_candidato, parziale):
        # --- SOSTITUISCI CON IL VINCOLO DELLA TRACCIA ---
        # Es. "Nessun pilota del set deve essere collegato agli altri":
        # for nodo_in_squadra in parziale:
        #     if self.grafo.has_edge(nodo_candidato, nodo_in_squadra):
        #         return False
        return True

    # =========================================================================
    # TRUCCO 4: CALCOLO BILANCIO / INFLUENZA SU GRAFI ORIENTATI (DiGraph)
    # === QUANDO USARLA ===
    # Quando la traccia chiede di trovare l'artista/nodo con maggiore influenza,
    # calcolata come "Peso Archi Uscenti - Peso Archi Entranti".
    # === ATTENZIONE ===
    # Funziona SOLO se hai impostato self.grafo = nx.DiGraph() nell'__init__!
    # =========================================================================
    def get_nodo_piu_influente(self):
        # 1. Controllo di sicurezza: se il grafo è vuoto, restituisco None
        if self.grafo.number_of_nodes() == 0:
            return None, 0

        # 2. Inizializzo il record da battere (parto da un numero bassissimo)
        max_influenza = -float('inf')
        miglior_nodo = None

        # 3. Ciclo su tutti i nodi del grafo
        for nodo in self.grafo.nodes():

            # TRUCCO NETWORKX: in_degree(weight='weight') calcola in automatico
            # la SOMMA DEI PESI di tutti gli archi che ENTRANO in questo nodo.
            peso_entrante = self.grafo.in_degree(nodo, weight='weight')

            # out_degree calcola la SOMMA DEI PESI di tutti gli archi che ESCONO.
            peso_uscente = self.grafo.out_degree(nodo, weight='weight')

            # 4. Applico la formula della traccia (Influenza = Uscenti - Entranti)
            influenza = peso_uscente - peso_entrante

            # 5. Se trovo un nuovo record, lo salvo
            if influenza > max_influenza:
                max_influenza = influenza
                miglior_nodo = nodo

        # 6. Restituisco l'oggetto nodo vincente e il suo punteggio
        return miglior_nodo, max_influenza

    # =========================================================================
    # RICORSIONE 4: PERCORSO NEL GRAFO CON CONDIZIONI SUI PESI DEGLI ARCHI
    # === QUANDO USARLA ===
    # "Trova il cammino più lungo partendo da A, tale per cui il peso
    # di ogni arco attraversato sia STRETTAMENTE CRESCENTE / DECRESCENTE".
    # === PERCHÈ È DIVERSA? ===
    # Rispetto alla ricorsione normale, questa ha bisogno di un parametro extra
    # (peso_precedente) per "ricordarsi" quanto pesava la strada appena fatta
    # e decidere se può prendere la strada successiva.
    # =========================================================================
    def calcola_percorso_lungo_con_vincolo_archi(self, nodo_partenza):
        self._soluzione_ottima = []
        self._punteggio_ottimo = 0  # Cerchiamo il percorso più lungo (numero di nodi)

        # Il percorso deve iniziare con il nodo di partenza!
        parziale = [nodo_partenza]

        # Avvio la ricorsione.
        # Passo -1 come 'peso_precedente' (o -float('inf')) in modo che il PRIMO
        # arco che imboccherò (che avrà peso > 0) venga sicuramente accettato.
        self._ricorsione_cammino_vincolato(parziale, -1)

        return self._soluzione_ottima, self._punteggio_ottimo

    def _ricorsione_cammino_vincolato(self, parziale, peso_precedente):
        # 1. VALUTAZIONE: Siccome stiamo cercando il cammino PIÙ LUNGO,
        # aggiorno il record ogni volta che la lista 'parziale' supera il record precedente.
        # (Si valuta ad ogni giro, perché non sappiamo quando si arriverà in un vicolo cieco).
        if len(parziale) > self._punteggio_ottimo:
            self._punteggio_ottimo = len(parziale)
            self._soluzione_ottima = copy.deepcopy(parziale)

        # 2. ESPLORAZIONE: Ci muoviamo SOLO seguendo le strade del grafo!
        ultimo_nodo = parziale[-1]

        # 🚨 BIVIO NETWORKX:
        # Se il grafo è ORIENTATO (nx.DiGraph), devi usare self.grafo.successors(ultimo_nodo)
        # Se il grafo è NORMALE (nx.Graph), devi usare self.grafo.neighbors(ultimo_nodo)
        vicini_raggiungibili = self.grafo.successors(ultimo_nodo)  # (Uso successors per i DiGraph)

        for vicino in vicini_raggiungibili:

            # VINCOLO A (Standard): "Cammino Semplice" = Non posso passare due volte dallo stesso nodo
            if vicino not in parziale:

                # VINCOLO B (Speciale): "Archi strettamente crescenti"
                # Leggo quanto pesa l'arco che collega l'ultimo_nodo al vicino
                peso_nuovo_arco = self.grafo[ultimo_nodo][vicino]['weight']

                # Controllo se il nuovo arco è più pesante di quello precedente
                if peso_nuovo_arco > peso_precedente:
                    # 3. AZIONE: Aggiungo il nodo, vado in profondità e faccio backtracking
                    parziale.append(vicino)

                    # Vado in profondità, passandogli come ricordo il peso appena attraversato
                    self._ricorsione_cammino_vincolato(parziale, peso_nuovo_arco)

                    parziale.pop()

    # =========================================================================
    # RICORSIONE 5: PERCORSO NEL GRAFO CON CONDIZIONI SUI NODI (Es. Età)
    # === QUANDO USARLA ===
    # "Trova il cammino più lungo partendo da A, tale per cui ogni
    # nodo successivo abbia una proprietà (es. età) STRETTAMENTE DECRESCENTE".
    # === PERCHÈ È DIVERSA? ===
    # Non ci interessa il peso dell'arco, ma dobbiamo confrontare un attributo
    # dell'oggetto in cui ci troviamo (ultimo_nodo) con l'oggetto dove stiamo
    # per andare (vicino). Non serve passare parametri extra nella firma.
    # =========================================================================
    def calcola_percorso_lungo_con_vincolo_nodi(self, nodo_partenza):
        self._soluzione_ottima = []
        self._punteggio_ottimo = 0

        # Il percorso inizia con il nodo di partenza
        parziale = [nodo_partenza]

        self._ricorsione_cammino_vincolo_nodi(parziale)

        return self._soluzione_ottima, self._punteggio_ottimo

    def _ricorsione_cammino_vincolo_nodi(self, parziale):
        # 1. VALUTAZIONE: Stiamo cercando il percorso più LUNGO
        if len(parziale) > self._punteggio_ottimo:
            self._punteggio_ottimo = len(parziale)
            self._soluzione_ottima = copy.deepcopy(parziale)

        # 2. ESPLORAZIONE
        ultimo_nodo = parziale[-1]

        # Uso .neighbors() per i grafi non orientati (come richiesto in questo esame)
        for vicino in self.grafo.neighbors(ultimo_nodo):

            # VINCOLO A (La traccia chiede "Cammino Semplice"): Non ripassare sui nodi
            if vicino not in parziale:

                # VINCOLO B (Speciale): "Età strettamente decrescente"
                # Confronto l'attributo .eta (che devi aver messo nel DTO) del vicino
                # con l'attributo .eta del nodo in cui mi trovo ora.

                # Sostituisci '.eta' con l'attributo reale del tuo DTO all'esame!
                if vicino.eta < ultimo_nodo.eta:
                    # 3. AZIONE E BACKTRACKING
                    parziale.append(vicino)
                    self._ricorsione_cammino_vincolo_nodi(parziale)
                    parziale.pop()

        # =========================================================================
        # RICORSIONE 6: PERCORSO ESATTO (Partenza, Arrivo e Lunghezza Fissa)
        # === QUANDO USARLA ===
        # Quando la traccia fissa un "Punto A" e un "Punto B", e chiede di trovare
        # il cammino di lunghezza esatta "LUN" che massimizzi (o minimizzi) il peso.
        # === ATTENZIONE ===
        # Di default usa '.successors()' (Grafo Orientato). Se il tuo esame ha
        # un grafo NON orientato, ricordati di cambiare 'successors' in 'neighbors'!
        # =========================================================================
        def calcola_percorso_lunghezza_fissa(self, nodo_start, nodo_end, lunghezza_target):
            self._soluzione_ottima = []
            self._punteggio_ottimo = 0  # Metti float('inf') se cerchi il minimo!

            # Il percorso DEVE partire dal nodo_start
            parziale = [nodo_start]

            # Avvio ricorsione: parziale, destinazione, lunghezza voluta, peso_accumulato_finora
            self._ricorsione_percorso_fisso(parziale, nodo_end, lunghezza_target, 0)

            return self._soluzione_ottima, self._punteggio_ottimo

        def _ricorsione_percorso_fisso(self, parziale, nodo_end, lunghezza_target, peso_attuale):

            # 1. VALUTAZIONE: Controllo se ho raggiunto la lunghezza e la destinazione
            if len(parziale) == lunghezza_target and parziale[-1] == nodo_end:
                # Controllo se è il nuovo record MAX (Usa < se cerchi il MIN)
                if peso_attuale > self._punteggio_ottimo:
                    self._punteggio_ottimo = peso_attuale
                    self._soluzione_ottima = copy.deepcopy(parziale)
                return

            # 2. PRUNING: Se ho superato la lunghezza massima, è inutile continuare
            if len(parziale) >= lunghezza_target:
                return

            # 3. ESPLORAZIONE
            ultimo_nodo = parziale[-1]

            # 🚨 BIVIO NETWORKX:
            # Usa .successors() se nx.DiGraph()
            # Usa .neighbors() se nx.Graph()
            for vicino in self.grafo.successors(ultimo_nodo):

                # Vincolo Base: Cammino semplice (nessun nodo ripetuto)
                if vicino not in parziale:
                    # Leggo il peso dell'arco
                    peso_arco = self.grafo[ultimo_nodo][vicino]['weight']

                    # Vado in profondità
                    parziale.append(vicino)
                    self._ricorsione_percorso_fisso(parziale, nodo_end, lunghezza_target, peso_attuale + peso_arco)
                    parziale.pop()