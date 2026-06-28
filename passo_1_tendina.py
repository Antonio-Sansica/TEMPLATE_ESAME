# =========================================================================
# 🚀 PASSO 1: POPOLAMENTO TENDINE (MANUALE DI SOPRAVVIVENZA)
# =========================================================================
# 🛑 CHECKLIST ANTI-CRASH (Controlla queste 5 cose prima di impazzire):
# 1. SQL: Hai usato DISTINCT (no doppioni) e ORDER BY (lista ordinata) nella query?
# 2. FLET: Hai impostato key=str(...) nel Controller? (Flet vuole le stringhe!)
# 3. FLET: Hai chiamato self._view.update_page() alla fine del ciclo nel Controller?
# 4. VIEW: In fondo a load_interface(), c'è self._controller.populate_dd_iniziali()?
# 5. DAO: Con dictionary=True, hai scritto i nomi colonna esattamente uguali al DB?
# =========================================================================

# -------------------------------------------------------------------------
# 1. FILE: model/dto.py (Solo se la tendina mostra oggetti complessi)
# -------------------------------------------------------------------------
from dataclasses import dataclass


@dataclass
class OggettoTendina:
    id_univoco: int
    nome_display: str

    def __str__(self):
        # Definisce come appare l'oggetto testualmente (fallback se non usi 'text')
        return f"{self.nome_display}"


# -------------------------------------------------------------------------
# 2. FILE: database/DAO.py (L'estrattore SQL)
# -------------------------------------------------------------------------
class DAO:
    @staticmethod
    def get_dati_tendina():
        # cnx = DBConnect.get_connection()
        # cursor = cnx.cursor(dictionary=True)

        # 🚨 REGOLA AUREA: Sempre DISTINCT e ORDER BY
        # query = "SELECT DISTINCT colonna_id, colonna_nome FROM tabella ORDER BY colonna_nome"
        # cursor.execute(query)

        # result = []
        # for row in cursor:
        #     # Se usi il DTO: result.append(OggettoTendina(**row))
        #     # Se è un valore semplice (es. Anni): result.append(row['anno'])
        # return result
        pass


# -------------------------------------------------------------------------
# 3. FILE: model/model.py (Il ponte)
# -------------------------------------------------------------------------
class Model:
    def get_dati_tendina(self):
        # Il Model passa semplicemente la palla dal DAO al Controller
        return DAO.get_dati_tendina()


# -------------------------------------------------------------------------
# 4. FILE: UI/view.py (La vetrina)
# -------------------------------------------------------------------------
import flet as ft


class View:
    def load_interface(self):
        # 1. Dichiaro l'oggetto grafico
        self.dd_filtro = ft.Dropdown(label="Seleziona...", width=300)
        # (Codice per fare l'append di dd_filtro alla pagina o a una Row...)

        # 🚨 FONDAMENTALE: In fondo a questo metodo, do il via al caricamento dati!
        # self._controller.populate_dd_iniziali()
        # self._page.update()


# -------------------------------------------------------------------------
# 5. FILE: UI/controller.py (Il Regista - QUI AVVIENE LA MAGIA)
# -------------------------------------------------------------------------
class Controller:

    def populate_dd_iniziali(self):
        # 1. PULIZIA: Svuoto la tendina per evitare duplicati in caso di riavvii
        self._view.dd_filtro.options.clear()

        # 2. CHIAMATA AL MODEL: Scarico i dati
        dati = self._model.get_dati_tendina()

        # 3. CICLO E RIEMPIMENTO DELLA TENDINA
        for dato in dati:
            # 🚨 TRANELLO KEY vs TEXT:
            # - key: Valore nascosto letto dal PC. OBBLIGATORIAMENTE STRINGA -> str()
            # - text: Quello che l'utente legge a schermo.

            # ---> SCENARIO A: Valori Semplici (es. "2015", "Italia")
            # self._view.dd_filtro.options.append(
            #     ft.dropdown.Option(key=str(dato), text=str(dato))
            # )

            # ---> SCENARIO B: Oggetti Complessi (es. DTO Categoria)
            self._view.dd_filtro.options.append(
                ft.dropdown.Option(
                    key=str(dato.id_univoco),
                    text=dato.nome_display
                )
            )

        # 4. AGGIORNAMENTO: Dico alla scheda video di ridisegnare la pagina
        self._view.update_page()

    def handle_bottone_crea_grafo(self, e):
        # === COME LEGGERE IL VALORE SCELTO DALL'UTENTE ===

        # 1. Leggo la KEY nascosta (ATTENZIONE: Flet la restituisce SEMPRE come stringa)
        valore_selezionato_str = self._view.dd_filtro.value

        # 2. Controllo Anti-Crash (l'utente ha cliccato senza scegliere)
        if valore_selezionato_str is None:
            self._view.create_alert("Seleziona un elemento dalla tendina!")
            return

        # 3. Trasformo la stringa di nuovo in numero (se il mio ID è intero)
        # id_selezionato = int(valore_selezionato_str)

        # 4. Procedo con la creazione del grafo...
        pass