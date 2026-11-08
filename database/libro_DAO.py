from database.DB_connect import DBConnect
from model.libro_DTO import Libro

"""
    LIBRO DAO
    Gestisce le operazioni di accesso al database relative ai libri (Effettua le Query).
"""

class LibroDAO:
    def __init__(self):
        pass

    def get_all_generi(self) -> list[str] | None:
        """
        Recupera tutti i generi distinti dei libri memorizzati nel database.
        return: Lista di stringhe con i nomi dei generi, ordinati alfabeticamente.
        """
        cnx = DBConnect.get_connection()
        if cnx is None:
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """
            SELECT DISTINCT genere
            FROM libro
            WHERE genere IS NOT NULL
            ORDER BY genere ASC
        """
        try:
            cursor.execute(query)
            generi = []
            for row in cursor:
                generi.append(row["genere"])
            return generi
        except Exception as e:
            print(f"Errore durante la lettura dei generi: {e}")
            return None
        finally:
            cursor.close()
            cnx.close()

    def get_libri_filtrati(self, id_biblioteca: int | None, genere: str | None) -> list[Libro] | None:
        """
        Recupera i libri applicando filtri opzionali su id_biblioteca e genere tramite COALESCE.
        param id_biblioteca: intero con l'ID biblioteca o None se nessun filtro.
        param genere: stringa del genere o None se nessun filtro.
        return: Lista di oggetti Libro o None in caso di errore.
        """
        cnx = DBConnect.get_connection()
        if cnx is None:
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """
            SELECT id, titolo, autore, genere, anno_pubblicazione, id_biblioteca
            FROM libro
            WHERE id_biblioteca = COALESCE(%s, id_biblioteca)
              AND genere = COALESCE(%s, genere)
            ORDER BY titolo ASC
        """
        try:
            # Query parametrica: id_biblioteca e genere passati come tupla
            cursor.execute(query, (id_biblioteca, genere))
            risultato = []
            for row in cursor:
                l = Libro(
                    id=row["id"],
                    titolo=row["titolo"],
                    autore=row["autore"],
                    genere=row["genere"],
                    anno_pubblicazione=row["anno_pubblicazione"],
                    id_biblioteca=row["id_biblioteca"]
                )
                risultato.append(l)
            return risultato
        except Exception as e:
            print(f"Errore durante la ricerca filtrata dei libri: {e}")
            return None
        finally:
            cursor.close()
            cnx.close()
