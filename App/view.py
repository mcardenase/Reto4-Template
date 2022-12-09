"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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

import sys
import config
import threading
import time
from App import controller
from DISClib.ADT import stack
from DISClib.ADT import list as lt 

assert config


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("\n")
    print("*****")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de buses de Barcelona")
    print("3- Buscar un camino posible entre dos estaciones")
    print("4- Buscar el camino con menos paradas entre dos estaciones")
    print("5- Reconocer los componentes conectados de la Red de rutas de bus")
    print("6- Planear el camino con distancia mínima entre dos puntos geográficos ")
    print("7- Informar las estaciones “alcanzables” desde un origen a un número máximo de conexiones ")
    print("8- Buscar el camino con mínima distancia entre una estación de origen y un vecindario de destino ")
    print("9- Encontrar un posible camino circular desde una estación de origen: ")
    print("0- Salir")
    print("*****")

catalog = None
def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def deltaTime(end, start):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed




def optionTwo(cont):
    start_time = getTime()
    print("\nCargando información de transporte de singapur ....")
    porcentajedatos = input(
            '\nIndique el porcentaje de datos a cargar (small, 5pct, 10pct, 20pct, 30pct, 50pct, 80pct, large): ')
    controller.loadData(cont, porcentajedatos)
    numedges = controller.totalConnections(cont)
    numvertex = controller.totalStops(cont)
    print('Numero de vertices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))
    print('El limite de recursion actual: ' + str(sys.getrecursionlimit()))
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    print('El tiempo gastado fue de: ' + str(delta_time))

def optionThree(cont, est_origen, est_destino):
    start_time = getTime()
    print("\nBuscando camino posible entre dos estaciones ....")
    est_origen = "1480-78"
    est_destino = "1481-78"
    dist_total, contador_estaciones ,camino, total_transbordos, pesos = controller.caminoPosible(cont, est_origen, est_destino)
    
    print("La distancia entre los puntos es: " + str(dist_total))
    print("El número de estaciones es: " + str(contador_estaciones))
    print("El número de transbordos es: " + str(total_transbordos))
    print("El camino es: ")
    for i in range(1, lt.size(camino)+1):
        if i == lt.size(camino):
            print(f"{i}. {lt.getElement(camino, i)}")
        else:
            print(f"{i}. {lt.getElement(camino, i)}, peso: {lt.getElement(pesos, i)}")
        
    print("El peso del camino es: " + str(pesos))
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    print('El tiempo gastado fue de: ' + str(delta_time))

def optionFour(cont, est_origen, est_destino):
    start_time = getTime()
    dist_total, contador_estaciones ,camino, total_transbordos, pesos = controller.caminoCorto(cont, est_origen, est_destino)
    
    print("La distancia entre los puntos es: " + str(dist_total))
    print("El número de estaciones es: " + str(contador_estaciones))
    print("El número de transbordos es: " + str(total_transbordos))
    print("El camino es: ")
    for i in range(1, lt.size(camino)+1):
        print(f"{i}. {lt.getElement(camino, i)}, peso: {lt.getElement(pesos, i)}")
        
    print("El peso del camino es: " + str(pesos))
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    print('El tiempo gastado fue de: ' + str(delta_time))

def optionFive(cont):
    start_time = getTime()
    print("\nReconociendo componentes conectados de la red de rutas de bus ....")
    info_comp = controller.componentesConectados(cont)
    print("El número de componentes conectados es: " + str(info_comp["num_componentes"]))
    for i in lt.iterator(info_comp["componentes"]):
        print(i)
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    print('El tiempo gastado fue de: ' + str(delta_time))

def optionSix(cont, lat1, lat2,lon1,lon2):
    start_time = getTime()
    distancia, num_estaciones, estaciones, num_transbordos, pesos = controller.distancia_2_puntos_geo(cont, lat1, lat2,lon1,lon2)
    print("La distancia entre los puntos es: " + str(distancia))
    print("El número de estaciones es: " + str(num_estaciones))
    print("El número de transbordos es: " + str(num_transbordos))
    print("El camino es: ")
    for i in range(1, lt.size(estaciones)+1):
        print(f"{i}. {lt.getElement(estaciones, i)}, peso: {lt.getElement(pesos, i)}")
        
    print("El peso del camino es: " + str(pesos))
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    print('El tiempo gastado fue de: ' + str(delta_time))

def optionSeven(cont, est_origen, num_conexiones):
    pass

def optionEight(cont, est_origen,vecindario):
    start_time = getTime()
    distancia,estacion, num_estaciones, estaciones, num_transbordos, pesos = controller.ruta_minima_vecindario(cont, est_origen,vecindario)
    print("La estacion más cercana al vecindario es: " + estacion )
    print("La distancia entre los puntos es: " + str(distancia))
    print("El número de estaciones es: " + str(num_estaciones))
    print("El número de transbordos es: " + str(num_transbordos))
    print("El camino es: ")
    for i in range(1, lt.size(estaciones)+1):
        print(f"{i}. {lt.getElement(estaciones, i)}, peso: {lt.getElement(pesos, i)}")
        
    print("El peso del camino es: " + str(pesos))
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    print('El tiempo gastado fue de: ' + str(delta_time))

def optionNine(cont, est_origen):
    pass

"""
Menu principal
"""
def thread_cycle():
    while True:
        printMenu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs[0]) == 1:
            print("Cargando información de los archivos ....")
            cont = controller.init()

        elif int(inputs) == 2:
            print(optionTwo(cont))


        elif int(inputs) == 3:
            est_origen = input("Identificador de la estación origen: ")
            est_destino = input("Identificador de la estación destino: ")
            optionThree(cont, est_origen, est_destino)

        elif int(inputs) == 4:
            est_origen = input("Identificador de la estación origen: ")
            est_destino = input("Identificador de la estación destino: ")
            optionFour(cont, est_origen, est_destino)

        elif int(inputs) == 5:
            optionFive(cont)
            
        elif int(inputs) == 6:
            lat1 = input("Latitud 1: ")
            lat2 = input("Latitud 2: ")
            lon1 = input("Longitud 1: ")
            lon2 = input("Longitud 2: ")
            #TODO
            lon1 ="2.137373"
            lat1 ="41.33108"

            lon2 = "2.140321"
            lat2= "41.33497"
            

            optionSix(cont, lat1, lat2,lon1,lon2)

        elif int(inputs) == 7:
            est_origen = input("Identificador de la estación origen: ")
            num_conexiones = input("Número de conexiones permitidas desde la estación origen: ")
            optionSeven(cont, est_origen, num_conexiones)

        elif int(inputs) == 8:
            est_origen = input("Identificador de la estación origen: ")
            vecindario = input ("Nombre del vecindario: ")

            est_origen = "1168-46"
            vecindario = "la Bordeta"
            optionEight(cont,est_origen,vecindario)

        elif int(inputs) == 9:
            est_origen = input("Identificador de la estación origen: ")
            optionNine(cont, est_origen)

        else:
            sys.exit(0)
    sys.exit(0)

if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=thread_cycle)
    thread.start()
