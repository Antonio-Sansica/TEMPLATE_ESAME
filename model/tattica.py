import flet as ft


# =========================================================================
# 📘 MANUALE TATTICO: STRUTTURE DATI, ORDINAMENTI E INTERFACCIA
# =========================================================================

class ModelManuale:
    def __init__(self):
        # ---------------------------------------------------------------------
        # 1. IL DIZIONARIO (La tua arma principale per l'efficienza)
        # === QUANDO USARLO ===
        # - Per la cache dei nodi (mappa_oggetti).
        # - Per salvare aggregazioni dal DAO prima di un ciclo (es. vendite_prodotti).
        # === PERCHÉ ===
        # Cercare un elemento in un dizionario è istantaneo (costo O(1)).
        # In una lista, il PC deve scorrere tutti gli elementi, bloccandosi.
        # ---------------------------------------------------------------------
        self.mappa_oggetti = {}
        self.vendite_cache = {}

    def popola_mappa_nodi(self, lista_oggetti_dal_dao):
        """Salva i DTO in un dizionario per ritrovarli all'istante tramite l'ID."""
        for oggetto in lista_oggetti_dal_dao:
            # CHIAVE = ID univoco (int o stringa) | VALORE = L'oggetto DTO intero
            self.mappa_oggetti[oggetto.id_univoco] = oggetto

    def recupera_da_cache_in_sicurezza(self, id_cercato):
        """
        === IL TRUCCO DEL .get() ===
        Non usare MAI: self.mappa_oggetti[id_cercato] (Se non esiste, l'app crasha!).
        Usa SEMPRE .get(). Se la chiave non esiste, restituisce None (o 0), salvandoti.
        """
        oggetto = self.mappa_oggetti.get(id_cercato, None)
        # Esempio per i pesi: peso = self.vendite_cache.get(id_prodotto, 0)
        return oggetto

    def test_lista_vs_set(self):
        # ---------------------------------------------------------------------
        # 2. LISTA vs SET (Quando usare cosa)
        # ---------------------------------------------------------------------

        # ---> LA LISTA []
        # === QUANDO USARLA ===
        # Per percorsi (l'ordine conta), classifiche (Top 5) o risultati grezzi SQL.
        percorso = []
        percorso.append("Nodo_A")  # Aggiunge in fondo
        percorso.pop()  # Rimuove l'ultimo (fondamentale per il Backtracking!)

        # ---> IL SET {}
        # === QUANDO USARLO ===
        # Per controllare se hai GIA' visitato un nodo. Ignora i doppioni ed è fulmineo.
        nodi_visitati = set()
        nodi_visitati.add("Nodo_A")

        # L'operazione "in" su un Set è veloce quanto un dizionario.
        if "Nodo_B" not in nodi_visitati:
            pass

    def manuale_ordinamenti(self):
        # ---------------------------------------------------------------------
        # 3. L'ARTE DEL SORTING (Ordinare qualsiasi cosa)
        # ---------------------------------------------------------------------
        lista_dto = []  # Immagina sia piena di oggetti (es. Prodotti)
        lista_tuple = []  # Immagina sia [(nodoA, 100), (nodoB, 50)]
        dizionario_dati = {101: 50, 102: 900}  # {id_prodotto: vendite}

        # --- A) ORDINARE LISTE DI OGGETTI (DTO) ---
        # Crescente (es. dalla A alla Z)
        lista_dto.sort(key=lambda x: x.nome_prodotto)

        # Decrescente (es. dal più costoso al più economico)
        lista_dto.sort(key=lambda x: x.prezzo, reverse=True)

        # Doppio vincolo (Prima per Categoria, poi a parità di Categoria per Nome)
        lista_dto.sort(key=lambda x: (x.categoria, x.nome_prodotto))

        # --- B) ORDINARE LISTE DI TUPLE ---
        # Voglio ordinare per il punteggio (che si trova all'indice [1] della tupla)
        lista_tuple.sort(key=lambda x: x[1], reverse=True)
        # Voglio ordinare per il nome del nodo (oggetto all'indice [0] della tupla)
        lista_tuple.sort(key=lambda x: x[0].nome)

        # --- C) ORDINARE UN DIZIONARIO ---
        # I dizionari non si ordinano! Devi estrarre gli elementi (.items()) e creare una lista.
        # Restituisce una lista di tuple ordinata per i VALORI (x[1]) decrescenti.
        lista_ordinata_da_dict = sorted(dizionario_dati.items(), key=lambda x: x[1], reverse=True)


# =========================================================================
# 📘 INTERFACCIA: COME GESTIRE LE TENDINE (DROPDOWN) SENZA CRASH
# =========================================================================

class ControllerManuale:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def riempi_tendina_correttamente(self):
        """
        === LA REGOLA AUREA DELLE TENDINE ===
        TEXT: La "vetrina" per l'utente umano (es. "Bicicletta Rossa").
        KEY: Il "codice a barre" per il database/grafo (es. l'ID 105).
        """
        self._view.dd_nodi.options.clear()

        # 1. Prendo i dati e li ordino SEMPRE (l'utente odia le tendine disordinate)
        nodi = list(self._model.get_tutti_i_nodi())
        nodi.sort(key=lambda x: x.nome)

        # 2. Inserisco separando KEY e TEXT
        for nodo in nodi:
            self._view.dd_nodi.options.append(
                ft.dropdown.Option(
                    key=str(nodo.id_univoco),  # ⚠️ FLET VUOLE STRINGHE: converti sempre l'ID con str()
                    text=nodo.nome  # Quello che appare a schermo
                )
            )
        self._view.update_page()

    def leggi_da_tendina_correttamente(self, e):
        """
        === COME LEGGERE E USARE L'ID SCELTO DALL'UTENTE ===
        """
        # 1. Leggo la KEY nascosta (che Flet mi restituisce come Stringa, es. "105")
        id_selezionato_str = self._view.dd_nodi.value

        # 2. Controllo anti-crash (se l'utente clicca il bottone senza scegliere nulla)
        if id_selezionato_str is None:
            self._view.create_alert("Seleziona un elemento dalla tendina!")
            return

        # 3. Converto la stringa in numero (se il mio ID nel database è un intero)
        id_selezionato = int(id_selezionato_str)

        # 4. CHICCA ASSOLUTA: Uso l'ID per recuperare l'oggetto intero dal Model!
        oggetto_scelto = self._model.recupera_da_cache_in_sicurezza(id_selezionato)

        if oggetto_scelto is None:
            self._view.create_alert("Errore: Oggetto non trovato in memoria.")
            return

        # 5. Adesso passo l'oggetto al Model per fare le analisi
        # self._model.calcola_percorso(oggetto_scelto)