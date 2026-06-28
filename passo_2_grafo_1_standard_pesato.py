# =========================================================================
# 🕸️ PASSO 2 - GRAFO TIPO 1: LO STANDARD PESATO (COMPAGNI / EVENTI COMUNI)
# =========================================================================
# === QUANDO USARLO ===
# La traccia dice: "Due nodi sono collegati se hanno condiviso un evento"
# (es. stesso film, stesso team, stesso ordine).
# =========================================================================

# 🛑 CHECKLIST ANTI-CRASH:
# 1. MODEL: nx.Graph() ha le parentesi?
# 2. SQL: Hai messo t1.id < t2.id nella JOIN per evitare archi doppi?
# 3. SQL: Se la traccia dice "Peso maggiore di X", hai aggiunto l'HAVING nella query?
# =========================================================================

# -------------------------------------------------------------------------
# 1. FILE: database/DAO.py (L'estrattore)
# -------------------------------------------------------------------------
class DAO:
    @staticmethod
    def get_archi_pesati(filtro_utente, peso_minimo=0):
        # cnx = DBConnect.get_connection()
        # cursor = cnx.cursor(dictionary=True)
        # result = []

        # 🚨 LA QUERY "MAGICA" DELLE COPPIE (SELF JOIN)
        # query = """
        #     SELECT
        #         t1.id_nodo AS n1,
        #         t2.id_nodo AS n2,
        #         COUNT(*) AS peso_arco
        #     FROM tabella_ponte t1, tabella_ponte t2
        #     WHERE t1.id_evento = t2.id_evento
        #       AND t1.id_nodo < t2.id_nodo  <--- 🚨 FONDAMENTALE: Evita doppioni A-B e B-A!
        #       AND t1.filtro = %s
        #       AND t2.filtro = %s
        #     GROUP BY t1.id_nodo, t2.id_nodo
        #     HAVING peso_arco >= %s         <--- 🚨 TRUCCO: Usalo se la traccia chiede un peso minimo!
        # """

        # cursor.execute(query, (filtro_utente, filtro_utente, peso_minimo))
        # for row in cursor:
        #     result.append((row['n1'], row['n2'], row['peso_arco']))

        # return result
        pass


# -------------------------------------------------------------------------
# 2. FILE: model/model.py (Il Costruttore e l'Analista)
# -------------------------------------------------------------------------
import networkx as nx


class Model:
    # def __init__(self):
    #     self.grafo = nx.Graph()

    def build_graph(self, filtro_utente):
        # self.grafo.clear()

        # ---> SCENARIO A: Tutti i nodi nel grafo (anche quelli isolati senza archi)
        # self.grafo.add_nodes_from(self.mappa_oggetti.values())

        # archi_grezzi = DAO.get_archi_pesati(filtro_utente)

        # for id1, id2, peso in archi_grezzi:
        #     if id1 in self.mappa_oggetti and id2 in self.mappa_oggetti:
        #         nodo1 = self.mappa_oggetti[id1]
        #         nodo2 = self.mappa_oggetti[id2]
        #         self.grafo.add_edge(nodo1, nodo2, weight=peso)

        # ---> SCENARIO B (Opzionale): La traccia dice "Inserire SOLO i nodi che hanno almeno un arco"
        # In questo caso, CANCELLA add_nodes_from iniziale! Aggiungi i nodi dinamicamente qui:
        #         self.grafo.add_node(nodo1)
        #         self.grafo.add_node(nodo2)
        #         self.grafo.add_edge(nodo1, nodo2, weight=peso)
        pass

    # =========================================================================
    # LE 3 RICHIESTE DI ANALISI PIÙ FREQUENTI DEI PROFESSORI
    # =========================================================================

    def get_dettagli_grafo(self):
        """Richiesta Base: Numero nodi e archi"""
        return self.grafo.number_of_nodes(), self.grafo.number_of_edges()

    def get_top_archi(self, k=5):
        """
        Richiesta: "Stampare i 5 archi di peso maggiore"
        === COME FUNZIONA ===
        Estrae tutti gli archi, li ordina per il 'weight' (x[2] è il dizionario dei dati dell'arco).
        """
        archi_ordinati = sorted(self.grafo.edges(data=True), key=lambda x: x[2].get('weight', 0), reverse=True)
        return archi_ordinati[:k]

    def get_analisi_componenti_connesse(self):
        """
        Richiesta: "Stampare numero di componenti connesse e i nodi della maggiore"
        === ATTENZIONE ===
        Funziona SOLO su grafi non orientati (nx.Graph).
        Se il grafo è DiGraph, usa nx.weakly_connected_components(self.grafo).
        """
        if self.grafo.number_of_nodes() == 0:
            return 0, []

        componenti = list(nx.connected_components(self.grafo))
        numero_componenti = len(componenti)

        # Trova l'insieme di nodi più grande
        comp_maggiore = max(componenti, key=len)

        return numero_componenti, list(comp_maggiore)


# -------------------------------------------------------------------------
# 3. FILE: UI/controller.py (La Stampa a Video)
# -------------------------------------------------------------------------
import flet as ft


