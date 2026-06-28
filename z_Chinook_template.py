# =====================================================================================
# 🔮 CHINOOK HACKS: METODI PER IL DAO
# Incolla questi metodi nel file DAO.py in base a quale simulazione ti capita!
# =====================================================================================
from database.DB_connect import DBConnect


class DAO_Chinook_Hacks:

    # ---------------------------------------------------------------------------------
    # 🎸 SIMULAZIONE A: L'Affinità tra i Generi (Focus sui Clienti)
    # TRACCIA: Due generi sono collegati se un cliente di Nazione X li ha comprati entrambi.
    # ---------------------------------------------------------------------------------
    @staticmethod
    def get_nodi_generi():
        """Estrae tutti i generi musicali."""
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None: return []
        try:
            cursor = cnx.cursor(dictionary=True)
            query = "SELECT * FROM Genre ORDER BY Name"
            cursor.execute(query)
            for row in cursor:
                result.append(Genre(**row))
            return result
        except Exception as e:
            print("Errore Nodi A:", e)
            return []
        finally:
            cursor.close()
            cnx.close()

    @staticmethod
    def get_archi_generi_comprati_insieme(nazione):
        """
        🚨 TRAPPOLA 2 EVITATA: Magazzino vs Vendite (Track vs InvoiceLine)
        Passiamo per Track -> InvoiceLine -> Invoice -> Customer.

        🚨 IL SALVAVITA (No GROUP BY): Restituisco le TUPLE GREZZE (Genere1, Genere2, Cliente).
        Fare il conteggio dei clienti in SQL bloccherebbe il PC del laboratorio!
        """
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None: return []
        try:
            cursor = cnx.cursor(dictionary=True)
            query = """
            SELECT DISTINCT t1.GenreId AS id1, t2.GenreId AS id2, c.CustomerId AS cliente
            FROM Track t1
            JOIN InvoiceLine il1 ON t1.TrackId = il1.TrackId
            JOIN Invoice i1 ON il1.InvoiceId = i1.InvoiceId
            JOIN Customer c ON i1.CustomerId = c.CustomerId
            JOIN Invoice i2 ON c.CustomerId = i2.CustomerId
            JOIN InvoiceLine il2 ON i2.InvoiceId = il2.InvoiceId
            JOIN Track t2 ON il2.TrackId = t2.TrackId
            WHERE c.Country = %s AND t1.GenreId < t2.GenreId
            """
            cursor.execute(query, (nazione,))
            for row in cursor:
                result.append((row["id1"], row["id2"], row["cliente"]))
            return result
        except Exception as e:
            print("Errore Archi A:", e)
            return []
        finally:
            cursor.close()
            cnx.close()

    # ---------------------------------------------------------------------------------
    # 🎧 SIMULAZIONE B: Playlist Condivise (Focus su Artisti)
    # TRACCIA: Due artisti collegati se compaiono nella stessa Playlist.
    # ---------------------------------------------------------------------------------
    @staticmethod
    def get_nodi_artisti():
        """Estrae tutti gli artisti."""
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None: return []
        try:
            cursor = cnx.cursor(dictionary=True)
            query = "SELECT * FROM Artist"
            cursor.execute(query)
            for row in cursor:
                result.append(Artist(**row))
            return result
        except Exception as e:
            print("Errore Nodi B:", e)
            return []
        finally:
            cursor.close()
            cnx.close()

    @staticmethod
    def get_archi_artisti_stessa_playlist():
        """
        🚨 TRAPPOLA 1 EVITATA: Artist -> Track (Il Salto Mortale)
        L'artista non è collegato alle tracce, BISOGNA passare per Album!
        """
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None: return []
        try:
            cursor = cnx.cursor(dictionary=True)
            query = """
            SELECT al1.ArtistId AS id1, al2.ArtistId AS id2, COUNT(DISTINCT pt1.PlaylistId) AS peso
            FROM Album al1
            JOIN Track t1 ON al1.AlbumId = t1.AlbumId
            JOIN PlaylistTrack pt1 ON t1.TrackId = pt1.TrackId
            JOIN PlaylistTrack pt2 ON pt1.PlaylistId = pt2.PlaylistId
            JOIN Track t2 ON pt2.TrackId = t2.TrackId
            JOIN Album al2 ON t2.AlbumId = al2.AlbumId
            WHERE al1.ArtistId < al2.ArtistId
            GROUP BY al1.ArtistId, al2.ArtistId
            """
            cursor.execute(query)
            for row in cursor:
                result.append((row["id1"], row["id2"], row["peso"]))
            return result
        except Exception as e:
            print("Errore Archi B:", e)
            return []
        finally:
            cursor.close()
            cnx.close()

    # ---------------------------------------------------------------------------------
    # 💿 SIMULAZIONE C: Co-Acquisti Nello Stesso Scontrino (Focus su Tracce)
    # TRACCIA: Tracce dello stesso MediaType acquistate nello stesso scontrino.
    # ---------------------------------------------------------------------------------
    @staticmethod
    def get_archi_tracce_stesso_scontrino(media_type_id):
        """
        🚨 TRAPPOLA 3 EVITATA: Doppioni nelle Fatture
        Usando id1 < id2 ed estraendo i pesi sommati, evitiamo di contare le cose due volte.
        """
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None: return []
        try:
            cursor = cnx.cursor(dictionary=True)
            query = """
            SELECT il1.TrackId AS id1, il2.TrackId AS id2, (t1.UnitPrice + t2.UnitPrice) AS peso
            FROM InvoiceLine il1
            JOIN InvoiceLine il2 ON il1.InvoiceId = il2.InvoiceId
            JOIN Track t1 ON il1.TrackId = t1.TrackId
            JOIN Track t2 ON il2.TrackId = t2.TrackId
            WHERE t1.MediaTypeId = %s AND t2.MediaTypeId = %s AND il1.TrackId < il2.TrackId
            """
            cursor.execute(query, (media_type_id, media_type_id))
            for row in cursor:
                result.append((row["id1"], row["id2"], row["peso"]))
            return result
        except Exception as e:
            print("Errore Archi C:", e)
            return []
        finally:
            cursor.close()
            cnx.close()

            # =====================================================================================
            # 🧠 CHINOOK HACKS: MODEL - COSTRUZIONE GRAFI
            # Come incollare i dati dal DAO nel Grafo senza far freezare il PC!
            # =====================================================================================
            import networkx as nx

