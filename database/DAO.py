from database.DB_connect import DBConnect


# from model.template_dto import MioOggettoDTO  <-- Ricordati di scommentare e importare il tuo vero DTO!

class DAO:

    # =====================================================================================
    # 1. METODO BASE: ESTRARRE TUTTI GLI OGGETTI
    # === QUANDO USARLA ===
    # All'avvio del programma per riempire l'Identity Map nel Model, oppure per riempire
    # le tendine (Dropdown) dell'interfaccia grafica con tutti gli elementi del DB.
    # === COME USARLA ===
    # Chiama DAO.get_tutti_gli_oggetti(). Restituisce una lista di oggetti DTO completi.
    # =====================================================================================
    @staticmethod
    def get_tutti_gli_oggetti():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None: return result
        try:
            # dictionary=True è OBBLIGATORIO per usare row['NOME_COLONNA']
            cursor = cnx.cursor(dictionary=True)

            # DISTINCT evita doppioni. ORDER BY è utile se devi mostrare i dati in una tendina
            query = "SELECT DISTINCT * FROM tabella ORDER BY id"
            cursor.execute(query)

            for row in cursor:
                # Creiamo l'oggetto DTO "mattoncino" usando i dati del dizionario
                oggetto = MioOggettoDTO(
                    id=row['ID'],
                    nome=row['NOME'],
                    valore=row['VALORE']
                )
                # Se la tua tabella drivers ha tantissime colonne e hai chiamato gli attributi
                # nel dataclass del DTO esattamente come le colonne del database, c'è una scorciatoia
                # potentissima (il dictionary unpacking) per risparmiare 10 righe di codice per ogni DTO:
                #
                # oggetto = MioOggettoDTO(**row)
                result.append(oggetto)

            return result
        except Exception as e:
            print(f"Errore DAO estrazione base: {e}")
            return []
        finally:
            cursor.close()
            cnx.close()

    # =====================================================================================
    # 2. METODO AVANZATO: FILTRI OPZIONALI E AGGREGAZIONI (SUM, COUNT, AVG)
    # === QUANDO USARLA ===
    # Quando l'utente inserisce dei filtri (es. Anno, Categoria) e preme un bottone per
    # calcolare una media, un conteggio totale o una somma.
    # === COME USARLA ===
    # Restituisce UNA SOLA RIGA (dizionario), quindi usiamo fetchone() invece del ciclo for!
    # =====================================================================================
    @staticmethod
    def get_dati_filtrati_aggregati(filtro_1, filtro_2):
        cnx = DBConnect.get_connection()
        if cnx is None: return None
        try:
            cursor = cnx.cursor(dictionary=True)

            # TRUCCO COALESCE: Se dal Controller passi 'None' come filtro_1, SQL ignora il filtro!
            # È perfetto per i menu a tendina "opzionali".
            query = """
                SELECT 
                    SUM(valore_a) AS somma_totale,
                    COUNT(*) AS numero_righe
                FROM tabella
                WHERE 
                    colonna_1 = COALESCE(%s, colonna_1)
                    AND colonna_2 = COALESCE(%s, colonna_2)
            """
            # Attenzione: l'ordine dei parametri deve essere identico all'ordine dei %s
            cursor.execute(query, (filtro_1, filtro_2))

            # Restituiamo direttamente l'unica riga trovata (es. {'somma_totale': 100, 'numero_righe': 5})
            return cursor.fetchone()

        except Exception as e:
            print(f"Errore DAO filtri aggregati: {e}")
            return None
        finally:
            cursor.close()
            cnx.close()

    # =====================================================================================
    # 3. METODO GRAFO (NODI): LA "LISTA DEGLI INVITATI" (IL PARADOSSO DELL'AUSTRALIA)
    # === QUANDO USARLA ===
    # Quando la traccia chiede di mettere nel grafo SOLO i nodi che rispettano una certa
    # condizione (es. "solo gli stati esistenti in quell'anno", Lab 10).
    # === COME USARLA ===
    # Restituisce una lista di semplici ID (numeri o stringhe), non oggetti interi!
    # =====================================================================================
    @staticmethod
    def get_id_nodi_validi(filtro_anno):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None: return []
        try:
            cursor = cnx.cursor(dictionary=True)

            # TRUCCO UNION: Unisce le due colonne di un collegamento scartando i doppioni.
            # Ottimo per dire "Dammi tutti gli ID coinvolti in almeno un collegamento valido".
            query = """
                SELECT id_origine AS id_valido FROM tabella_collegamenti WHERE anno <= %s
                UNION
                SELECT id_destinazione AS id_valido FROM tabella_collegamenti WHERE anno <= %s
            """
            # Passo due volte il parametro perché ci sono due %s nella query
            cursor.execute(query, (filtro_anno, filtro_anno))

            for row in cursor:
                result.append(row['id_valido'])

            return result

        except Exception as e:
            print(f"Errore DAO ID Nodi Grafo: {e}")
            return []
        finally:
            cursor.close()
            cnx.close()

    # =====================================================================================
    # 4. METODO GRAFO (ARCHI): "LE STRADE" E IL TRUCCO NINJA (GRAFO NON ORIENTATO E PESATO)
    # === QUANDO USARLA ===
    # SEMPRE, ogni volta che devi tracciare gli archi di un grafo non orientato leggendo da
    # un database che salva i voli "A->B" e "B->A" come righe separate.
    # === COME USARLA ===
    # Restituisce una lista di tuple: [(ID_1, ID_2, peso), (ID_1, ID_2, peso), ...]
    # =====================================================================================
    @staticmethod
    def get_archi_grafo_pesato(soglia_minima):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None: return []
        try:
            cursor = cnx.cursor(dictionary=True)

            # TRUCCO NINJA LEAST/GREATEST:
            # Forza l'ID più piccolo a stare a sinistra, e il più grande a destra.
            # In questo modo "Roma-Milano" e "Milano-Roma" diventano la stessa identica coppia!
            # AVG/SUM/COUNT fondono i dati di andata e ritorno in un unico 'peso_arco'.
            query = """
                SELECT 
                    LEAST(t.id_partenza, t.id_arrivo) AS id_1, 
                    GREATEST(t.id_partenza, t.id_arrivo) AS id_2, 
                    AVG(t.valore) AS peso_arco
                FROM tabella_collegamenti t
                GROUP BY 
                    LEAST(t.id_partenza, t.id_arrivo), 
                    GREATEST(t.id_partenza, t.id_arrivo)
                HAVING peso_arco > %s
            """

            cursor.execute(query, (soglia_minima,))

            for row in cursor:
                # Appendo una TUPLA con i tre dati fondamentali per tracciare l'arco pesato
                result.append((row['id_1'], row['id_2'], row['peso_arco']))

            return result

        except Exception as e:
            print(f"Errore DAO estrazione archi: {e}")
            return []
        finally:
            cursor.close()
            cnx.close()