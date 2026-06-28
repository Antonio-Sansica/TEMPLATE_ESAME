import heapq
from dataclasses import dataclass
from enum import Enum


# =============================================================================
# 1. DEFINIZIONE DEI TIPI DI EVENTO
# =============================================================================
class TipoEvento(Enum):
    ARRIVO_CLIENTE = 1
    FINE_SERVIZIO = 2
    # Aggiungi qui altri eventi in base alla traccia


# =============================================================================
# 2. STRUTTURA DELL'EVENTO (Da mettere in coda)
# =============================================================================
@dataclass(order=True)
class Evento:
    # ATTENZIONE: Il "tempo" (o la data) DEVE essere il primo attributo!
    # heapq usa il primo attributo per mettere in ordine cronologico gli eventi.
    tempo: int
    tipo: TipoEvento

    # Aggiungi qui chi subisce l'evento (es. un ID, un oggetto Cliente, un volo...)
    # nodo_coinvolto: object = field(compare=False) # Usa compare=False per non far impazzire l'ordinamento


# =============================================================================
# 3. IL MOTORE DEL SIMULATORE
# =============================================================================
class Simulatore:
    def __init__(self):
        # La "Linea del tempo" (Coda di priorità)
        self.coda_eventi = []

        # --- STATO DEL SISTEMA (Es. quante casse sono aperte, posti liberi...) ---
        self.risorse_disponibili = 10

        # --- STATISTICHE FINALI (I risultati che stampi a schermo) ---
        self.clienti_serviti = 0
        self.clienti_rifiutati = 0

    def inizializza(self, parametro_iniziale):
        """Pulisce tutto e inserisce i primissimi eventi nella linea del tempo."""
        self.coda_eventi = []
        self.clienti_serviti = 0
        self.clienti_rifiutati = 0
        self.risorse_disponibili = parametro_iniziale

        # ESEMPIO: Faccio arrivare il primo cliente al minuto 0
        # primo_evento = Evento(tempo=0, tipo=TipoEvento.ARRIVO_CLIENTE)
        # heapq.heappush(self.coda_eventi, primo_evento)

    def run(self):
        """Il ciclo infinito che fa scorrere il tempo finché ci sono eventi."""
        while len(self.coda_eventi) > 0:
            # Estraggo l'evento più imminente (quello col tempo minore)
            evento_corrente = heapq.heappop(self.coda_eventi)
            # Lo faccio accadere!
            self._processa_evento(evento_corrente)

    def _processa_evento(self, e: Evento):
        """Smista l'evento e modifica lo stato del sistema."""

        if e.tipo == TipoEvento.ARRIVO_CLIENTE:
            # Cosa succede quando arriva qualcuno?
            if self.risorse_disponibili > 0:
                self.risorse_disponibili -= 1
                self.clienti_serviti += 1

                # Genero un NUOVO evento nel futuro (es. il servizio finisce tra 15 minuti)
                # nuovo_evento = Evento(tempo=e.tempo + 15, tipo=TipoEvento.FINE_SERVIZIO)
                # heapq.heappush(self.coda_eventi, nuovo_evento)
            else:
                self.clienti_rifiutati += 1

        elif e.tipo == TipoEvento.FINE_SERVIZIO:
            # Cosa succede quando il servizio finisce?
            # La risorsa torna libera!
            self.risorse_disponibili += 1