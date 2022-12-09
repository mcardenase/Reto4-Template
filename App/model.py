"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """

import math
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import stack as stk
from DISClib.ADT import graph as gr
from DISClib.ADT import map as m
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import mergesort as mg
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import dfs as dfs
from DISClib.Algorithms.Graphs import bfs as bfs
from haversine import haversine, Unit
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos


def newCatalog():
    """ 
    Inicializa el analizador
   stops: Tabla de hash para guardar los vertices del grafo
   connections: Grafo para representar las rutas entre estaciones
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """

    catalog = {
        'conexiones': None,
    }

    catalog['conexiones'] = gr.newGraph(datastructure='ADJ_LIST',
                                        directed=True,
                                        size=200,
                                        comparefunction=compareStopIds)
    catalog["conexiones_no_dirigido"] = gr.newGraph(datastructure='ADJ_LIST',
                                        directed=False,
                                        size=200,
                                        comparefunction=compareStopIds)
    catalog['pesos'] = m.newMap()

    catalog["Vecindario"] = m.newMap()

    return catalog
# Funciones para agregar informacion al catalogo


def addVertice(catalog, stops):
    bus_stop = stops["Bus_Stop"]
    vertice = str(stops["Code"]) + "-" + bus_stop.split("-")[1]
    addMaps(catalog, vertice,stops)


def addMaps(catalog, vertice,stops):
    m.put(catalog['pesos'], vertice, stops)
def addVecindario(catalog, vertice, vecindario):
    if not m.contains(catalog["Vecindario"], vecindario):
        lista = lt.newList(datastructure='ARRAY_LIST')
        lt.addLast(lista, vertice)
        m.put(catalog["Vecindario"], vecindario, lista)
    else:
        lista = m.get(catalog["Vecindario"], vecindario)
        lista = me.getValue(lista)
        lt.addLast(lista, vertice)
def addEdges(catalog, edges):
    valorOrigen = m.get(catalog["pesos"], f"{edges['Code']}-{edges['Bus_Stop'].split('-')[1]}")
    valorDestiny = m.get(catalog["pesos"], f"{edges['Code_Destiny']}-{edges['Bus_Stop'].split('-')[1]}")
    if valorOrigen is not None and valorDestiny is not None:
        valorOrigen = me.getValue(valorOrigen)
        valorDestiny = me.getValue(valorDestiny)

        longitud1 = valorOrigen["Longitude"]
        latitud1 = valorOrigen["Latitude"]

        
        longitud2 = valorDestiny["Longitude"]
        latitud2 = valorDestiny["Latitude"]

        weight = peso(latitud1, latitud2, longitud1, longitud2)

        bus_stop = edges["Bus_Stop"]

        vertexa = str(edges["Code"]) + "-" + bus_stop.split("-")[1]
        vertexb = str(edges["Code_Destiny"]) + "-" + bus_stop.split("-")[1]

        #insercion a la tabla de hash para los vertices en un vecindario
        vecindario_A = valorOrigen["Neighborhood_Name"]
        vecindario_B = valorDestiny["Neighborhood_Name"]
        addVecindario(catalog, vertexa, vecindario_A)
        addVecindario(catalog, vertexb, vecindario_B)
        if not gr.containsVertex(catalog["conexiones"], vertexa):
            gr.insertVertex(catalog["conexiones"], vertexa)
        if not gr.containsVertex(catalog["conexiones"], vertexb):
            gr.insertVertex(catalog["conexiones"], vertexb)
        if not gr.containsVertex(catalog["conexiones_no_dirigido"], vertexa):
            gr.insertVertex(catalog["conexiones_no_dirigido"], vertexa)
        if not gr.containsVertex(catalog["conexiones_no_dirigido"], vertexb):
            gr.insertVertex(catalog["conexiones_no_dirigido"], vertexb)
        gr.addEdge(catalog['conexiones'], vertexa, vertexb, weight)

        if valorOrigen["Transbordo"] == "S":
            transbordo = "T-" + valorOrigen["Code"]
            transbordo_info= valorOrigen.copy()
            transbordo_info["Code"] = transbordo
            addVecindario(catalog, transbordo, vecindario_A)
            #agregamos la información de transbordo a la tabla de hash
            m.put(catalog['pesos'], transbordo, transbordo_info)
            if not gr.containsVertex(catalog["conexiones"], transbordo):
                gr.insertVertex(catalog["conexiones"], transbordo)
                gr.insertVertex(catalog["conexiones_no_dirigido"], transbordo)
            gr.addEdge(catalog['conexiones'], transbordo, vertexa, weight)
            gr.addEdge(catalog['conexiones'], vertexa, transbordo, weight)
            gr.addEdge(catalog['conexiones_no_dirigido'], transbordo, vertexa, weight)
        if valorDestiny["Transbordo"] == "S":
            transbordo = "T-" + valorDestiny["Code"]
            transbordo_info= valorDestiny.copy()
            transbordo_info["Code"] = transbordo
            addVecindario(catalog, transbordo, vecindario_B)
            m.put(catalog['pesos'], transbordo, transbordo_info)
            if not gr.containsVertex(catalog["conexiones"], transbordo):
                gr.insertVertex(catalog["conexiones"], transbordo)
                gr.insertVertex(catalog["conexiones_no_dirigido"], transbordo)
            
            gr.addEdge(catalog['conexiones'], transbordo, vertexb, weight)
            gr.addEdge(catalog['conexiones'], vertexb, transbordo, weight)
            gr.addEdge(catalog['conexiones_no_dirigido'], transbordo, vertexb, weight)
    #TODO: Falta imprimir información