class Model_Chinook_Hacks:
    def __init__(self):
        self.grafo = nx.Graph()  # Oppure nx.DiGraph()
        self.mappa_nodi = {}

    # ---------------------------------------------------------------------------------
    # 🎸 REGOLA A: CALCOLO DEL PESO IN PYTHON (Il Salvavita per SQL lenti)
    # Quando vedi SQL metterci troppo tempo (es. Simulazione Generi/Clienti), usa questo!
    # ---------------------------------------------------------------------------------
    def build_graph_A(self, nazione):
        self.grafo = nx.Graph()  # Grafo NON orientato
        self.grafo.clear()
        self.mappa_nodi.clear()

        # 1. Popolo
        for nodo in DAO.get_nodi_generi():
            self.mappa_nodi[nodo.GenreId] = nodo
        self.grafo.add_nodes_from(self.mappa_nodi.values())

        # 2. Prendo le TUPLE GREZZE (id1, id2, ID_Cliente_In_Comune)
        archi_grezzi = DAO.get_archi_generi_comprati_insieme(nazione)

        # 3. Costruisco e Accumulo il peso (Nessun GROUP BY in SQL!)
        for id1, id2, cliente in archi_grezzi:
            # Trappola Self-Loop: evitare archi tra lo stesso nodo
            if id1 == id2: continue

            if id1 in self.mappa_nodi and id2 in self.mappa_nodi:
                n1 = self.mappa_nodi[id1]
                n2 = self.mappa_nodi[id2]

                # SE L'ARCO ESISTE GIÀ: Il peso sale di 1 (Abbiamo trovato un altro cliente)
                if self.grafo.has_edge(n1, n2):
                    self.grafo[n1][n2]['weight'] += 1

                # SE È IL PRIMO CLIENTE CHE TROVO IN COMUNE: Creo l'arco partendo da 1
                else:
                    self.grafo.add_edge(n1, n2, weight=1)

    # ---------------------------------------------------------------------------------
    # 🎧 REGOLA B: DIREZIONI DEGLI ARCHI (Grafo Orientato DiGraph)
    # Quando l'arco punta da A a B in base a una caratteristica dei nodi!
    # ---------------------------------------------------------------------------------
    def build_graph_B(self):
        self.grafo = nx.DiGraph()  # 🚨 ATTENZIONE: Grafo Orientato!
        self.grafo.clear()
        self.mappa_nodi.clear()

        for nodo in DAO.get_nodi_artisti():
            self.mappa_nodi[nodo.ArtistId] = nodo
        self.grafo.add_nodes_from(self.mappa_nodi.values())

        archi_pesati = DAO.get_archi_artisti_stessa_playlist()

        for id1, id2, peso in archi_pesati:
            if id1 == id2: continue

            if id1 in self.mappa_nodi and id2 in self.mappa_nodi:
                n1 = self.mappa_nodi[id1]
                n2 = self.mappa_nodi[id2]

                # 🚨 LA LOGICA DELLA FRECCIA
                # La traccia dice: Freccia da chi ha nome più lungo a chi ce l'ha più corto
                len_n1 = len(n1.Name)
                len_n2 = len(n2.Name)

                if len_n1 > len_n2:
                    self.grafo.add_edge(n1, n2, weight=peso)
                elif len_n2 > len_n1:
                    self.grafo.add_edge(n2, n1, weight=peso)
                else:
                    # In caso di parità, doppio arco (come nella tua traccia originale!)
                    self.grafo.add_edge(n1, n2, weight=peso)
                    self.grafo.add_edge(n2, n1, weight=peso)

                # =====================================================================================
                # 🔁 CHINOOK HACKS: MODEL - LE 3 RICORSIONI SALVA ESAME
                # =====================================================================================
                import copy

    class Model_Ricorsioni_Hacks:

        # ---------------------------------------------------------------------------------
        # TRUCCO 1: PERCORSO A PESI CRESCENTI (La trappola più frequente)
        # "Ogni arco attraversato deve costare strettamente di più del precedente"
        # ---------------------------------------------------------------------------------
        def calcola_percorso_pesi_crescenti(self, nodo_partenza):
            self._soluzione_ottima = []
            self._max_nodi = 0

            parziale = [nodo_partenza]

            # Passo iniziale -1 così il primo arco (che ha peso > 0) va sempre bene
            self._ricorsione_pesi_crescenti(parziale, -1)

            return self._soluzione_ottima, self._max_nodi

        def _ricorsione_pesi_crescenti(self, parziale, peso_precedente):
            if len(parziale) > self._max_nodi:
                self._max_nodi = len(parziale)
                self._soluzione_ottima = copy.deepcopy(parziale)

            ultimo_nodo = parziale[-1]

            # 🚨 BIVIO NETWORKX: Usa .successors() se DiGraph, .neighbors() se Graph
            for vicino in self.grafo.neighbors(ultimo_nodo):
                if vicino not in parziale:
                    peso_arco = self.grafo[ultimo_nodo][vicino]['weight']

                    # 🚨 VINCOLO TRACCIA: L'arco deve essere MAGGIORE del precedente
                    if peso_arco > peso_precedente:
                        parziale.append(vicino)
                        self._ricorsione_pesi_crescenti(parziale,
                                                        peso_arco)  # Passo il nuovo peso come 'ricordo'
                        parziale.pop()

        # ---------------------------------------------------------------------------------
        # TRUCCO 2: SOTTOINSIEME ISOLATO (Il Problema dello Zaino - Senza Collegamenti)
        # "Trova una squadra di K Artisti che NON hanno NESSUN arco in comune"
        # ---------------------------------------------------------------------------------
        def calcola_team_isolate(self, dimensione_k):
            self._soluzione_ottima = []
            self._trovato = False

            # 🚨 Se chiedono l'ordine alfabetico, lo facciamo ORA prima della ricorsione!
            nodi_validi = sorted(list(self.grafo.nodes()), key=lambda x: x.Name)

            self._ricorsione_isole([], nodi_validi, dimensione_k, 0)
            return self._soluzione_ottima

        def _ricorsione_isole(self, parziale, nodi_validi, K, pos):
            if self._trovato: return  # Pruning estremo

            # Condizione di terminazione
            if len(parziale) == K:
                self._soluzione_ottima = copy.deepcopy(parziale)
                self._trovato = True
                return

            # Pruning di sicurezza: se non bastano i nodi rimasti nel cesto, fermati
            if (len(parziale) + (len(nodi_validi) - pos)) < K:
                return

            # Esplorazione dalla Lista (NON con i neighbors!)
            for i in range(pos, len(nodi_validi)):
                candidato = nodi_validi[i]

                # 🚨 IL VINCOLO: Il candidato NON deve essere collegato a quelli già in squadra
                puo_entrare = True
                for nodo_in_squadra in parziale:
                    if self.grafo.has_edge(candidato, nodo_in_squadra):
                        puo_entrare = False
                        break

                if puo_entrare:
                    parziale.append(candidato)
                    # Passo all'indice i+1 per non ripescare la stessa persona
                    self._ricorsione_isole(parziale, nodi_validi, K, i + 1)
                    parziale.pop()

        # ---------------------------------------------------------------------------------
        # TRUCCO 3: CONDIZIONI BASATE SUI NODI (E non sugli archi)
        # "Ogni artista successivo visitato deve avere un nome più corto del precedente"
        # ---------------------------------------------------------------------------------
        def calcola_percorso_nomi_decrescenti(self, nodo_partenza):
            self._soluzione_ottima = []
            self._max_len = 0

            parziale = [nodo_partenza]
            self._ricorsione_nodi_decrescenti(parziale)
            return self._soluzione_ottima

        def _ricorsione_nodi_decrescenti(self, parziale):
            if len(parziale) > self._max_len:
                self._max_len = len(parziale)
                self._soluzione_ottima = copy.deepcopy(parziale)

            ultimo_nodo = parziale[-1]

            for vicino in self.grafo.neighbors(ultimo_nodo):
                if vicino not in parziale:

                    # 🚨 VINCOLO SULLE PROPRIETA' DEGLI OGGETTI NODO
                    if len(vicino.Name) < len(ultimo_nodo.Name):
                        parziale.append(vicino)
                        self._ricorsione_nodi_decrescenti(parziale)
                        parziale.pop()


