from dataclasses import dataclass

@dataclass
class MioOggettoDTO:
    # =========================================================================
    # 1. ATTRIBUTI DEL DATABASE
    # =========================================================================
    # Devono corrispondere alle colonne della tabella (anche se i nomi variano).
    # Assicurati di usare i tipi di dato corretti (int, str, float).
    id_oggetto: int
    nome: str
    valore_a: float
    valore_b: float

    # =========================================================================
    # 2. PROPRIETÀ CALCOLATE (TRUCCO ESAME)
    # === QUANDO USARLA ===
    # Se la traccia chiede di stampare o usare un valore che non esiste nel DB,
    # ma si calcola partendo da altri campi (es. "Densità" = Popolazione / Area).
    # === COME USARLA ===
    # Nel codice la chiami normalmente SENZA parentesi: print(oggetto.valore_totale)
    # =========================================================================
    @property
    def valore_totale(self):
        return self.valore_a * self.valore_b


    # =========================================================================
    # 3. METODO DI STAMPA (__str__)
    # === QUANDO USARLA ===
    # Sempre. Definisce come apparirà l'oggetto quando lo inserisci in una tendina
    # di Flet o lo stampi nell'interfaccia.
    # =========================================================================
    def __str__(self):
        return f"[{self.id_oggetto}] {self.nome} - Totale: {self.valore_totale}"

    # =========================================================================
    # 4. I METODI MAGICI (__eq__ e __hash__) - FONDAMENTALI PER I GRAFI!
    # === QUANDO USARLA ===
    # SEMPRE. NetworkX usa i Set e i Dizionari dietro le quinte. Se non metti
    # questi due metodi, NetworkX non capirà se due nodi sono uguali o diversi,
    # e creerà doppioni o non traccerà gli archi!
    # =========================================================================
    def __eq__(self, other):
        # SICUREZZA: Controllo che 'other' sia davvero un oggetto di questa classe.
        # Evita i crash se confronti l'oggetto con una stringa o con None.
        if isinstance(other, MioOggettoDTO):
            return self.id_oggetto == other.id_oggetto
        return False

    def __hash__(self):
        return hash(self.id_oggetto)

    # -------------------------------------------------------------------------
    # EMERGENZA ESAME: CHIAVE PRIMARIA COMPOSTA
    # === QUANDO USARLA ===
    # Se la tabella del DB usa due colonne per fare la chiave primaria (es. ID + Anno).
    # (Scommenta questo blocco e cancella quello sopra).
    # -------------------------------------------------------------------------
    # def __eq__(self, other):
    #     if isinstance(other, MioOggettoDTO):
    #         # Le metto tra parentesi tonde per confrontarle come se fossero una tupla!
    #         return (self.id_1, self.id_2) == (other.id_1, other.id_2)
    #     return False
    #
    # def __hash__(self):
    #     # La doppia parentesi è d'obbligo: fai l'hash di una singola tupla (id1, id2)
    #     return hash((self.id_1, self.id_2))
    # -------------------------------------------------------------------------

    @property
    def eta(self):
        """
        Metodo @property inserito nel DTO per calcolare l'età esatta dell'attore ad oggi.
        Gestisce matematicamente il giorno e il mese di nascita per evitare scarti di un anno.
        """
        # 1. Recupero la data esatta di oggi (anno, mese, giorno)
        oggi = date.today()

        # 2. Estraggo anno, mese e giorno di nascita dall'oggetto date dell'attore
        anno_nascita = self.date_of_birth.year
        mese_nascita = self.date_of_birth.month
        giorno_nascita = self.date_of_birth.day

        # 3. Calcolo iniziale della differenza basato puramente sull'anno
        eta_calcolata = oggi.year - anno_nascita

        # 4. IL TRUCCO DEL COMPLEANNO (Fondamentale per l'esame):
        # Confronterò due tuple: (mese_corrente, giorno_corrente) e (mese_nascita, giorno_nascita).
        # In Python, le tuple si confrontano elemento per elemento.
        # Se la tupla di OGGI è MINORE di quella di NASCITA, significa che l'anno corrente
        # è andato avanti ma l'attore NON ha ancora festeggiato il compleanno.
        if (oggi.month, oggi.day) < (mese_nascita, giorno_nascita):
            eta_calcolata -= 1  # Sottoraggo un anno perché deve ancora compierli!

        return eta_calcolata