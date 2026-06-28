import flet as ft

# =============================================================================
# IMPORTIAMO I 3 PILASTRI DELL'ARCHITETTURA MVC
# (Attenzione: all'esame ricordati di usare i nomi corretti dei tuoi file!)
# =============================================================================
from model.template_model_GRAFO import ModelGrafo  # O semplicemente 'Model' se si chiama così
from UI.template_view import View
from UI.template_controller import Controller

def main(page: ft.Page):
    """
    IL DIRETTORE D'ORCHESTRA.
    Il suo unico scopo è creare gli oggetti e presentarli l'uno all'altro.
    NON deve mai importare o toccare il DAO o le logiche di calcolo!
    """

    # STEP 1: Creiamo il Model (Il cervello dei dati e dei grafi)
    my_model = ModelGrafo()

    # STEP 2: Creiamo la View (La grafica, passandole la 'page' di Flet)
    my_view = View(page)

    # STEP 3: Creiamo il Controller (Il vigile urbano che smista le richieste)
    # Gli passiamo sia la View che il Model così può farli parlare tra loro!
    my_controller = Controller(my_view, my_model)

    # STEP 4: Diamo alla View il "numero di telefono" del Controller.
    # Questo è FONDAMENTALE per far funzionare i bottoni (es. on_click=self._controller.azione)
    my_view.set_controller(my_controller)

    # STEP 5: Ora che tutti si conoscono, accendiamo l'interfaccia!
    # Questo metodo disegna fisicamente i bottoni e le tendine sullo schermo.
    my_view.load_interface()

# Comando standard di Flet per far partire l'applicazione desktop
ft.app(target=main)