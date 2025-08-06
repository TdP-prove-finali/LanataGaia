import flet as ft
import time

class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self.circuitoVincolante = None
        self.year = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDYear(self):
        years = self._model.get_years()
        for y in years:
            self._view._ddAnno.options.append(ft.dropdown.Option(key = y, data = y, on_click= self.handleDDYearSelection))
        self._view.update_page()

    def handleDDYearSelection(self, e):
        self.year = e.control.data

    def handleCreaGrafo(self, e):
        self._view._txt_result.controls.clear()

        # Costruisco i due grafi
        self._model.buildGraphUfficiale(self.year)
        self._model.buildGraphOttimizzato(self.year)

        # Riempio il dd
        self.fillDDCircuitiVincolanti()

        # Info grafo ufficiale
        numNodes, numEdges = self._model.getGraphDetailsUfficiale()
        self._view._txt_result.controls.append(ft.Text(f"Grafo ufficiale creato con {numNodes} nodi e {numEdges} archi.\n"))
        peso_ufficiale = self._model.getPesoTotStagione()
        self._view._txt_result.controls.append(ft.Text(f"Totale km percorsi nel calendario ufficiale della stagione {self.year}: {peso_ufficiale:.2f} km. \nSegue il dettaglio degli spostamenti ufficiali:"))
        archiConPeso = self._model.getArchiUfficiale(self.year)
        i = 1
        for n1, n2, p in archiConPeso:
            self._view._txt_result.controls.append(ft.Text(f"{i}. {n1.name}({n1.country}) → {n2.name}({n2.country}): {p:.2f} km"))
            i+=1
        self._view.update_page()
        # Ricostruisco il cammino ufficiale ordinato
        cammino_ufficiale = [n1 for n1, _, _ in archiConPeso]
        cammino_ufficiale.append(archiConPeso[-1][1])  # aggiungo ultima tappa
        # Creo e mostro la mappa
        self._model.creaMappa(cammino_ufficiale, nome_file="mappa_ufficiale.html")
        self._model.apriMappa("mappa_ufficiale.html")

    def fillDDCircuitiVincolanti(self):
        self._view._ddCircuitoVincolante.options.clear()
        circuiti = self._model.get_circuiti(self.year)
        for c in circuiti:
            self._view._ddCircuitoVincolante.options.append(ft.dropdown.Option(key=c, data=c, on_click=self.handleAggiungiCircuiti))
        self._view.update_page()

    def handleAggiungiCircuiti(self, e):
        self.circuitoVincolante = e.control.data

    def handleCercaCamminoMin(self, e):
        k_str = self._view._txtK.value.strip()

        # Caso 1: nessun vincolo
        if self.circuitoVincolante is None and k_str == "":
            self._model.setVincoloCircuito(None, None)

        # Caso 2: entrambi i vincoli
        elif self.circuitoVincolante is not None and k_str != "":
            try:
                k = int(k_str)
                self._model.setVincoloCircuito(self.circuitoVincolante, k-1)
            except ValueError:
                self._view._txt_result.controls.append(ft.Text("Inserire un numero intero valido per K"))
                self._view.update_page()
                return

        # Caso 3: inserito solo un vincolo (errore, devono esserci entrambi per funzionare)
        else:
            self._view._txt_result.controls.append(ft.Text("Se si vuole inserire un vincolo, selezionare sia un circuito sia un valore per K"))
            self._view.update_page()
            return

        # Avvio la ricerca del cammino minimo e stampo i risultati
        tic = time.time()
        cammino, kmOttimizzati = self._model.getCamminoMin()
        toc = time.time()
        t = (toc-tic)/60
        self._view._txt_result.controls.append(ft.Text(f"\nTempo impiegato per la ricerca del cammino minimo: {t:.2f} minuti"))

        kmUfficiali = self._model.getPesoTotStagione()
        risparmio = 100 * (kmUfficiali - kmOttimizzati) / kmUfficiali

        self._view._txt_result.controls.append(ft.Text(f"\nCalendario ottimizzato trovato per la stagione {self.year} con {kmOttimizzati:.2f} km totali percorsi e risparmio del {risparmio:.2f}%. \nSegue il dettaglio degli spostamenti ottimizzati:"))

        for i in range(len(cammino) - 1):
            partenza = cammino[i]
            arrivo = cammino[i + 1]
            distanza = self._model.graphOttimizzato[partenza][arrivo]["weight"]
            self._view._txt_result.controls.append(ft.Text(f"{i+1}. {partenza.name}({partenza.country}) → {arrivo.name}({arrivo.country}): {distanza:.2f} km"))

        # Creo e mostro la mappa del cammino ottimizzato
        self._model.creaMappa(cammino, nome_file="mappa_ottimizzata.html")
        self._model.apriMappa("mappa_ottimizzata.html")

        self._view.update_page()



