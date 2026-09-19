
import urllib.request
url = "https://raw.githubusercontent.com/BloodCrests/baile/refs/heads/master/src/SimpleSearch.py"

urllib.request.urlretrieve(url, 'SimpleSearch.py')

import time
import matplotlib.pyplot as plt #Libreria para graficar
import pandas as pd #libreria para manipulacion del dataframe
import SimpleSearch as sp#libreria para algoritmos de busqueda
from SimpleSearch import Node #refernciar la clase node


def plot_tablero(estado):
    peon, enemigos = estado
    tablero=[[(i+j)%2 for j in range(8)] for i in range(8)]#Crea una matriz 8x8 que representa el tablero de ajedrez.
    fig, ax=plt.subplots(figsize=(8,8))#Muestra la matriz tablero como una imagen en los ejes. cmap="gray" asigna un mapa de colores en escala de grises, donde los valores 0 y 1
    ax.imshow(tablero, cmap="gray")
    ax.set_xlim(-0.5, 7.5)#Establece los límites del eje X desde -0.5 hasta 7.5. Esto asegura que el tablero de 8x8
    ax.set_ylim(-0.5, 7.5)#verticalidad
    ax.set_xticks(range(8))#Establece los límites del eje X desde -0.5 hasta 7.5. Esto asegura que el tablero de 8x8
    ax.set_yticks(range(8))#Define las posiciones de las marcas del eje Y
    ax.set_xticklabels(["a", "b", "c", "d", "e", "f", "g", "h"])
    ax.set_yticklabels(["1", "2", "3", "4", "5", "6", "7", "8"])

    # Piezas enemigas
    for fila, col in enemigos:
        ax.text(col, fila, "♟", ha="center", va="center", fontsize=28, color="darkred")

    # Peón
    fila_p, col_p = peon
    ax.text(col_p, fila_p, "♙", ha="center", va="center", fontsize=28, color="blue")

    plt.show()

def sucesores(estado):#Define una función llamada sucesores que toma un argumento estado.
#Este estado es una tupla que representa la situación actual del tablero, conteniendo la posición del peón y las posiciones de los enemigos.
    posicion, enemigos = estado
    fila = posicion[0]#Extrae la fila actual del peón de la variable posicion.
    columna = posicion[1] #Extrae la columna actual del peón de la variable posicion
    sucesores = [] #Aquí se irán añadiendo todos los posibles nuevos estados

    if fila == 1: #Esta condición verifica si el peón se encuentra en su posición inicia
      nueva_posicion = (fila + 2, columna) #Calcula la posición a la que llegaría el peón si avanza dos casillas hacia adelante
      casilla1 = (fila + 1, columna) #Calcula la posición a la que llegaría el peón si avanza dos casillas hacia adelante.
      casilla2 = (fila + 2, columna) #Define la posición de la casilla final, dos casillas delante del peó
      if casilla1 not in enemigos and casilla2 not in enemigos: #Verifica si ambas casillas (la intermedia y la final) están libres de enemigos.
      #Si hay un enemigo en cualquiera de ellas, el peón no puede avanzar dos casillas.
        nuevo_estado = (nueva_posicion, enemigos)#Si el avance de dos casillas es válido, crea un nuevo_estado con la nueva_posicion del peón y el mismo conjunto de enemigos
        sucesores.append(nuevo_estado) #Añade este nuevo_estado a la lista de sucesores.


    nueva_posicion = (fila + 1, columna)#Calcula la posición para un avance de una casilla hacia adelante.
    if nueva_posicion not in enemigos and fila + 1 < 8: #Verifica dos condiciones para este movimiento: nueva_posicion not in enemigos: Que la casilla directamente enfrente del peón esté libre.
    # fila + 1 < 8: Que el peón no se salga del tablero al avanzar (la fila 7 es la última fila válida).Verifica dos condiciones para este movimiento:
      nuevo_estado = (nueva_posicion, enemigos) #Si el avance de una casilla es válido, crea un nuevo_estado
      sucesores.append(nuevo_estado)#Si el avance de una casilla es válido, crea un nuevo_estado

    casilla_izq = (fila + 1, columna - 1)#Calcula la posición de la casilla diagonal izquierda frontal.
    if (columna - 1 >= 0 and fila + 1 < 8 and casilla_izq in enemigos):#Verifica las condiciones para una captura diagonal izquierda:
                                                                      #columna - 1 >= 0: Que la casilla no se salga del tablero por el lado izquierdo.
                                                                      #fila + 1 < 8: Que la casilla no se salga del tablero por arriba.
                                                                      # casilla_izq in enemigos: Que exista un enemigo en esa casilla.

        nuevos_enemigos = enemigos - {casilla_izq} #Si se realiza la captura, crea un nuevo frozenset de enemigos, eliminando la pieza capturada de la casilla_izq.
        nuevo_estado = (casilla_izq, nuevos_enemigos) #Crea un nuevo_estado con el peón en la casilla_izq y el conjunto actualizado de nuevos_enemigos
        sucesores.append(nuevo_estado) #Añade este nuevo_estado a la lista de sucesores.

    casilla_der = (fila + 1, columna + 1)#calcula la posición de la casilla diagonal derecha frontal
    if (columna + 1 < 8 and fila + 1 < 8 and casilla_der in enemigos):#Verifica las condiciones para una captura diagonal derecha:
        nuevos_enemigos = enemigos - {casilla_der}#Si se realiza la captura, crea un nuevo frozenset de enemigos, eliminando la pieza capturada de la casilla_der
        nuevo_estado = (casilla_der, nuevos_enemigos)
        sucesores.append(nuevo_estado)

    return sucesores

def successor(node):
    return [Node(estado, node, node.depth + 1) for estado in sucesores(node.state)]


def es_meta(nodo, estado_meta): #definimos la funcion meta que recibira el nodo, y un estado meta
                                #nodo: representa la posición actual que el algoritmo está revisando
                                #estado_meta: representa el estado objetivo que busca alcanzar

    estado = nodo.state

    peon, enemigos = estado

    fila = peon[0]
    columna = peon[1] #posiciones del peon y enemigos

    if fila == 7 and 0 <= columna <= 7: # La meta se cumple cuando el peón alcanza la última fila del tablero regresa verdadero en caso de que si alcance
        return True

    return False #en caso de no llegar ala fila 7 y columna 7 retornara que no alcanzo el estado meta


def heuristica(nodo, estado_meta):

    estado = nodo.state

    peon, enemigos = estado

    fila = peon[0]

    return 7 - fila


def heuristica_cero(nodo, estado_meta):
    return 0

def heuristica_avanzar_adelante(nodo, estado_meta):
  peon, enemigos = nodo.state
  fila, columna = peon

  # Distancia base a la fila meta (7)
  h_fila = 7 - fila

  # Contar cuántos enemigos están físicamente más adelante
  enemigos_adelante = sum(1 for f, c in enemigos if f > fila)

  return h_fila + enemigos_adelante


MAX_ITER = 500000

def fila(nombre_instancia, nombre_estrategia, buscador, r, tiempo):
  if r is None:
    return {"Instancia": nombre_instancia, "Estrategia": nombre_estrategia,
                "Nodos expandidos": buscador.iterations, "Tiempo (s)": round(tiempo, 4),
                "Longitud": None, "Costo g": None}
  return  {"Instancia": nombre_instancia, "Estrategia": nombre_estrategia,
            "Nodos expandidos": buscador.iterations, "Tiempo (s)": round(tiempo, 4),
            "Longitud": len(r.getPath()) - 1, "Costo g": r.cost}

