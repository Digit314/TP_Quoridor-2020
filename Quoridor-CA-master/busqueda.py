import regla
from sys import maxsize



#Algoritmo BFS (Breadth-First Search)
def BFS(inicio, fin, tablero):
    frontera = []
    visitado = set()
    frontera.append(inicio)
    visitado.add(inicio)
    while frontera != []:
        padre = frontera.pop(0)
        if (padre == fin):
            return True

        hijos = get_sucesores(padre)
        for hijo in hijos:
            if not (hijo in visitado):
                if not bloqueado(hijo[0], hijo[1], padre[0], padre[1], tablero):
                    frontera.append(hijo)
                    visitado.add(hijo)
    return False

def PathMaker(origen, actual):
    tot_camino = [actual]
    while actual in origen.keys():
        actual = origen[actual]
        tot_camino.append(actual)
    return tot_camino

def camino(inicio, fin, tablero):
    frontera = []
    visitado = set()
    frontera.append(inicio)
    visitado.add(inicio)
    distancia = {}
    distancia[inicio] = 0
    while frontera != []:
        padre = frontera.pop(0)
        if (padre == fin):
            return distancia[fin]

        hijos = get_sucesores(padre)
        for hijo in hijos:
            if not (hijo in visitado):
                if not bloqueado(hijo[0], hijo[1], padre[0], padre[1], tablero):
                    frontera.append(hijo)
                    distancia[hijo] = distancia[padre] + 1
                    visitado.add(hijo)

    return maxsize

def bloqueado(x1, y1, x2, y2, tablero):
    for pared in tablero.paredes:
        if (pared.orientacion == "horizontal"):
            if (y1 < y2):
                if (pared.top_l.y == y1 and (pared.top_l.x == x1 or (pared.top_l.x + 1) == x1)):
                    return True
            if (y1 > y2):
                if (pared.top_l.y == y2 and (pared.top_l.x == x1 or (pared.top_l.x + 1) == x1)):
                    return True
        if (pared.orientacion == "vertical"):
            if (x1 < x2):
                if (pared.top_l.x == x1 and (pared.top_l.y == y1 or (pared.top_l.y + 1) == y1)):
                    return True
            if (x1 > x2):
                if (pared.top_l.x == x2 and (pared.top_l.y == y2 or (pared.top_l.y + 1) == y2)):
                    return True
    return False

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