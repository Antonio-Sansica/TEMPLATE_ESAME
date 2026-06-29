import flet as ft

class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    # =========================================================================
    # FASE 1: AVVIO DELL'APPLICAZIONE (Opzionale)
    # =========================================================================
    def populate_dd_iniziali(self):
        # self._view.dd_filtro_base.options.clear()
        # dati = self._model.get_filtri_dal_db()
        # for dato in dati:
        #     self._view.dd_filtro_base.options.append(ft.dropdown.Option(str(dato)))
        pass

    # =========================================================================
    # FASE 2: BOTTONE 1 - CREAZIONE DEL GRAFO E STAMPA DETTAGLI
    # =========================================================================
    def handle_crea_grafo(self, e):
        # 1. LETTURA INPUT E CONTROLLO ERRORI
        valore_str = self._view.txt_input.value
        try:
            parametro_utente = int(valore_str)
        except ValueError:
            self._view.create_alert("Attenzione: Inserisci un numero valido!")
            return

        # Trasforma le date di Flet in stringhe SQL-friendly per non perdere l'ultimo giorno
        # d1_str = date1.strftime("%Y-%m-%d")
        # d2_str = date2.strftime("%Y-%m-%d")

        # 2. CHIAMATA AL MODEL
        self._model.build_graph(parametro_utente)

        # 3. PULIZIA SCHERMO E VERIFICA
        self._view.txt_result.controls.clear()

        if self._model.grafo.number_of_nodes() == 0:
            self._view.txt_result.controls.append(ft.Text("Nessun grafo creato con questi parametri."))
            self._view.update_page()
            return

        # 4. STAMPA DELLE RISPOSTE STANDARD
        nodi, archi = self._model.get_dettagli_grafo()
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato con successo!", color="green"))
        self._view.txt_result.controls.append(ft.Text(f"Numero Nodi: {nodi}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero Archi: {archi}"))

        # ---> TRUCCO: STAMPA ARCHI E PESI (Scommenta se richiesto)
        # for u, v, data in self._model.grafo.edges(data=True):
        #     peso = data.get('weight', 'N/A')
        #     self._view.txt_result.controls.append(ft.Text(f"{u.nome} <---> {v.nome} | Peso: {peso}"))

        # a) Stampa i tre archi di peso maggiore
        self._view.txt_result.controls.append(ft.Text("Archi di peso maggiore:", color="red"))
        top_archi = self._model.get_top_archi_peso(3)
        for u, v, dati in top_archi:
            self._view.txt_result.controls.append(ft.Text(f"{u.surname} -> {v.surname} ({dati['weight']})"))

        # b) Numero componenti connesse e componente maggiore
        num_comp, comp_maggiore = self._model.get_componente_connessa_maggiore()
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {num_comp} componenti connesse", color="red"))
        self._view.txt_result.controls.append(
            ft.Text(f"Componente più grande ({len(comp_maggiore)} nodi):", color="red"))

        # Stampa i nodi della componente maggiore (puoi stamparli come preferisci)
        for nodo in comp_maggiore:
            self._view.txt_result.controls.append(ft.Text(f"{nodo.surname} ({nodo.driver_id}) -- DoB: {nodo.dob}"))

        # 1. Creiamo una funzione di supporto (o una funzione lambda) per calcolare il peso massimo di un nodo(serve quando la traccia dice:(il programma dovrà identificare la componente connessa di dimensione maggiore, e stamparne
        # tutti i nodi, ordinati in senso decrescente di peso massimo degli archi incidenti)
        def get_peso_massimo_nodo(nodo):
            # Prendiamo tutti gli archi collegati a questo nodo
            archi_incidenti = self._model.grafo.edges(nodo, data=True)

            # Se il nodo è isolato (non ha archi), il suo peso massimo è 0
            if not archi_incidenti:
                return 0

            # Estraiamo il valore 'weight' da ogni arco e cerchiamo il massimo
            # (data_arco[2] contiene il dizionario degli attributi dell'arco, ad esempio {'weight': 45})
            pesi = [data_arco[2].get('weight', 0) for data_arco in archi_incidenti]
            return max(pesi)

        # 2. Ordiniamo la lista 'comp_maggiore' usando la nostra funzione come chiave di ordinamento
        # Usiamo reverse=True perché la traccia chiede l'ordine DECRESCENTE (dal più grande al più piccolo)
        comp_maggiore_ordinata = sorted(comp_maggiore, key=get_peso_massimo_nodo, reverse=True)

        # 3. Stampiamo i nodi ormai ordinati (ricordati di usare i campi corretti del tuo Constructor!)
        for nodo in comp_maggiore_ordinata:
            # Calcoliamo il peso massimo solo per poterlo stampare a schermo (utile per verificare se è giusto!)
            peso_max = get_peso_massimo_nodo(nodo)

            # Sostituito surname/driver_id/dob con i campi reali dell'oggetto Constructor (name, nationality)
            self._view._txt_result.controls.append(
                ft.Text(f"{nodo.name} ({nodo.nationality}) -- Peso Max Arco: {peso_max}")
            )

        # c) Nodi ordinati per grado
        self._view.txt_result.controls.append(ft.Text("Componente connessa in ordine decrescente:", color="red"))
        nodi_ordinati = self._model.ordina_nodi_per_grado(comp_maggiore)

        for nodo in nodi_ordinati:
            grado = self._model.grafo.degree(nodo)
            self._view.txt_result.controls.append(
                ft.Text(f"{nodo.surname} ({nodo.driver_id}) -- DoB: {nodo.dob} (grado={grado})"))

        # d) ESEMPIO NODO PIÙ INFLUENTE (Solo per grafi Orientati / DiGraph)
        # === Scommenta per stampare il nodo con bilancio Max (Uscenti - Entranti) ===
        # nodo_influente, score_influenza = self._model.get_nodo_piu_influente()
        # if nodo_influente is not None:
        #     self._view.txt_result.controls.append(
        #         ft.Text(f"Nodo più influente: {nodo_influente.nome} (Score: {score_influenza})", color="blue")
        #     )

        # 5. RIEMPIMENTO DELLA TENDINA NODI (TRUCCO LAMBDA E KEY)
        self._view.dd_nodo_scelto.options.clear()
        nodi_ordinati = list(self._model.grafo.nodes())
        nodi_ordinati.sort(key=lambda x: x.nome)

        for nodo in nodi_ordinati:
            self._view.dd_nodo_scelto.options.append(
                ft.dropdown.Option(
                    key=str(nodo.id_oggetto),
                    text=nodo.nome
                )
            )

        self._view.update_page()



    # =========================================================================
    # FASE 3: BOTTONE 2 - ANALISI / PERCORSI / RICORSIONE
    # =========================================================================
    def handle_ricerca_avanzata(self, e):
        id_nodo_selezionato = self._view.dd_nodo_scelto.value

        if id_nodo_selezionato is None:
            self._view.create_alert("Seleziona prima un nodo dalla tendina!")
            return

        self._view.txt_result.controls.clear()

        # ---------------------------------------------------------------------
        # SCEGLI L'OPZIONE IN BASE ALLA TRACCIA DELL'ESAME (A, B o C)
        # ---------------------------------------------------------------------

        # ---> OPZIONE A: Ricerca Raggiungibili (DFS)
        stati_raggiungibili = self._model.get_nodi_raggiungibili_dfs(id_nodo_selezionato)
        self._view.txt_result.controls.append(ft.Text(f"Trovati {len(stati_raggiungibili)} nodi:", color="blue"))
        for stato in stati_raggiungibili:
            self._view.txt_result.controls.append(ft.Text(f"- {stato.nome}"))


        # ---> OPZIONE B: Percorso Ottimo (Dijkstra)
        # id_nodo_destinazione = self._view.dd_destinazione.value
        # percorso = self._model.get_percorso_piu_breve(id_nodo_selezionato, id_nodo_destinazione)
        # if percorso is None:
        #     self._view.txt_result.controls.append(ft.Text("Nessun percorso trovato!"))
        # else:
        #     for nodo in percorso:
        #         self._view.txt_result.controls.append(ft.Text(f"-> {nodo.nome}"))



        # ---> OPZIONE C: Ricorsione di Ottimizzazione (Problema dello Zaino)
        # vincolo_1 = 100 # Es. leggi da un textfield
        # vincolo_2 = 50
        # percorso_ottimo, punteggio = self._model.calcola_percorso_ottimo(vincolo_1, vincolo_2)
        # self._view.txt_result.controls.append(ft.Text(f"Punteggio Massimo: {punteggio}", color="red", weight="bold"))
        # for nodo in percorso_ottimo:
        #     self._view.txt_result.controls.append(ft.Text(f"* {nodo.nome}"))


        # ---> OPZIONE D: Percorso con vincolo sui pesi (Es. Archi strettamente crescenti)
        # === Scommenta quando devi trovare un cammino in cui il peso degli archi ha una regola ===
        # percorso_vincolato, lunghezza_max = self._model.calcola_percorso_lungo_con_vincolo_archi(id_nodo_selezionato)
        # self._view.txt_result.controls.append(
        #     ft.Text(f"Trovato percorso lungo {lunghezza_max} nodi:", color="red", weight="bold")
        # )
        # for nodo in percorso_vincolato:
        #     # Usa l'attributo corretto del tuo DTO (es. nodo.nome, nodo.titolo, ecc.)
        #     self._view.txt_result.controls.append(ft.Text(f"-> {nodo.nome}"))



        # ---> OPZIONE E: Percorso con vincolo sulle proprietà dei Nodi (Es. Età decrescente)
        # === Scommenta quando la regola di avanzamento dipende dai dati dell'oggetto nodo ===
        # percorso_nodi, lunghezza_max = self._model.calcola_percorso_lungo_con_vincolo_nodi(id_nodo_selezionato)
        # self._view.txt_result.controls.append(
        #     ft.Text(f"Trovato percorso lungo {lunghezza_max} attori:", color="red", weight="bold")
        # )
        # for nodo in percorso_nodi:
        #     self._view.txt_result.controls.append(ft.Text(f"-> {nodo.nome} (Età: {nodo.eta})"))

        self._view.update_page()

        # ---> OPZIONE F: Percorso tra A e B di lunghezza fissa
        # === Scommenta quando devi andare da Start a End con un numero esatto di passi ===
        #
        # ⚠️ ATTENZIONE: Per usare questa opzione la tua View deve avere DUE tendine
        # (es. dd_nodo_scelto e dd_nodo_arrivo) e un TextField (es. txt_lunghezza)!
        #
        # id_arrivo = self._view.dd_nodo_arrivo.value
        # try:
        #     lun = int(self._view.txt_lunghezza.value)
        # except ValueError:
        #     self._view.create_alert("Inserisci una lunghezza numerica!")
        #     return
        #
        # percorso_esatto, max_peso = self._model.calcola_percorso_lunghezza_fissa(id_nodo_selezionato, id_arrivo, lun)
        # self._view.txt_result.controls.append(
        #     ft.Text(f"Trovato percorso con peso {max_peso}:", color="red", weight="bold")
        # )
        # for nodo in percorso_esatto:
        #     self._view.txt_result.controls.append(ft.Text(f"-> {nodo.nome}"))

    def handle_cerca_percorso_fisso(self, e):
        # ==========================================
        # 1. LETTURA E VALIDAZIONE INPUT
        # ==========================================
        # A. Recupero il nodo di partenza (es. dal menu a tendina)
        nodo_selezionato = self._view.dd_artisti.value
        if nodo_selezionato is None:
            self._view.create_alert("Attenzione: Seleziona prima un artista dal menu a tendina!")
            return

        # B. Recupero e valido la lunghezza inserita dall'utente
        valore_input = self._view.txt_lunghezza.value
        if not valore_input:
            self._view.create_alert("Attenzione: Inserisci una lunghezza per il percorso!")
            return

        try:
            lunghezza_input = int(valore_input)
            # Un cammino deve avere almeno un punto A e un punto B (lunghezza 2)
            if lunghezza_input < 2:
                self._view.create_alert("La lunghezza deve essere di almeno 2 nodi!")
                return
        except ValueError:
            self._view.create_alert("Attenzione: La lunghezza deve essere un numero intero valido!")
            return

        # ==========================================
        # 2. CHIAMATA AL MODEL E PULIZIA VIEW
        # ==========================================
        self._view.txt_result.controls.clear()

        # Chiamo la ricorsione passandogli il nodo (convertito se serve) e la lunghezza
        percorso_ottimo, peso_max = self._model.calcola_percorso_crescente_lunghezza_fissa(nodo_selezionato,
                                                                                           lunghezza_input)

        # Controllo se ha trovato qualcosa
        if not percorso_ottimo:
            self._view.txt_result.controls.append(
                ft.Text(f"Nessun percorso di lunghezza {lunghezza_input} trovato con pesi crescenti.", color="red")
            )
            self._view.update_page()
            return

        # ==========================================
        # 3. STAMPE DEI RISULTATI (Scegli quella richiesta dalla traccia)
        # ==========================================
        # Stampa dell'intestazione (Sempre utile)
        self._view.txt_result.controls.append(
            ft.Text(f"Trovato percorso ottimo! Peso totale: {peso_max}", color="green", weight="bold")
        )

        # -------------------------------------------------------------
        # VARIANTE A: Stampa Base (Solo la lista dei nodi in ordine)
        # "Stampare i nodi del percorso dal primo all'ultimo"
        # -------------------------------------------------------------
        self._view.txt_result.controls.append(ft.Text("Nodi attraversati:", weight="bold"))
        for nodo in percorso_ottimo:
            # Assicurati che l'oggetto nodo abbia il metodo __str__ impostato!
            self._view.txt_result.controls.append(ft.Text(f"-> {nodo}"))

        # -------------------------------------------------------------
        # VARIANTE B: Stampa Dettagliata (Nodi + Pesi dei singoli archi)
        # "Stampare l'elenco degli archi attraversati e il relativo peso"
        # -------------------------------------------------------------
        # self._view.txt_result.controls.append(ft.Text("Dettaglio Archi:", weight="bold"))
        # for i in range(len(percorso_ottimo) - 1):
        #     nodo_corrente = percorso_ottimo[i]
        #     nodo_successivo = percorso_ottimo[i + 1]
        #
        #     # Vado a pescare il peso specifico di questo arco dal grafo del model
        #     peso_arco = self._model.grafo[nodo_corrente][nodo_successivo]['weight']
        #
        #     self._view.txt_result.controls.append(
        #         ft.Text(f"{nodo_corrente} ---> {nodo_successivo} (Peso: {peso_arco})")
        #     )

        # -------------------------------------------------------------
        # VARIANTE C: Metriche Aggiuntive
        # "Stampare il numero totale di archi attraversati e i nodi estremi"
        # -------------------------------------------------------------
        # numero_archi = len(percorso_ottimo) - 1
        # nodo_partenza = percorso_ottimo[0]
        # nodo_arrivo = percorso_ottimo[-1]
        # self._view.txt_result.controls.append(
        #     ft.Text(f"Partenza: {nodo_partenza} | Arrivo: {nodo_arrivo} | Archi totali: {numero_archi}")
        # )

        # 4. Non dimenticare di aggiornare la UI alla fine!
        self._view.update_page()

        # -------------------------------------------------------------
        # STAMPA ORDINATA (Es. Ordine Alfabetico per Nome dell'Artista) da sostituire ad A
        # -------------------------------------------------------------
        self._view.txt_result.controls.append(ft.Text("Nodi attraversati (Ordinati alfabeticamente):", weight="bold"))

        # Uso sorted() e una lambda per dire a Python: "Ordina basandoti sull'attributo .nome dell'oggetto"
        # Se il prof chiede l'ordine DECRESCENTE, aggiungi reverse=True -> sorted(..., reverse=True)
        nodi_ordinati = sorted(percorso_ottimo, key=lambda nodo: nodo.nome)

        for nodo in nodi_ordinati:
            self._view.txt_result.controls.append(ft.Text(f"- {nodo}"))




    def handle_cerca_percorso_crescente_peso(self, e):
        # ==========================================
        # 1. LETTURA INPUT (Nodo di partenza)
        # ==========================================
        nodo_selezionato = self._view.dd_artisti.value
        if nodo_selezionato is None:
            self._view.create_alert("Attenzione: Seleziona prima un artista dal menu!")
            return

        # ==========================================
        # 2. GESTIONE CASO 2 vs CASO 3
        # ==========================================
        # Leggo cosa ha scritto l'utente nella casella della lunghezza
        valore_input = self._view.txt_lunghezza.value
        lunghezza_massima = None  # Di default parto presupponendo il CASO 2

        # Se l'utente ha scritto qualcosa, allora siamo nel CASO 3!
        if valore_input:
            try:
                lunghezza_massima = int(valore_input)
                if lunghezza_massima < 2:
                    self._view.create_alert("La lunghezza massima deve essere almeno 2!")
                    return
            except ValueError:
                self._view.create_alert("Inserisci un numero intero valido per la lunghezza!")
                return

        # ==========================================
        # 3. CHIAMATA AL MODEL
        # ==========================================
        self._view.txt_result.controls.clear()

        # Passo il nodo e la lunghezza_massima (che sarà un numero per il Caso 3, o 'None' per il Caso 2)
        percorso_ottimo, peso_max = self._model.calcola_percorso_crescente_max_peso(
            nodo_selezionato,
            lunghezza_max=lunghezza_massima
        )

        # ==========================================
        # 4. STAMPA DEI RISULTATI
        # ==========================================
        if not percorso_ottimo:
            self._view.txt_result.controls.append(
                ft.Text("Nessun percorso trovato con le condizioni richieste.", color="red")
            )
            self._view.update_page()
            return

        # Intestazione con il risultato vincente
        self._view.txt_result.controls.append(
            ft.Text(f"Trovato percorso ottimo! Peso totale massimo: {peso_max}", color="green", weight="bold")
        )

        # Stampa dei nodi (In ordine naturale di cammino)
        self._view.txt_result.controls.append(ft.Text("Nodi attraversati:", weight="bold"))
        for nodo in percorso_ottimo:
            # Stampa l'oggetto (richiede che l'oggetto abbia il metodo __str__)
            self._view.txt_result.controls.append(ft.Text(f"-> {nodo}"))

        # (Opzionale) Se il prof chiede di stampare anche i pesi degli archi attraversati
        # self._view.txt_result.controls.append(ft.Text("\nDettaglio archi attraversati:", weight="bold"))
        # for i in range(len(percorso_ottimo) - 1):
        #     u = percorso_ottimo[i]
        #     v = percorso_ottimo[i+1]
        #     peso_arco = self._model.grafo[u][v]['weight']
        #     self._view.txt_result.controls.append(ft.Text(f"{u} ---> {v} (Peso: {peso_arco})"))

        self._view.update_page()

