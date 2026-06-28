# =================================================================================================
# 📚 ARSENALE DELLE QUERY SQL PER L'ESAME
# =================================================================================================
# ISTRUZIONI PER L'USO:
# 1. Trova la query che assomiglia di più alla richiesta della traccia.
# 2. Copia il blocco di codice nel tuo VERO DAO.py.
# 3. Cambia NOME_TABELLA e NOME_COLONNA con quelli reali del tuo database.
# 4. Assicurati di importare e usare il tuo VERO DTO al posto di 'MioOggettoDTO'.
# =================================================================================================

from database.DB_connect import DBConnect

class TemplateDAO:

    # =====================================================================================
    # LIVELLO 1: LE TENDINE E I DATI BASE (Estrazioni Semplici)
    # =====================================================================================

    # 1A. RIEMPIRE UNA TENDINA CON VALORI UNICI (Es. Tutti gli anni, tutte le categorie)
    # === QUANDO USARLA === All'avvio dell'app per popolare i menu a tendina.
    # === COME USARLA === Usa DISTINCT per evitare doppioni e ORDER BY per l'estetica.
    @staticmethod
    def get_valori_per_tendina():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None: return result
        cursor = None
        try:
            cursor = cnx.cursor(dictionary=True)
            # Modifica 'anno' e 'tabella_gare'
            query = "SELECT DISTINCT anno FROM tabella_gare ORDER BY anno DESC"
            cursor.execute(query)
            for row in cursor:
                result.append(row["anno"])
            return result
        except Exception as e:
            print(e)
            return []
        finally:
            if cursor is not None: cursor.close()
            cnx.close()


    # =====================================================================================
    # LIVELLO 2: ESTRAZIONE DEI NODI DEL GRAFO
    # =====================================================================================

    # 2A. NODI CON FILTRO SEMPLICE (Es. "Tutti i piloti nati dopo il 1980")
    # === QUANDO USARLA === Se i nodi del grafo dipendono da 1 o 2 parametri dell'utente.
    @staticmethod
    def get_nodi_filtrati(param1, param2):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None: return result
        cursor = None
        try:
            cursor = cnx.cursor(dictionary=True)
            # BETWEEN gestisce i range. Usa %s come segnaposto!
            query = """
                SELECT * FROM tabella_nodi 
                WHERE colonna_filtro BETWEEN %s AND %s
            """
            cursor.execute(query, (param1, param2))
            for row in cursor:
                # result.append(MioOggettoDTO(**row)) # Scorciatoia se i nomi combaciano
                pass
            return result
        except Exception as e:
            print(e)
            return []
        finally:
            if cursor is not None: cursor.close()
            cnx.close()

    # 2B. NODI CON JOIN SU 3 TABELLE (L'incubo della traccia di solito)
    # === QUANDO USARLA === "I nodi sono i Piloti che hanno corso in un Circuito in un certo Anno"
    # === COME USARLA === Usa DISTINCT perché un pilota corre tante gare, ma nel grafo ci va 1 sola volta!
    @staticmethod
    def get_nodi_con_join_multipla(filtro_anno):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None: return result
        cursor = None
        try:
            cursor = cnx.cursor(dictionary=True)
            query = """
                SELECT DISTINCT n.* FROM tabella_nodi n, tabella_ponte p, tabella_filtro f
                WHERE n.id_nodo = p.id_nodo 
                  AND p.id_filtro = f.id_filtro
                  AND f.anno = %s
            """
            cursor.execute(query, (filtro_anno,))
            for row in cursor:
                # result.append(MioOggettoDTO(**row))
                pass
            return result
        except Exception as e:
            print(e)
            return []
        finally:
            if cursor is not None: cursor.close()
            cnx.close()


    # =====================================================================================
    # LIVELLO 3: ESTRAZIONE DEGLI ARCHI (LE STRADE DEL GRAFO)
    # =====================================================================================

    # 3A. ARCHI GRAFO NON ORIENTATO E NON PESATO (Solo collegamenti)
    # === QUANDO USARLA === "Due nodi sono collegati se hanno condiviso almeno un evento"
    # === TRUCCO NINJA === n1.id < n2.id evita di avere (A-B) e (B-A) e impedisce i self-loop (A-A).
    @staticmethod
    def get_archi_non_pesati(parametro):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None: return result
        cursor = None
        try:
            cursor = cnx.cursor(dictionary=True)
            query = """
                SELECT DISTINCT p1.id_nodo AS id1, p2.id_nodo AS id2
                FROM tabella_ponte p1, tabella_ponte p2
                WHERE p1.id_evento = p2.id_evento 
                  AND p1.id_nodo < p2.id_nodo
                  AND p1.anno = %s
            """
            cursor.execute(query, (parametro,))
            for row in cursor:
                result.append((row['id1'], row['id2'])) # Restituisce tuple (Nodo1, Nodo2)
            return result
        except Exception as e:
            print(e)
            return []
        finally:
            if cursor is not None: cursor.close()
            cnx.close()

    # 3B. ARCHI GRAFO NON ORIENTATO E PESATO (Il grande classico dell'esame)
    # === QUANDO USARLA === "Il peso dell'arco è il NUMERO DI VOLTE che hanno corso insieme"
    # === COME USARLA === Aggiungi GROUP BY e COUNT(*) o SUM(). Non serve il DISTINCT qui!
    @staticmethod
    def get_archi_pesati_conteggio():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None: return result
        cursor = None
        try:
            cursor = cnx.cursor(dictionary=True)
            query = """
                SELECT 
                    p1.id_nodo AS id1, 
                    p2.id_nodo AS id2, 
                    COUNT(*) AS peso 
                FROM tabella_ponte p1, tabella_ponte p2
                WHERE p1.id_evento = p2.id_evento 
                  AND p1.id_nodo < p2.id_nodo
                GROUP BY id1, id2
            """
            cursor.execute(query)
            for row in cursor:
                result.append((row['id1'], row['id2'], row['peso'])) # Tupla a 3: N1, N2, Peso
            return result
        except Exception as e:
            print(e)
            return []
        finally:
            if cursor is not None: cursor.close()
            cnx.close()

    # 3C. ARCHI CON FILTRO SUL PESO MINIMO (La clausola HAVING)
    # === QUANDO USARLA === "Traccia l'arco SOLO SE hanno corso insieme ALMENO X volte"
    # === COME USARLA === Metti HAVING dopo il GROUP BY. Non puoi usare WHERE per filtrare i COUNT!
    @staticmethod
    def get_archi_pesati_con_soglia(soglia_minima):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None: return result
        cursor = None
        try:
            cursor = cnx.cursor(dictionary=True)
            query = """
                SELECT 
                    p1.id_nodo AS id1, 
                    p2.id_nodo AS id2, 
                    COUNT(*) AS peso 
                FROM tabella_ponte p1, tabella_ponte p2
                WHERE p1.id_evento = p2.id_evento 
                  AND p1.id_nodo < p2.id_nodo
                GROUP BY id1, id2
                HAVING peso >= %s
            """
            cursor.execute(query, (soglia_minima,))
            for row in cursor:
                result.append((row['id1'], row['id2'], row['peso']))
            return result
        except Exception as e:
            print(e)
            return []
        finally:
            if cursor is not None: cursor.close()
            cnx.close()


    # =====================================================================================
    # LIVELLO 4: LE QUERY "AMMAZZA-ESAME" (Avanzate)
    # =====================================================================================

    # 4A. LA SOTTOQUERY (Filtrare confrontando con la Media Globale)
    # === QUANDO USARLA === "Seleziona i piloti che hanno vinto PIÙ DELLA MEDIA di tutti i piloti"
    # === COME USARLA === Si fa una SELECT dentro un'altra SELECT (fra parentesi).
    @staticmethod
    def get_nodi_sopra_media():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None: return result
        cursor = None
        try:
            cursor = cnx.cursor(dictionary=True)
            query = """
                SELECT * FROM piloti p
                WHERE p.vittorie > (
                    SELECT AVG(vittorie) FROM piloti
                )
            """
            cursor.execute(query)
            for row in cursor:
                pass
            return result
        except Exception as e:
            print(e)
            return []
        finally:
            if cursor is not None: cursor.close()
            cnx.close()

    # 4B. LA TABELLA DI COLLEGAMENTO ESPLICITA (Quando hai Partenza e Arrivo in una riga)
    # === QUANDO USARLA === Se il DB ha già una tabella tipo "Voli" con "Aeroporto_Partenza" e "Aeroporto_Arrivo".
    # === IL PROBLEMA === Il volo Roma->Milano e Milano->Roma sono due righe, ma il grafo NON è orientato.
    # === TRUCCO NINJA === Si usa LEAST e GREATEST per fondere i due sensi di marcia in un unico arco pesato!
    @staticmethod
    def get_archi_da_tabella_diretta():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None: return result
        cursor = None
        try:
            cursor = cnx.cursor(dictionary=True)
            query = """
                SELECT 
                    LEAST(partenza_id, arrivo_id) AS id1,
                    GREATEST(partenza_id, arrivo_id) AS id2,
                    SUM(passeggeri) AS peso_totale
                FROM voli
                GROUP BY id1, id2
            """
            cursor.execute(query)
            for row in cursor:
                result.append((row['id1'], row['id2'], row['peso_totale']))
            return result
        except Exception as e:
            print(e)
            return []
        finally:
            if cursor is not None: cursor.close()
            cnx.close()

    # =====================================================================================
    # LIVELLO 5: I NODI SONO AGGREGAZIONI (I nodi dipendono da un conteggio)
    # === QUANDO USARLA ===
    # "I nodi sono i Team, ma SOLO SE in quel range di anni hanno disputato ALMENO X gare".
    # === PERCHÈ USARLA ===
    # Non basta un WHERE. Devi contare le gare (GROUP BY) e usare HAVING per la soglia.
    # =====================================================================================
    @staticmethod
    def get_nodi_aggregati_con_soglia(anno_da, anno_a, soglia_gare):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None: return result
        cursor = None
        try:
            cursor = cnx.cursor(dictionary=True)
            query = """
                SELECT c.*, COUNT(r.raceId) AS numero_gare
                FROM constructors c, results re, races r
                WHERE c.constructorId = re.constructorId
                  AND re.raceId = r.raceId
                  AND r.year BETWEEN %s AND %s
                GROUP BY c.constructorId
                HAVING numero_gare >= %s
            """
            cursor.execute(query, (anno_da, anno_a, soglia_gare))
            for row in cursor:
                # result.append(MioOggettoDTO(**row))
                pass
            return result
        except Exception as e:
            print(e)
            return []
        finally:
            if cursor is not None: cursor.close()
            cnx.close()

    # =====================================================================================
    # LIVELLO 6: ARCHI BASATI SU MATEMATICA E VALORE ASSOLUTO
    # === QUANDO USARLA ===
    # "Due nodi sono connessi se la differenza (delta) della loro età è minore di X".
    # === PERCHÈ USARLA ===
    # Usa la funzione ABS() (Valore Assoluto) per non preoccuparti di chi sia nato prima.
    # =====================================================================================
    @staticmethod
    def get_archi_differenza_matematica(anno_filtro, delta_max):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None: return result
        cursor = None
        try:
            cursor = cnx.cursor(dictionary=True)
            query = """
                SELECT re1.driverId AS id_1, re2.driverId AS id_2, ABS(YEAR(d1.dob) - YEAR(d2.dob)) AS differenza_eta
                FROM results re1, results re2, races ra, drivers d1, drivers d2
                WHERE re1.raceId = re2.raceId
                  AND re1.driverId = d1.driverId
                  AND re2.driverId = d2.driverId
                  AND ra.raceId = re1.raceId
                  AND ra.year = %s
                  AND re1.driverId < re2.driverId -- Evita (A,B) e (B,A)
                  AND ABS(YEAR(d1.dob) - YEAR(d2.dob)) <= %s
                GROUP BY id_1, id_2
            """
            cursor.execute(query, (anno_filtro, delta_max))
            for row in cursor:
                result.append((row['id_1'], row['id_2'], row['differenza_eta']))
            return result
        except Exception as e:
            print(e)
            return []
        finally:
            if cursor is not None: cursor.close()
            cnx.close()

    # =====================================================================================
    # LIVELLO 7: ARCHI BASATI SU TESTO E SOTTO-STRINGHE
    # === QUANDO USARLA ===
    # "Collega due piloti se hanno la stessa iniziale del cognome".
    # === PERCHÈ USARLA ===
    # Usa SUBSTRING(colonna, posizione_partenza, lunghezza) per tagliare il testo.
    # =====================================================================================
    @staticmethod
    def get_archi_corrispondenza_testo():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None: return result
        cursor = None
        try:
            cursor = cnx.cursor(dictionary=True)
            query = """
                SELECT d1.driverId AS id_1, d2.driverId AS id_2
                FROM drivers d1, drivers d2
                WHERE d1.driverId < d2.driverId
                  -- AND d1.nationality = d2.nationality -- Esempio: stessa nazione
                  AND SUBSTRING(d1.surname, 1, 1) = SUBSTRING(d2.surname, 1, 1) -- Stessa iniziale
            """
            cursor.execute(query)
            for row in cursor:
                result.append((row['id_1'], row['id_2'], 1))  # Peso fittizio a 1
            return result
        except Exception as e:
            print(e)
            return []
        finally:
            if cursor is not None: cursor.close()
            cnx.close()

    # =====================================================================================
    # LIVELLO 8: MANIPOLAZIONE DATE (DATEDIFF)
    # === QUANDO USARLA ===
    # "Il peso dell'arco è pari ai GIORNI di differenza tra la loro prima gara assoluta".
    # === PERCHÈ USARLA ===
    # Le date in SQL non si sottraggono col "-". Serve DATEDIFF(data1, data2).
    # =====================================================================================
    @staticmethod
    def get_peso_archi_differenza_giorni():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None: return result
        cursor = None
        try:
            cursor = cnx.cursor(dictionary=True)
            query = """
                SELECT re1.driverId AS id_1, re2.driverId AS id_2, ABS(DATEDIFF(MIN(ra1.date), MIN(ra2.date))) AS giorni_differenza
                FROM results re1, results re2, races ra1, races ra2
                WHERE re1.driverId < re2.driverId
                  AND re1.raceId = ra1.raceId
                  AND re2.raceId = ra2.raceId
                GROUP BY id_1, id_2
            """
            cursor.execute(query)
            for row in cursor:
                result.append((row['id_1'], row['id_2'], row['giorni_differenza']))
            return result
        except Exception as e:
            print(e)
            return []
        finally:
            if cursor is not None: cursor.close()
            cnx.close()

    # =====================================================================================
    # LIVELLO 9: MASSIMO PER GRUPPO (Sottoquery Correlata) - LA PIÙ DIFFICILE
    # === QUANDO USARLA ===
    # "Estrai per ogni circuito SOLO l'ultima gara cronologica che vi si è svolta".
    # === PERCHÈ USARLA ===
    # Devi agganciare una riga esterna con il MAX() di se stessa calcolato internamente.
    # =====================================================================================
    @staticmethod
    def get_ultime_gare_per_circuito():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None: return result
        cursor = None
        try:
            cursor = cnx.cursor(dictionary=True)
            query = """
                SELECT ra.* FROM races ra
                WHERE ra.date = (
                    SELECT MAX(ra_interna.date) 
                    FROM races ra_interna 
                    WHERE ra_interna.circuitId = ra.circuitId
                )
            """
            cursor.execute(query)
            for row in cursor:
                pass
            return result
        except Exception as e:
            print(e)
            return []
        finally:
            if cursor is not None: cursor.close()
            cnx.close()