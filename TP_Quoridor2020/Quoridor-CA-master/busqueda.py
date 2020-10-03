from sys import *

#BUSQUEDA DEL CAMINO MAS CORTO DEL INICIO AL FINAL
#Se comienza en la raiz y se exploran todos los vecinos de este nodo hijo.
def bfs(inicio, final):
    frontera = []
    visitado = set()
    frontera.append(inicio)
    visitado.add(inicio)
    while frontera != []:
        padre = frontera.pop(0)
        if (padre == final):
            return True
    return False

#FUNCION QUE DEFINE EL CAMINO DESDE LA POSICION INICIAL AL LLEGAR AL FINAL DEL TABLERO
def camino(inicio, final, tablero):
    frontera = []
    visitado = set()
    frontera.append(inicio)
    visitado.add(inicio)
    distancia = {}
    distancia[inicio] = 0
    while frontera != []:
        padre = frontera.pop(0)
        if (padre == final):
            return distancia[final]
        hijos = get_sucesores(padre)
        for hijo in hijos:
            if not (hijo in visitado):
                    frontera.append(hijo)
                    distancia[hijo] = distancia[padre] + 1
                    visitado.add(hijo)
    return maxsize

#FUNCION QUE OBTIENE TODOS LOS NODOS HIJOS DEL PADRE QUE SE ENCUENTRA
def get_sucesores(padre):
    hijos = set()
    p0 = padre[0]
    p1 = padre[1]
    x1 = padre[0] - 1
    x2 = padre[0] + 1
    y1 = padre[1] - 1
    y2 = padre[1] + 1
    if (x1 >= 0):
        hijos.add((x1, p1))
    if (y1 >= 0):
        hijos.add((p0, y1))
    if (x2 <= 8):
        hijos.add((x2, p1))
    if (y2 <= 8):
        hijos.add((p0, y2))
    return hijos