class Controller:
    def handle_crea_grafo(self, e):
        # 1. Lettura input e chiamata model
        # ...

        # 2. CONTROLLO SICUREZZA
        # self._view.txt_result.controls.clear()
        # n_nodi, n_archi = self._model.get_dettagli_grafo()
        # if n_nodi == 0:
        #     self._view.txt_result.controls.append(ft.Text("Nessun grafo creato!"))
        #     self._view.update_page()
        #     return

        # 3. STAMPE BASE
        # self._view.txt_result.controls.append(ft.Text(f"Grafo creato: {n_nodi} Nodi, {n_archi} Archi", color="green"))

        # 4. SCOMMENTA QUELLO CHE TI CHIEDE LA TRACCIA:

        # ---> RICHIESTA: Top Archi
        # self._view.txt_result.controls.append(ft.Text("Archi più pesanti:", color="red"))
        # for u, v, dati in self._model.get_top_archi(5):
        #     self._view.txt_result.controls.append(ft.Text(f"{u.nome} <-> {v.nome} (Peso: {dati['weight']})"))

        # ---> RICHIESTA: Componenti Connesse
        # num_comp, comp_max = self._model.get_analisi_componenti_connesse()
        # self._view.txt_result.controls.append(ft.Text(f"Componenti connesse: {num_comp}", color="red"))
        # self._view.txt_result.controls.append(ft.Text(f"Dimensione componente maggiore: {len(comp_max)} nodi"))

        # self._view.update_page()
        pass


# =========================================================================
# 🚨 APPENDICE: VARIANTI DEL GRAFO TIPO 1 (GLI "INTERRUTTORI" RAPIDI) 🚨
# =========================================================================
# Usa questa check-list per modificare rapidamente il codice del Grafo Tipo 1
# in base alle parole chiave che trovi nella traccia dell'esame.
# =========================================================================

# -------------------------------------------------------------------------
# VARIANTE A: GRAFO NON PESATO
# === PAROLE CHIAVE NELLA TRACCIA ===
# "Collegare due nodi se hanno corso nello stesso team ALMENO UNA VOLTA".
# Non ti interessa quante volte, ma solo SE è successo.
# -------------------------------------------------------------------------

class VariantiDAO_NonPesato:
    @staticmethod
    def get_archi_non_pesati(filtro):
        # 1. SQL: Via il COUNT! Basta una SELECT DISTINCT.
        # 2. SQL: MANTENGO t1.id < t2.id perché il grafo è ancora Non Orientato!
        """
        query = '''
            SELECT DISTINCT
                t1.id_nodo AS n1,
                t2.id_nodo AS n2
            FROM tabella_ponte t1, tabella_ponte t2
            WHERE t1.id_evento = t2.id_evento
              AND t1.id_nodo < t2.id_nodo  <--- 🚨 SEMPRE PRESENTE!
              AND t1.filtro = %s
        '''
        # (Nessun GROUP BY necessario con DISTINCT)
        """
        pass


class VariantiModel_NonPesato:
    def build_graph_non_pesato(self):
        # 3. PYTHON: Quando creo l'arco, NON passo il parametro 'weight'.
        """
        archi_grezzi = DAO.get_archi_non_pesati(filtro)
        for id1, id2 in archi_grezzi:
            nodo1 = self.mappa_oggetti[id1]
            nodo2 = self.mappa_oggetti[id2]

            # 🚨 NESSUN PESO!
            self.grafo.add_edge(nodo1, nodo2)
        """
        pass


# -------------------------------------------------------------------------
# VARIANTE B: GRAFO ORIENTATO (CONDIZIONE DI DIREZIONE NELLA STESSA GARA/EVENTO)
# === PAROLE CHIAVE NELLA TRACCIA ===
# "Grafo diretto/orientato. Aggiungere un arco dal pilota che è arrivato primo
# al pilota che è arrivato secondo nella stessa gara".
# -------------------------------------------------------------------------

class VariantiDAO_Orientato:
    @staticmethod
    def get_archi_orientati():
        # 1. SQL: CANCELLO t1.id < t2.id! Nei grafi orientati le frecce hanno un senso!
        # 2. SQL: Imposto la condizione di direzione (es. t1 vince, t2 perde).
        """
        query = '''
            SELECT
                t1.id_pilota AS sorgente,
                t2.id_pilota AS destinazione
            FROM risultati t1, risultati t2
            WHERE t1.id_gara = t2.id_gara

              -- 🚨 ATTENZIONE: t1.id < t2.id È STATO ELIMINATO!

              -- CONDIZIONE DELLA FRECCIA: Da chi arriva prima (t1) a chi arriva dopo (t2)
              AND t1.posizione < t2.posizione
        '''
        """
        pass


class VariantiModel_Orientato:
    def init_orientato(self):
        # 3. PYTHON: Ricordati le parentesi nel DiGraph!
        """
        self.grafo = nx.DiGraph()
        """
        pass

    def build_graph_orientato(self):
        # 4. PYTHON: Aggiungo l'arco. L'ordine in cui scrivi i nodi DECIDE la freccia!
        """
        for id_sorgente, id_destinazione in archi_grezzi:
            nodo_sorgente = self.mappa_oggetti[id_sorgente]
            nodo_destinazione = self.mappa_oggetti[id_destinazione]

            # 🚨 L'arco parte SEMPRE dal primo parametro e arriva al secondo!
            self.grafo.add_edge(nodo_sorgente, nodo_destinazione)
        """
        pass