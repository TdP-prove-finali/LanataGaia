import copy
import os
import webbrowser

import geopy
import networkx as nx
import folium

from database.DAO import DAO

from geopy.distance import distance

class Model:
    def __init__(self):
        self.listaOttimizzata = []
        self.score = None
        self.graphUfficiale = None
        self.graphOttimizzato = None
        self.idMap = {}
        self.vincolo_circuito = None
        self.vincolo_k = None

    def get_years(self):
        return DAO.get_years()

    def get_circuiti(self, anno):
        return DAO.getAllNodes(anno)

    def buildGraphUfficiale(self, anno):
        self.graphUfficiale = nx.DiGraph()
        allNodes = self.get_circuiti(anno)
        self.graphUfficiale.add_nodes_from(allNodes)
        for n in allNodes:
            self.idMap[n.circuitId] = n
        self.addArchiUfficiale(anno)

    def addArchiUfficiale(self, anno):
        lista = DAO.getAllEdges(anno)
        for n1, n2 in lista:
            p = getTraversalTime(self.idMap[n1], self.idMap[n2])
            self.graphUfficiale.add_edge(self.idMap[n1], self.idMap[n2], weight = p)

    def getArchiUfficiale(self, anno):
        lista = DAO.getAllEdges(anno)
        archiConPeso = []
        for n1, n2 in lista:
            p = getTraversalTime(self.idMap[n1], self.idMap[n2])
            archiConPeso.append((self.idMap[n1], self.idMap[n2], p))
        return archiConPeso

    def buildGraphOttimizzato(self, anno):
        self.graphOttimizzato = nx.Graph()  # grafo non orientato
        circuiti = self.get_circuiti(anno)
        self.graphOttimizzato.add_nodes_from(circuiti) # aggiungo tutti i circuiti dell'anno selezionato al grafo

        # aggiungo archi tra tutte le coppie (grafo completo)
        for i in range(len(circuiti)):
            for j in range(i + 1, len(circuiti)):
                c1 = circuiti[i]
                c2 = circuiti[j]
                peso = getTraversalTime(c1, c2)
                self.graphOttimizzato.add_edge(c1, c2, weight=peso)

    def getGraphDetailsUfficiale(self):
        return self.graphUfficiale.number_of_nodes(), self.graphUfficiale.number_of_edges()

    def getPesoTotStagione(self):
        pesoTot = 0
        for n1, n2 in self.graphUfficiale.edges():
            pesoTot += self.graphUfficiale[n1][n2]["weight"]
        return pesoTot

    def setVincoloCircuito(self, circuito, k):
        self.vincolo_circuito = circuito
        self.vincolo_k = k

    def getCamminoMin(self):
        self.listaOttimizzata = []
        self.score = None
        for n in self.graphOttimizzato.nodes():
            self.ricorsione([n])
        return self.listaOttimizzata, self.score

    def ricorsione(self, parziale):
        # calcola la soluzione ottima
        if len(parziale) == self.graphOttimizzato.number_of_nodes():
            if self.score is None or self.getScore(parziale) < self.score:
                self.listaOttimizzata = copy.deepcopy(parziale)
                self.score = self.getScore(parziale)

        else:
            for v in nx.neighbors(self.graphOttimizzato, parziale[-1]):
                if self.condizione(parziale, v):
                    parziale.append(v)
                    self.ricorsione(parziale)
                    parziale.pop()

    def condizione(self, parziale, v):
        if v in parziale:
            return False

        # se non ho vincoli posso aggiungere il nodo
        if self.vincolo_circuito is None or self.vincolo_k is None:
            return True

        # boolean per gestire l'inserimento del circuito vincolante
        circuito = False
        # se il circuito è già nel cammino allora diventa True
        for nodo in parziale:
            if nodo.circuitId == self.vincolo_circuito.circuitId:
                circuito = True

        # se la posizione attuale è pari a K e il circuito ancora non è presente lo aggiungo per forza
        if len(parziale) == self.vincolo_k:
            if not circuito:
                return v.circuitId == self.vincolo_circuito.circuitId # True se v è il circuito vincolante e False altrimenti

        if len(parziale) > self.vincolo_k:
            if not circuito:
                return False

        return True

    def getScore(self, parziale):
        km = 0
        for i in range(len(parziale) - 1):
            nodo1 = parziale[i]  # un nodo
            nodo2 = parziale[i + 1]  # il nodo successivo
            km += self.graphOttimizzato[nodo1][nodo2]['weight']  # il peso dell'arco
        return km

    # creo la mappa interattiva che si apre su browser
    def creaMappa(self, cammino, nome_file="mappa.html"):
        if not cammino:
            return

        mappa = folium.Map(location=[cammino[0].lat, cammino[0].lng], zoom_start=2)
        # prima creo i punti sulla mappa con le info
        for i in range(len(cammino)):
            circuito = cammino[i]
            numero = i + 1
            label = f"{numero}. {circuito.name} ({circuito.country})"
            folium.Marker(
                location=[circuito.lat, circuito.lng],
                popup=label,
                tooltip=label,
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(mappa)
        # poi creo le rette che li collegano
        for idx in range(len(cammino) - 1):
            c1 = cammino[idx]
            c2 = cammino[idx + 1]
            folium.PolyLine(
                locations=[[c1.lat, c1.lng], [c2.lat, c2.lng]],
                color='blue',
                weight=2
            ).add_to(mappa)

        mappa.save(nome_file)

    def apriMappa(self, file_html):
        path = os.path.abspath(file_html)
        webbrowser.open(f"file://{path}")


def getTraversalTime(u, v):
    dist = geopy.distance.distance((u.lat, u.lng), (v.lat, v.lng)).km
    # geopy permette di manipolare informazioni di distanza
    return dist






