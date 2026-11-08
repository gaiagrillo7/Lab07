from database.DB_connect import DBConnect
from model.biblioteca_DTO import Biblioteca

"""
    Biblioteca DAO
    Gestisce le operazioni di accesso al database relative alle biblioteche (Effettua le Query).
"""

class BibliotecaDAO:
    def __init__(self):
        pass

    def get_all_biblioteche(self) -> list[Biblioteca] | None:
        """
        Esegue la query per recuperare tutte le biblioteche ordinate per nome.
        return: Lista di oggetti Biblioteca o None in caso di errore.
        """
        cnx = DBConnect.get_connection()
        if cnx is None:
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """
            SELECT id, nome, indirizzo
            FROM biblioteca
            ORDER BY nome ASC
        """
        try:
            cursor.execute(query)
            risultato = []
            for row in cursor:
                b = Biblioteca(
                    id=row["id"],
                    nome=row["nome"],
                    indirizzo=row["indirizzo"]
                )
                risultato.append(b)
            return risultato
        except Exception as e:
            print(f"Errore durante la lettura delle biblioteche: {e}")
            return None
        finally:
            cursor.close()
            cnx.close()
