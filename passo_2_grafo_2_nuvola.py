# =========================================================================
# ☁️ PASSO 2 - GRAFO TIPO 2: IL GRAFO "A NUVOLA" COMPLETO (PYTHON LOOPS)
# =========================================================================
# === QUANDO USARLO ===
# La traccia non fissa un evento condiviso (es. stesso scontrino), ma una
# condizione slegata: "Collega due prodotti se ENTRAMBI sono stati venduti
# nell'anno X". Si costruisce con il doppio ciclo for in Python.
# =========================================================================

# -------------------------------------------------------------------------
# 1. FILE: model/dto.py (Il Nodo)
# -------------------------------------------------------------------------
# REQUISITO FONDAMENTALE: Il DTO deve avere i metodi magici, altrimenti
# il doppio ciclo `for n1, n2 in...` inserirà nodi duplicati in NetworkX.
"""
@dataclass
class OggettoDTO:
    id_univoco: int
    nome: str

    def __eq__(self, other):
        if isinstance(other, OggettoDTO):
            return self.id_univoco == other.id_univoco
        return False

    def __hash__(self):
        return hash(self.id_univoco)
"""


# -------------------------------------------------------------------------
# 2. FILE: database/DAO.py (L'estrattore della Mappa)
# -------------------------------------------------------------------------
class DAO:
    @staticmethod
    def get_mappa_pesi_nodi(filtro_utente):
        """
        🚨 NESSUNA JOIN QUI! Estraiamo solo i dati di ogni SINGOLO nodo.
        Restituisce un dizionario: {ID_NODO: VALORE_UTILE}
        """
        # cnx = DBConnect.get_connection()
        # cursor = cnx.cursor(dictionary=True)
        # result = {}

        # query = """
        #     SELECT id_nodo, COUNT(*) AS punteggio
        #     FROM tabella_dati
        #     WHERE colonna_filtro = %s
        #     GROUP BY id_nodo
        # """

        # cursor.execute(query, (filtro_utente,))
        # for row in cursor:
        #     result[row['id_nodo']] = row['punteggio']

        # return result
        pass


# -------------------------------------------------------------------------
# 3. FILE: model/model.py (Il Motore degli Incroci con tutte le varianti)
# -------------------------------------------------------------------------
import networkx as nx


class Model:
    # def __init__(self):
    #     self.grafo = nx.Graph()   <-- Cambia in nx.DiGraph() se la traccia vuole frecce!

    def build_graph_nuvola(self, filtro_utente):
        # 1. PULIZIA E PREPARAZIONE
        # self.grafo.clear()

        # Spesso la traccia chiede di includere anche i nodi isolati:
        # self.grafo.add_nodes_from(self.mappa_oggetti.values())

        # 2. CARICO LA CACHE DAL DAO (1 sola query SQL!)
        # mappa_valori = DAO.get_mappa_pesi_nodi(filtro_utente)

        # 3. IL DOPPIO CICLO
        # nodi = list(self.grafo.nodes())

        # for i in range(len(nodi)):
        #     for j in range(i + 1, len(nodi)):  # 🚨 range(i+1) evita doppioni A-B e B-A!

        #         n1 = nodi[i]
        #         n2 = nodi[j]

        #         # 4. LETTURA SICURA (Se il nodo non è nel DB, vale 0)
        #         valore1 = int(mappa_valori.get(n1.id_univoco, 0))
        #         valore2 = int(mappa_valori.get(n2.id_univoco, 0))

        #         # ===============================================================
        #         # 🚨 BIVIO LOGICO: SCEGLI IL BLOCCO IN BASE ALLA TRACCIA!
        #         # ===============================================================

        #         # ---> SCENARIO A: GRAFO NON ORIENTATO E NON PESATO
        #         # "Collega se entrambi hanno valore > 0" (Niente frecce, niente pesi)
        #         if valore1 > 0 and valore2 > 0:
        #             self.grafo.add_edge(n1, n2)

        #         # ---> SCENARIO B: GRAFO NON ORIENTATO E PESATO
        #         # "Collega se entrambi > 0. Il peso è la somma dei valori"
        #         if valore1 > 0 and valore2 > 0:
        #             peso_totale = valore1 + valore2
        #             self.grafo.add_edge(n1, n2, weight=peso_totale)

        #         # ---> SCENARIO C: GRAFO ORIENTATO (CONDIZIONALE)
        #         # "Orientato. Dal maggiore al minore. In caso di parità, doppio arco. Peso = somma"
        #         # (Ricordati di aver messo nx.DiGraph() nell'__init__)
        #         if valore1 > 0 and valore2 > 0:
        #             peso_totale = valore1 + valore2
        #
        #             if valore1 > valore2:
        #                 self.grafo.add_edge(n1, n2, weight=peso_totale)
        #             elif valore2 > valore1:
        #                 self.grafo.add_edge(n2, n1, weight=peso_totale)
        #             else:
        #                 # Pareggio
        #                 self.grafo.add_edge(n1, n2, weight=peso_totale)
        #                 self.grafo.add_edge(n2, n1, weight=peso_totale)
        pass

    # ---> METODI DI ANALISI STANDARD DA CHIAMARE NEL CONTROLLER
    def get_dettagli_grafo(self):
        return self.grafo.number_of_nodes(), self.grafo.number_of_edges()


# -------------------------------------------------------------------------
# 4. FILE: UI/controller.py (L'Interruttore e la Stampa)
# -------------------------------------------------------------------------
import flet as ft


class Controller:
    def handle_crea_grafo_nuvola(self, e):
        # 1. LETTURA INPUT E CONTROLLO ERRORI
        # valore_selezionato = self._view.dd_filtro.value
        # if valore_selezionato is None:
        #     self._view.create_alert("Seleziona un parametro!")
        #     return

        # 2. CHIAMATA AL MODEL
        # self._model.build_graph_nuvola(valore_selezionato)

        # 3. PULIZIA SCHERMO E VERIFICA SICUREZZA
        # self._view.txt_result.controls.clear()

        # n_nodi, n_archi = self._model.get_dettagli_grafo()
        # if n_nodi == 0:
        #     self._view.txt_result.controls.append(ft.Text("Attenzione: Il grafo è vuoto!", color="red"))
        #     self._view.update_page()
        #     return

        # 4. STAMPA DEL RISULTATO
        # self._view.txt_result.controls.append(ft.Text("Grafo Creato Correttamente!", color="green", weight="bold"))
        # self._view.txt_result.controls.append(ft.Text(f"Numero di Nodi: {n_nodi}"))
        # self._view.txt_result.controls.append(ft.Text(f"Numero di Archi: {n_archi}"))

        # 5. AZIONI SUCCESSIVE (Opzionali)
        # Scommenta se la traccia richiede di stampare subito archi top o componenti connesse (Vedi Grafo Tipo 1)
        # self.popola_tendine_nodi_per_punto_2()

        # self._view.update_page()
        pass