def peso(latitud1, latitud2, longitud1, longitud2):

    x = (math.sin(float(latitud1) - float(latitud2)/2)
         * math.sin(float(latitud1) - float(latitud2)/2))
    y = math.cos(float(latitud1))*math.cos(float(latitud2))
    z = (math.sin(float(longitud2) - float(longitud1)/2)
         * math.sin(float(longitud2) - float(longitud1)/2))
    semiversin = x + y*z

    distancia = (6356)*(1/semiversin)

    return distancia


def totalStops(catalog):
    return gr.numVertices(catalog['conexiones'])


def totalConnections(catalog):
    return gr.numEdges(catalog['conexiones'])


#Requerimiento 1

def caminoPosible (catalog, origen, destino):
    dfs1 = dfs.DepthFirstSearch(catalog['conexiones'], origen)
    dist_total = 0
    contador_estaciones = lt.newList()
    estaciones = lt.newList()
    total_transbordos =0
    pesos= lt.newList()
    if dfs.hasPathTo(dfs1, destino):
        path = dfs.pathTo(dfs1, destino)
        primero = None

        while not stk.isEmpty(path):
            vertice = stk.pop(path)
            if vertice[0] == "T":
                total_transbordos += 1
            if lt.isPresent(contador_estaciones, vertice) == 0 and vertice[0] != "T":
                lt.addLast(contador_estaciones, vertice)

            if lt.isPresent(estaciones, vertice) == 0:
                lt.addLast(estaciones, vertice)
            if primero is None:
                primero = vertice
                continue
            else:
                arco = gr.getEdge(catalog['conexiones'], primero, vertice)
                dist_total += arco['weight']
                lt.addLast(pesos, arco['weight'])

    return dist_total, lt.size(contador_estaciones),estaciones, total_transbordos, pesos


#Requerimiento 2

def caminoCorto (catalog, origen, destino):
    dfs1 = bfs.BreadhtFisrtSearch(catalog['conexiones'], origen)
    dist_total = 0
    contador_estaciones = lt.newList()
    estaciones = lt.newList()
    total_transbordos =0
    pesos= lt.newList()
    if bfs.hasPathTo(dfs1, destino):
        path = bfs.pathTo(dfs1, destino)
        primero = None

        while not stk.isEmpty(path):
            vertice = stk.pop(path)
            if vertice[0] == "T":
                total_transbordos += 1
            if lt.isPresent(contador_estaciones, vertice) == 0 and vertice[0] != "T":
                lt.addLast(contador_estaciones, vertice)

            if lt.isPresent(estaciones, vertice) == 0:
                lt.addLast(estaciones, vertice)
            if primero is None:
                primero = vertice
                continue
            else:
                arco = gr.getEdge(catalog['conexiones'], primero, vertice)
                dist_total += arco['weight']
                lt.addLast(pesos, arco['weight'])

    return dist_total, lt.size(contador_estaciones),estaciones, total_transbordos, pesos


#Requerimiento 3 

def componentesConectados(catalog):
    componentes_conectados = scc.KosarajuSCC(catalog['conexiones'])
    componentes = scc.connectedComponents(componentes_conectados)
    idscc = componentes_conectados['idscc']	
    tabla_hash = m.newMap()
    llaves= m.keySet(idscc)
    for vertice in lt.iterator(llaves):
        num_componente = me.getValue(m.get(idscc, vertice))
        if m.contains(tabla_hash, num_componente):
            lista_pareja_llave_valor = me.getValue(m.get(tabla_hash, num_componente))
            lt.addLast(lista_pareja_llave_valor[1], vertice)
        else:
            lista_pareja_llave_valor = (num_componente,lt.newList("ARRAY_LIST"))
            lt.addLast(lista_pareja_llave_valor[1], vertice)
            m.put(tabla_hash, num_componente, lista_pareja_llave_valor)
    #(1,[ver1,ver2,v3]),(2,[ver4,ver5,v6])...
    valores = m.valueSet(tabla_hash)
    valores_ordenados = mg.sort(valores, comparador_tuplas)
    dicc_retorno = {"componentes":valores_ordenados, "num_componentes":componentes}
    return dicc_retorno


#Requerimiento 4 