# =====================================================================================
# 🔮 CHINOOK HACKS V2: DAO.py
# Le due varianti d'esame più "pesanti" da gestire, risolte estraendo dati grezzi.
# =====================================================================================
from database.DB_connect import DBConnect

class DAO_Chinook_Hacks_V2:

    # ---------------------------------------------------------------------------------
    # 📀 SIMULAZIONE D: GLI ALBUM Nello Stesso Scontrino (Co-occorrenza)
    # TRACCIA: Nodi = Album di un determinato Genere. Archi = Due album sono
    # collegati se almeno una traccia del primo e una del secondo sono state
    # comprate nello STESSO scontrino (Invoice). Peso = Numero di scontrini in comune.
    # ---------------------------------------------------------------------------------
    @staticmethod
    def get_nodi_album_by_genere(id_genere):
        """Estrae tutti gli Album che contengono almeno una traccia di quel genere."""
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None: return []
        try:
            cursor = cnx.cursor(dictionary=True)
            # DISTINCT evita che lo stesso album esca 10 volte se ha 10 tracce rock!
            query = """
            SELECT DISTINCT a.* FROM Album a
            JOIN Track t ON a.AlbumId = t.AlbumId
            WHERE t.GenreId = %s
            """
            cursor.execute(query, (id_genere,))
            for row in cursor:
                result.append(Album(**row))
            return result
        except Exception as e:
            print("Errore Nodi D:", e)
            return []
        finally:
            cursor.close()
            cnx.close()

    @staticmethod
    def get_raw_invoices_albums(id_genere):
        """
        🚨 TRUCCO 'GOD-TIER': Evitiamo di unire InvoiceLine con se stessa in SQL!
        Estraiamo semplicemente una lista di: (Id_Scontrino, Id_Album).
        Poi in Python raggrupperemo chi sta nello stesso scontrino.
        """
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None: return []
        try:
            cursor = cnx.cursor(dictionary=True)
            query = """
            SELECT DISTINCT il.InvoiceId, t.AlbumId
            FROM InvoiceLine il
            JOIN Track t ON il.TrackId = t.TrackId
            WHERE t.GenreId = %s
            """
            cursor.execute(query, (id_genere,))
            for row in cursor:
                result.append((row["InvoiceId"], row["AlbumId"]))
            return result
        except Exception as e:
            print("Errore Archi Grezzi D:", e)
            return []
        finally:
            cursor.close()
            cnx.close()


    # ---------------------------------------------------------------------------------
    # 👤 SIMULAZIONE E: CLIENTI SIMILI (Soglie Minime e Set Intersection)
    # TRACCIA: Nodi = Clienti (Customer). Archi = Esiste un arco diretto se due
    # clienti hanno comprato almeno N Tracce in comune.
    # Freccia: Da chi ha speso di meno (In totale) a chi ha speso di più.
    # ---------------------------------------------------------------------------------
    @staticmethod
    def get_nodi_clienti_con_spesa():
        """Estrae i clienti calcolando GIA' la loro spesa totale per definire i versi!"""
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None: return []
        try:
            cursor = cnx.cursor(dictionary=True)
            # COALESCE evita crash se un cliente non ha mai comprato nulla
            query = """
            SELECT c.*, COALESCE(SUM(i.Total), 0) as SpesaTotale
            FROM Customer c
            LEFT JOIN Invoice i ON c.CustomerId = i.CustomerId
            GROUP BY c.CustomerId
            """
            cursor.execute(query)
            for row in cursor:
                result.append(Customer(**row)) # Assicurati di aggiungere 'SpesaTotale' al DTO Customer!
            return result
        except Exception as e:
            print("Errore Nodi E:", e)
            return []
        finally:
            cursor.close()
            cnx.close()

    @staticmethod
    def get_raw_customer_tracks():
        """
        🚨 TRUCCO DEI 'SET': Estraiamo solo (Id_Cliente, Id_Traccia_Comprata).
        Faremo l'intersezione in Python per trovare i brani in comune in 0.01 secondi!
        """
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None: return []
        try:
            cursor = cnx.cursor(dictionary=True)
            query = """
            SELECT DISTINCT i.CustomerId, il.TrackId
            FROM Invoice i
            JOIN InvoiceLine il ON i.InvoiceId = il.InvoiceId
            """
            cursor.execute(query)
            for row in cursor:
                result.append((row["CustomerId"], row["TrackId"]))
            return result
        except Exception as e:
            print("Errore Archi Grezzi E:", e)
            return []
        finally:
            cursor.close()
            cnx.close()

# =====================================================================================
# 🧠 CHINOOK HACKS V2: MODEL - COSTRUZIONE GRAFI
# Come tradurre le estrazioni grezze in Grafi complessi usando i Dizionari Python.
# =====================================================================================
import networkx as nx
import itertools

class Model_Chinook_Hacks_V2:
    def __init__(self):
        self.grafo = nx.Graph()
        self.mappa_nodi = {}

    # ---------------------------------------------------------------------------------
    # 📀 COSTRUZIONE D: Il Raggruppamento per Dizionario
    # ---------------------------------------------------------------------------------
    def build_graph_D(self, id_genere):
        self.grafo = nx.Graph()  # Non orientato
        self.grafo.clear()
        self.mappa_nodi.clear()

        # 1. Popolamento Classico
        for nodo in DAO.get_nodi_album_by_genere(id_genere):
            self.mappa_nodi[nodo.AlbumId] = nodo
        self.grafo.add_nodes_from(self.mappa_nodi.values())

        # 2. La Magia del Raggruppamento in Python
        raw_dati = DAO.get_raw_invoices_albums(id_genere)

        # Creo un dizionario "Scontrino" -> [Lista di Album in quello scontrino]
        scontrini_map = {}
        for id_invoice, id_album in raw_dati:
            if id_invoice not in scontrini_map:
                scontrini_map[id_invoice] = []
            scontrini_map[id_invoice].append(id_album)

        # 3. Creo gli archi iterando sulle liste (Molto più veloce del DB!)
        for id_invoice, lista_album in scontrini_map.items():
            # itertools.combinations crea tutte le coppie possibili di album nello stesso scontrino!
            # Esempio: se lo scontrino ha [A, B, C], crea le coppie (A,B), (A,C), (B,C)
            for id1, id2 in itertools.combinations(lista_album, 2):

                # Controllo di sicurezza
                if id1 in self.mappa_nodi and id2 in self.mappa_nodi:
                    n1 = self.mappa_nodi[id1]
                    n2 = self.mappa_nodi[id2]

                    # Aggiungo o aggiorno il peso
                    if self.grafo.has_edge(n1, n2):
                        self.grafo[n1][n2]['weight'] += 1
                    else:
                        self.grafo.add_edge(n1, n2, weight=1)

    # ---------------------------------------------------------------------------------
    # 👤 COSTRUZIONE E: I 'Set' per trovare gli elementi in comune
    # ---------------------------------------------------------------------------------
    def build_graph_E(self, parametro_N):
        self.grafo = nx.DiGraph()  # 🚨 Orientato
        self.grafo.clear()
        self.mappa_nodi.clear()

        for nodo in DAO.get_nodi_clienti_con_spesa():
            self.mappa_nodi[nodo.CustomerId] = nodo
        self.grafo.add_nodes_from(self.mappa_nodi.values())

        raw_dati = DAO.get_raw_customer_tracks()

        # Creo un dizionario "Cliente" -> SET di tracce comprate (Uso set() per le intersezioni!)
        cliente_tracce_map = {}
        for id_cliente, id_traccia in raw_dati:
            if id_cliente not in cliente_tracce_map:
                cliente_tracce_map[id_cliente] = set()  # 🚨 Inizializzo un Set vuoto
            cliente_tracce_map[id_cliente].add(id_traccia)

        # Itero su tutte le possibili coppie di clienti (Ci sono 59 clienti, 1711 combinazioni veloci)
        tutti_i_clienti = list(cliente_tracce_map.keys())

        for id1, id2 in itertools.combinations(tutti_i_clienti, 2):
            set_tracce_1 = cliente_tracce_map[id1]
            set_tracce_2 = cliente_tracce_map[id2]

            # 🚨 LA POTENZA DI PYTHON: Trovo i brani comprati da entrambi in 1 istante!
            tracce_in_comune = set_tracce_1.intersection(set_tracce_2)
            peso = len(tracce_in_comune)

            # Condizione traccia: Aggiungo arco SOLO SE ne hanno in comune almeno N
            if peso >= parametro_N:
                n1 = self.mappa_nodi[id1]
                n2 = self.mappa_nodi[id2]

                # Condizione Verso: Da chi spende meno a chi spende di più
                if n1.SpesaTotale < n2.SpesaTotale:
                    self.grafo.add_edge(n1, n2, weight=peso)
                elif n2.SpesaTotale < n1.SpesaTotale:
                    self.grafo.add_edge(n2, n1, weight=peso)

    # =====================================================================================
    # 🔁 CHINOOK HACKS V2: MODEL - RICORSIONE CON "BUDGET/PESO MAX"
    # =====================================================================================
    import copy

