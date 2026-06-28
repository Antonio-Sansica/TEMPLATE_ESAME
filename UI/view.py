import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        self._page.title = "Esame TdP - Template Grafi"
        self._page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self._page.theme_mode = ft.ThemeMode.LIGHT

        self._controller = None

        # =====================================================================
        # 1. DICHIARAZIONE DEI COMPONENTI (Le "scatole vuote")
        # =====================================================================
        self.title_label = None

        # --- Input Utente (Fase 1: Creazione Grafo) ---
        self.txt_input = None  # Per anni, pesi o distanze
        self.dd_filtro_base = None  # (Opzionale) se il filtro è a tendina
        self.btn_crea_grafo = None

        # --- Input Utente (Fase 2: Esplorazione Grafo) ---
        self.dd_nodo_scelto = None  # Tendina per selezionare il nodo di partenza
        self.btn_analizza = None  # Bottone per DFS, Componenti, ecc.

        # --- Output ---
        self.txt_result = None  # La lista dove stamperemo i risultati

    # =========================================================================
    # METODI DI SET-UP
    # =========================================================================
    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    # =========================================================================
    # CREAZIONE DELL'INTERFACCIA GRAFICA
    # =========================================================================
    def load_interface(self):
        # 1. IL TITOLO
        self.title_label = ft.Text("Gestione Grafi e Percorsi", size=26, color="blue", weight="bold")

        # ---------------------------------------------------------------------
        # 2. COMPONENTI FASE 1 (Costruzione del Grafo)
        # ---------------------------------------------------------------------
        self.txt_input = ft.TextField(
            label="Inserisci Parametro (Es. Anno/Peso)",
            width=250,
            hint_text="Es: 2015"
        )

        # (Opzionale: scommentala se la traccia ti fa scegliere un filtro base invece di scriverlo)
        # self.dd_filtro_base = ft.Dropdown(label="Filtro Iniziale", width=250)

        self.btn_crea_grafo = ft.ElevatedButton(
            text="Crea Grafo",
            on_click=self._controller.handle_crea_grafo  # <-- Chiama il Controller!
        )

        riga_fase_1 = ft.Row(
            controls=[self.txt_input, self.btn_crea_grafo],  # Aggiungi self.dd_filtro_base se lo usi
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        )

        # ---------------------------------------------------------------------
        # 3. COMPONENTI FASE 2 (Esplorazione del Grafo)
        # ---------------------------------------------------------------------
        # Questa tendina viene riempita dal Controller DOPO aver cliccato "Crea Grafo"
        self.dd_nodo_scelto = ft.Dropdown(
            label="Seleziona Nodo di Partenza",
            width=350,
        )

        self.btn_analizza = ft.ElevatedButton(
            text="Analizza / Trova Percorso",
            on_click=self._controller.handle_ricerca_avanzata  # <-- Chiama il Controller!
        )

        riga_fase_2 = ft.Row(
            controls=[self.dd_nodo_scelto, self.btn_analizza],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        )

        # ---------------------------------------------------------------------
        # 4. AREA DEI RISULTATI
        # ---------------------------------------------------------------------
        # ListView per creare lo scorrimento se ci sono centinaia di risultati
        self.txt_result = ft.ListView(expand=1, spacing=5, padding=10, auto_scroll=False)

        # Contenitore elegante per limitare l'altezza e mettere i bordi
        area_output_con_bordo = ft.Container(
            content=self.txt_result,
            border=ft.border.all(1, ft.colors.BLUE_GREY_200),
            border_radius=10,
            height=300,
            expand=True
        )

        # ---------------------------------------------------------------------
        # 5. MONTAGGIO SULLA PAGINA
        # ---------------------------------------------------------------------
        self._page.controls.append(self.title_label)
        self._page.controls.append(ft.Container(height=10))
        self._page.controls.append(riga_fase_1)
        self._page.controls.append(ft.Container(height=10))
        self._page.controls.append(riga_fase_2)
        self._page.controls.append(ft.Container(height=10))
        self._page.controls.append(area_output_con_bordo)

        self._page.update()

        # ---------------------------------------------------------------------
        # 6. AZIONI AUTOMATICHE ALL'AVVIO
        # ---------------------------------------------------------------------
        # Se la traccia chiede di popolare una tendina all'avvio del programma, scommenta:
        # self._controller.populate_dd_iniziali()

    # =========================================================================
    # METODI DI UTILITÀ (Scorciatoie per il Controller)
    # =========================================================================
    def update_page(self):
        self._page.update()

    def create_alert(self, message):
        """Crea un comodo Pop-up di errore a schermo (es. 'Inserisci un numero!')"""
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()