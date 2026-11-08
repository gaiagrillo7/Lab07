from database.biblioteca_DAO import BibliotecaDAO
from database.libro_DAO import LibroDAO

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Si occupa di interrogare il DAO (chiama i metodi di BibliotecaDAO e LibroDAO)
'''

class Model:
    def __init__(self):
        self._biblioteca_dao = BibliotecaDAO()
        self._libro_dao = LibroDAO()

    # --- LIBRI ---
    def get_libri_filtrati(self, biblioteca:str, genere:str):
        """Restituisce la lista di tutti i libri filtrati per biblioteca e/o genere (filtri opzionali)."""
        # 1. Normalizzo il filtro della biblioteca:
        # Se l'utente ha scelto "Nessun filtro" (o il valore è vuoto/None), passiamo None al DAO
        id_biblioteca = None
        if biblioteca and biblioteca != "Nessun filtro":
            try:
                id_biblioteca = int(biblioteca)
            except ValueError:
                # Se per caso viene passato il nome o una stringa non numerica,
                # cerchiamo l'id corrispondente tra le biblioteche
                biblioteche = self._biblioteca_dao.get_all_biblioteche()
                if biblioteche:
                    for b in biblioteche:
                        if b.nome == biblioteca or str(b.id) == biblioteca:
                            id_biblioteca = b.id
                            break

        # 2. Normalizzo il filtro del genere:
        # Se l'utente ha scelto "Nessun filtro" (o il valore è vuoto/None), passiamo None al DAO
        filtro_genere = None
        if genere and genere != "Nessun filtro":
            filtro_genere = genere

        # 3. Interrogo il DAO passando i filtri normalizzati (None attiva COALESCE in SQL)
        return self._libro_dao.get_libri_filtrati(id_biblioteca, filtro_genere)

    def get_generi(self):
        """Restituisce la lista di tutti i generi."""
        return self._libro_dao.get_all_generi()

    # --- BIBLIOTECHE ---
    def get_biblioteche(self):
        """ Restituisce la lista di tutte le biblioteche."""
        return self._biblioteca_dao.get_all_biblioteche()