class Model_Ricorsioni_Hacks_V2:

    # ---------------------------------------------------------------------------------
    # TRUCCO 4: CAMMINO VINCOLATO DAL PESO TOTALE
    # TRACCIA: Trova il percorso PIU' LUNGO in nodi, tale per cui
    # la SOMMA DEI PESI degli archi attraversati non superi un valore M.
    # ---------------------------------------------------------------------------------
    def calcola_percorso_entro_budget(self, nodo_partenza, budget_max):
        self._soluzione_ottima = []
        self._max_nodi = 0

        parziale = [nodo_partenza]

        # Passo la lista parziale e il "costo cumulato finora" (ovviamente all'inizio è 0)
        self._ricorsione_budget(parziale, 0, budget_max)

        return self._soluzione_ottima, self._max_nodi

    def _ricorsione_budget(self, parziale, spesa_attuale, budget_max):
        # Valuto ad ogni step se ho trovato un nuovo record di LUNGHEZZA
        if len(parziale) > self._max_nodi:
            self._max_nodi = len(parziale)
            self._soluzione_ottima = copy.deepcopy(parziale)

        ultimo_nodo = parziale[-1]

        # Esplorazione
        for vicino in self.grafo.neighbors(ultimo_nodo):
            if vicino not in parziale:

                # Quanto mi costa prendere questa strada?
                costo_arco = self.grafo[ultimo_nodo][vicino]['weight']

                # 🚨 SIMULAZIONE DEL BUDGET: Posso prendere questa strada solo se ho i soldi!
                nuova_spesa_totale = spesa_attuale + costo_arco

                if nuova_spesa_totale <= budget_max:
                    parziale.append(vicino)

                    # Avanzo portandomi dietro la spesa aggiornata
                    self._ricorsione_budget(parziale, nuova_spesa_totale, budget_max)

                    parziale.pop()
