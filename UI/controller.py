import flet as ft


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
        self._view._txt_result.controls.append(ft.Text(f"Totale km percorsi nel calendario ufficiale {self.year}: {peso_ufficiale:.2f} km. Segue il dettaglio dei trasferimenti ufficiali:"))
        archiConPeso = self._model.getArchiUfficiale(self.year)
        for n1, n2, p in archiConPeso:
            self._view._txt_result.controls.append(ft.Text(f"{n1.name}({n1.country}) → {n2.name}({n2.country}): {p:.2f} km"))

        self._view.update_page()

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
        cammino, kmOttimizzati = self._model.getCamminoMin()
        kmUfficiali = self._model.getPesoTotStagione()

        self._view._txt_result.controls.append(ft.Text(f"\nCammino ottimizzato trovato per la stagione {self.year} con {kmOttimizzati:.2f} km totali percorsi nell'ordine ottimale."))

        risparmio = 100 * (kmUfficiali - kmOttimizzati) / kmUfficiali
        self._view._txt_result.controls.append(ft.Text(f"Risparmio potenziale: {risparmio:.2f}%"))

        self._view._txt_result.controls.append(ft.Text("Dettaglio cammino ottimizzato:"))
        for i in range(len(cammino) - 1):
            partenza = cammino[i]
            arrivo = cammino[i + 1]
            distanza = self._model.graphOttimizzato[partenza][arrivo]["weight"]
            self._view._txt_result.controls.append(ft.Text(f"{i+1}. {partenza.name}({partenza.country}) → {arrivo.name}({arrivo.country}): {distanza:.2f} km"))

        self._view.update_page()