def distancia_2_puntos_geo(catalog,latitud1, latitud2, longitud1, longitud2):
    estacion_origen,peso1 = estacion_cercana(catalog, latitud1, longitud1)
    estacion_destino,peso2 = estacion_cercana(catalog, latitud2, longitud2)

    distancia, num_estaciones, estaciones, num_transbordos, pesos = caminoPosible_dijkstra(catalog, estacion_origen, estacion_destino)
    lt.addFirst(estaciones, f"{latitud1}, {longitud1}")
    lt.addLast(estaciones, f"{latitud2}, {longitud2}")
    lt.addFirst(pesos, peso1)
    lt.addLast(pesos, peso2)
    return distancia, num_estaciones, estaciones, num_transbordos, pesos
def estacion_cercana_dijt(destino,result_dijkstra):
    dijkstra= result_dijkstra
    dist_total = 0
    contador_estaciones = lt.newList()
    estaciones = lt.newList()
    total_transbordos =0
    pesos= lt.newList()
    if djk.hasPathTo(dijkstra, destino):
        path = djk.pathTo(dijkstra, destino)

        while not stk.isEmpty(path):
            arco = stk.pop(path)
            lt.addLast(pesos, arco['weight'])
            vertice1 = arco['vertexA'] 
            vertice2 = arco['vertexB']
            if lt.isPresent(estaciones, vertice1) == 0:
                lt.addLast(estaciones, vertice1)
            if lt.isPresent(estaciones, vertice2) == 0:
                lt.addLast(estaciones, vertice2)

            if arco['vertexB'][0] == "T":
                total_transbordos += 1
            if arco["vertexA"][0] == "T":
                total_transbordos += 1
            if lt.isPresent(contador_estaciones, arco["vertexA"]) == 0 and arco["vertexA"][0] != "T":
                lt.addLast(contador_estaciones, arco["vertexA"])
            if lt.isPresent(contador_estaciones, arco["vertexB"]) == 0 and arco["vertexB"][0] != "T":
                lt.addLast(contador_estaciones, arco["vertexB"])
        dist_total= djk.distTo(dijkstra, destino)


    return dist_total, lt.size(contador_estaciones),estaciones, total_transbordos, pesos


def caminoPosible_dijkstra (catalog, origen, destino):
    dijkstra = djk.Dijkstra(catalog['conexiones'], origen)
    dist_total = 0
    contador_estaciones = lt.newList()
    estaciones = lt.newList()
    total_transbordos =0
    pesos= lt.newList()
    if djk.hasPathTo(dijkstra, destino):
        path = djk.pathTo(dijkstra, destino)

        while not stk.isEmpty(path):
            arco = stk.pop(path)
            lt.addLast(pesos, arco['weight'])
            vertice1 = arco['vertexA'] 
            vertice2 = arco['vertexB']
            if lt.isPresent(estaciones, vertice1) == 0:
                lt.addLast(estaciones, vertice1)
            if lt.isPresent(estaciones, vertice2) == 0:
                lt.addLast(estaciones, vertice2)

            if arco['vertexB'][0] == "T":
                total_transbordos += 1
            if arco["vertexA"][0] == "T":
                total_transbordos += 1
            if lt.isPresent(contador_estaciones, arco["vertexA"]) == 0 and arco["vertexA"][0] != "T":
                lt.addLast(contador_estaciones, arco["vertexA"])
            if lt.isPresent(contador_estaciones, arco["vertexB"]) == 0 and arco["vertexB"][0] != "T":
                lt.addLast(contador_estaciones, arco["vertexB"])
        dist_total= djk.distTo(dijkstra, destino)


    return dist_total, lt.size(contador_estaciones),estaciones, total_transbordos, pesos
def comparador_tuplas(tupla1, tupla2):
    if lt.size (tupla1[1]) > lt.size (tupla2[1]):
        return True
    else:
        return False

def estacion_cercana(catalog, latitud, longitud):
    #TODO
    vertices = gr.vertices(catalog['conexiones'])
    mejor_vertice = ""
    peso_1 = -1
    latitud = float(latitud)
    longitud = float(longitud)
    for vertice in lt.iterator(vertices):
        
        valor = me.getValue(m.get(catalog['pesos'], vertice))
        if valor["Code"][0]!="T":
            lat1_ver = float(valor["Latitude"])
            lon1_ver = float(valor["Longitude"])
            distancia = haversine ((latitud, longitud), (lat1_ver, lon1_ver))
            if peso_1 == -1 or distancia < peso_1 :
                peso_1 = distancia
                mejor_vertice = vertice
    return mejor_vertice, peso_1


#Requerimiento 6 

def ruta_minima_vecindario(cont, est_origen,vecindario):
    vecindario = me.getValue(m.get(cont['Vecindario'], vecindario))
    minimo = -1
    estacion = ""
    num_estaciones, estaciones, num_transbordos, pesos = 0,0,0,0
    dij = djk.Dijkstra(cont['conexiones'], est_origen)
    for i in lt.iterator(vecindario):
        if i != est_origen:
            distancia, num_estaciones, estaciones, num_transbordos, pesos = estacion_cercana_dijt(i,dij)
            if minimo == -1 or distancia < minimo:
                minimo = distancia
                estacion = i
    return minimo, estacion, num_estaciones, estaciones, num_transbordos, pesos

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento

# Funciones de Comparación


def compareStopIds(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1
        