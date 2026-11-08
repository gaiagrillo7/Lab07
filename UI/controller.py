import flet as ft
from UI.view import View
from model.model import Model

'''
    CONTROLLER:
    - Funziona da intermediario tra MODELLO e VIEW
    - Gestisce la logica del flusso dell'applicazione
'''

class Controller:
    def __init__(self, view: View, model: Model):
        self._model = model
        self._view = view

        # Variabili per memorizzare le selezioni correnti
        self.biblioteca_selezionata = None
        self.genere_selezionato = None

    # POPOLA DROPDOWN
    def popola_dropdown(self):
        # 1. Recupero biblioteche e generi dal Modello
        biblioteche = self._model.get_biblioteche()
        generi = self._model.get_generi()

        # 2. Controllo di connessione al database
        if biblioteche is None or generi is None:
            self._view.show_alert("Errore di connessione al database durante il caricamento dei filtri!")
            return

        # 3. Pulizia opzioni precedenti
        self._view.dd_biblioteca.options.clear()
        self._view.dd_genere.options.clear()

        # 4. Inserimento della voce predefinita "Nessun filtro" (richiesta dal README)
        self._view.dd_biblioteca.options.append(ft.dropdown.Option(key="Nessun filtro", text="Nessun filtro"))
        self._view.dd_genere.options.append(ft.dropdown.Option(key="Nessun filtro", text="Nessun filtro"))

        # 5. Popolamento dropdown biblioteche
        # b è un oggetto Biblioteca(id, nome, indirizzo)
        for b in biblioteche:
            # key memorizza l'ID (es. "1"), text visualizza il nome a video
            self._view.dd_biblioteca.options.append(ft.dropdown.Option(key=str(b.id), text=b.nome))

        # 6. Popolamento dropdown generi
        for g in generi:
            self._view.dd_genere.options.append(ft.dropdown.Option(key=g, text=g))

    # CALLBACKS DROPDOWN
    def seleziona_biblioteca(self, e):
        # e.control fa riferimento al Dropdown che ha scatenato l'evento
        self.biblioteca_selezionata = e.control.value

    def seleziona_genere(self, e):
        self.genere_selezionato = e.control.value

    # AZIONE: MOSTRA LIBRI
    def mostra_libri(self, e):
        # 1. Recupero dei libri filtrati tramite il Modello
        libri = self._model.get_libri_filtrati(self.biblioteca_selezionata, self.genere_selezionato)

        # 2. Controllo errore database
        if libri is None:
            self._view.show_alert("Errore durante il recupero dei libri dal database!")
            return

        # 3. Pulizia della ListView
        self._view.lista_libri.controls.clear()

        # 4. Gestione lista vuota (Alert richiesto dalla traccia)
        if len(libri) == 0:
            self._view.show_alert("Nessun libro trovato con i criteri di filtraggio selezionati!")
        else:
            # Popolo la lista: str(libro) invoca il metodo __str__() di LibroDTO
            for l in libri:
                self._view.lista_libri.controls.append(ft.Text(str(l)))

        # 5. Aggiornamento visivo della pagina
        self._view.update()
