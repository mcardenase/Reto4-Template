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
 """

import config as cf
import model
import csv
import sys
from DISClib.ADT import list as lt

csv.field_size_limit(2147483647)

default_limit = 1000
sys.setrecursionlimit(default_limit*10)

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # catalog es utilizado para interactuar con el modelo
    catalog = model.newCatalog()
    return catalog 

# Funciones para la carga de datos
def loadData(catalog, porcentajedatos):
    
    file= cf.data_dir + "bus_stops_bcn-utf8-" + porcentajedatos + ".csv" #ruta archivo en una variable
    input_file = csv.DictReader(open(file, encoding="utf8")) #abrir archivo para leer como dict
    for stops in input_file:
        stops = stops 
        model.addVertice(catalog, stops)
        



    file = cf.data_dir + "bus_edges_bcn-utf8-" + porcentajedatos + ".csv" #ruta archivo en una variable 
    input_file = csv.DictReader(open(file, encoding="utf8")) #abrir archivo para leer como dict
    for edges in input_file:
        model.addEdges(catalog, edges)
               
       


        
           
        
                
    return catalog









def totalStops(catalog):
    return model.totalStops(catalog)
def totalConnections(catalog):
    return model.totalConnections(catalog)

# Requerimiento 1
def caminoPosible(catalog, source, destination):
    return model.caminoPosible(catalog, source, destination)

# Requerimiento 2
def caminoCorto(catalog, source, destination):
    return model.caminoCorto(catalog, source, destination)

# Requerimiento 3
def componentesConectados(catalog):
    return model.componentesConectados(catalog)

# Requerimiento 4
def distancia_2_puntos_geo(catalog, lat1, lat2,lon1,lon2):
    return model.distancia_2_puntos_geo(catalog,  lat1, lat2,lon1,lon2)

# Requerimiento 6 
def ruta_minima_vecindario(cont, est_origen,vecindario):
    return model.ruta_minima_vecindario(cont, est_origen,vecindario)
# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo