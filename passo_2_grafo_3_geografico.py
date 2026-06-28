# =========================================================================
# 🌍 PASSO 2 - GRAFO TIPO 3: IL GRAFO "GEOGRAFICO/SPAZIALE" (Distanze)
# =========================================================================
# === QUANDO USARLO ===
# La traccia fornisce le coordinate (Latitudine e Longitudine) per ogni nodo
# e ti chiede di collegarli se sono "vicini" (es. distanza < X km), oppure
# di usare la distanza fisica come 'weight' dell'arco.
# =========================================================================

# 🛑 CHECKLIST ANTI-CRASH (Errori letali da non fare):
# 1. DTO: Hai aggiunto lat e lon come float nel dataclass?
# 2. DTO: I metodi magici (__eq__, __hash__) ci sono sempre?
# 3. MATH: Hai importato 'math' per le formule?
# 4. PYTHON: Stai usando il doppio ciclo con range(i+1) per evitare doppioni?
# 5. CONDIZIONE: Stai confrontando km con km (o miglia con miglia)?
# =========================================================================

# -------------------------------------------------------------------------
# 1. FILE: model/dto.py (Il Nodo con Coordinate)
# -------------------------------------------------------------------------
"""
from dataclasses import dataclass

@dataclass
class LuogoDTO:
    id_univoco: int
    nome: str
    lat: float  # 🚨 ATTENZIONE: Devono essere float, non stringhe!
    lon: float

    def __eq__(self, other):
        if isinstance(other, LuogoDTO):
            return self.id_univoco == other.id_univoco
        return False

    def __hash__(self):
        return hash(self.id_univoco)
"""


# -------------------------------------------------------------------------
# 2. FILE: database/DAO.py (L'estrattore base)
# -------------------------------------------------------------------------
class DAO:
    @staticmethod
    def get_tutti_i_luoghi(filtro_utente=None):
        """
        Nessuna query complessa qui. Prendi solo i nodi.
        I calcoli di distanza si fanno nel Model.
        """
        # ... standard estrazione (Vedi Template Base) ...
        pass


# -------------------------------------------------------------------------
# 3. FILE: model/model.py (Il Motore Geografico)
# -------------------------------------------------------------------------
import networkx as nx
import math


class Model:
    # def __init__(self):
    #     self.grafo = nx.Graph()

    # =========================================================================
    # 🚨 LA FUNZIONE UNIVERSALE PER CALCOLARE LE DISTANZE (Formula di Haversine)
    # Copiala esattamente così. Non provare a reinventarla. Restituisce KM.
    # =========================================================================
    def calcola_distanza_km(self, lat1, lon1, lat2, lon2):
        R = 6371.0  # Raggio della Terra in km

        # Converte da gradi a radianti
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)

        dlon = lon2_rad - lon1_rad
        dlat = lat2_rad - lat1_rad

        a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distanza = R * c
        return distanza

    # =========================================================================
    # LA COSTRUZIONE DEL GRAFO
    # =========================================================================
    def build_graph_geografico(self, distanza_max_km):
        # 1. AZZERO IL GRAFO E AGGIUNGO I NODI
        # self.grafo.clear()
        # self.grafo.add_nodes_from(self.mappa_oggetti.values())

        # 2. DOPPIO CICLO PER ESPLORARE TUTTE LE COPPIE POSSIBILI
        # nodi = list(self.grafo.nodes())

        # for i in range(len(nodi)):
        #     for j in range(i + 1, len(nodi)): # 🚨 range(i+1) = niente doppioni!
        #
        #         n1 = nodi[i]
        #         n2 = nodi[j]
        #
        #         # 3. CALCOLO LA DISTANZA FISICA
        #         distanza = self.calcola_distanza_km(n1.lat, n1.lon, n2.lat, n2.lon)
        #
        #         # ===============================================================
        #         # 🚨 BIVIO LOGICO: SCEGLI IL BLOCCO IN BASE ALLA TRACCIA!
        #         # ===============================================================
        #
        #         # ---> SCENARIO A: SOGLIA DI DISTANZA (Non pesato o peso=distanza)
        #         # "Collega i due luoghi SE distano MENO di distanza_max_km"
        #         if distanza <= distanza_max_km:
        #
        #             # Opzione A1 (Non pesato):
        #             # self.grafo.add_edge(n1, n2)
        #
        #             # Opzione A2 (Peso = Distanza reale in km):
        #             # self.grafo.add_edge(n1, n2, weight=distanza)
        #
        #         # ---> SCENARIO B: PESO INVERSAMENTE PROPORZIONALE
        #         # Meno probabile ma infame: "Il peso è maggiore se sono più vicini".
        #         # La traccia ti darà la formula esatta, ma di solito è 1 / distanza
        #         # if distanza > 0 and distanza <= distanza_max_km:
        #         #     peso_inverso = 1 / distanza
        #         #     self.grafo.add_edge(n1, n2, weight=peso_inverso)

        pass

    # ---> METODI DI ANALISI STANDARD
    def get_dettagli_grafo(self):
        return self.grafo.number_of_nodes(), self.grafo.number_of_edges()

    def get_archi_piu_vicini(self, k=3):
        """
        Spesso chiedono: "Stampa le 3 città più vicine tra loro"
        (Cerco i pesi MINORI se il peso = distanza).
        Attenzione al 'reverse=False' per avere prima i numeri più piccoli!
        """
        archi = self.grafo.edges(data=True)
        # Ordino in modo CRESCENTE (dal più vicino al più lontano)
        archi_ordinati = sorted(archi, key=lambda x: x[2].get('weight', 999999), reverse=False)
        return archi_ordinati[:k]


# -------------------------------------------------------------------------
# 4. FILE: UI/controller.py (La Stampa)
# -------------------------------------------------------------------------
import flet as ft


class Controller:
    def handle_crea_grafo_geografico(self, e):
        # 1. LETTURA INPUT
        # try:
        #     dist_max = float(self._view.txt_distanza.value) # 🚨 float, non int!
        # except ValueError:
        #     self._view.create_alert("Inserisci un numero valido per i KM!")
        #     return

        # 2. CHIAMATA AL MODEL
        # self._model.build_graph_geografico(dist_max)

        # 3. VERIFICA SICUREZZA
        # self._view.txt_result.controls.clear()
        # n_nodi, n_archi = self._model.get_dettagli_grafo()
        #
        # if n_nodi == 0:
        #     self._view.txt_result.controls.append(ft.Text("Errore: Grafo vuoto!", color="red"))
        #     self._view.update_page()
        #     return

        # 4. STAMPE
        # self._view.txt_result.controls.append(ft.Text("Grafo Geografico Creato!", color="green"))
        # self._view.txt_result.controls.append(ft.Text(f"Nodi: {n_nodi} | Archi: {n_archi}"))

        # ---> RICHIESTA SPECIFICA (Es. i luoghi più vicini)
        # self._view.txt_result.controls.append(ft.Text("I 3 collegamenti più brevi:", color="blue"))
        # for u, v, dati in self._model.get_archi_piu_vicini(3):
        #     self._view.txt_result.controls.append(ft.Text(f"{u.nome} <-> {v.nome} (Distanza: {dati['weight']:.2f} km)"))

        # self._view.update_page()
        pass