import busqueda
import copy
from reglas import *
from sys import maxsize

minint = -maxsize - 1

class Computadora(Jugador):
    def __init__(self, num):
        super().__init__(num)
        if self.jugador_num == 1:
            self.win_fila = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0)]
            self.opp_fila = [(0, 8), (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8)]
            self.opp = 0
        else:
            self.opp_fila = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0)]
            self.win_fila = [(0, 8), (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8)]
            self.opp = 1

class Minimax(Computadora):
    def __init__(self, num):
        super().__init__(num)

    def finalMovimiento(self, estado):
        movimientos = {}
        posible_movimientos = self.posibleMovimientos(estado)
        for m in posible_movimientos:
            nodo = Nodo(self.jugador_num, estado, "movimiento", m.x, m.y)
            movimientos[nodo] = self.minimaxalgoritmo(nodo, 0, minint, maxsize, True)
        movimiento = max(movimientos, key=movimientos.get)
        if movimiento.movimiento_type == "movimiento":
            self.movimiento(movimiento.movimientoX, movimiento.movimientoY, estado)

    def miniMax(self, nodo, profundidad, maximizeJugador):
        if profundidad == 0 or self.ganadorMovimiento(nodo):
            return self.sfs(nodo, nodo.estado)
        if maximizeJugador:
            mejorPosicion = minint
            hijos = nodo.hijos(maximizeJugador)
            for hijo in hijos:
                v = self.miniMax(hijo, profundidad - 1, False)
                mejorPosicion = max(mejorPosicion, v)
            return mejorPosicion
        else:
            mejorPosicion = maxsize
            hijos = nodo.hijos(maximizeJugador)
            for hijo in hijos:
                v = self.miniMax(hijo, profundidad - 1, True)
                mejorPosicion = min(mejorPosicion, v)
            return mejorPosicion

    #Algoritmo que reduce el numero de nodos evaluados en un arbol
    def minimaxalgoritmo(self, nodo, profundidad, maximo, minimo, maximizeJugador):
        if profundidad == 0 or self.ganadorMovimiento(nodo):
            return self.sfs(nodo, nodo.estado)
        if maximizeJugador:
            mejorPosicion = minint
            hijos = nodo.hijos(maximizeJugador)
            for hijo in hijos:
                v = self.minimaxalgoritmo(hijo, profundidad - 1, maximo, minimo, False)
                mejorPosicion = max(mejorPosicion, v)
                maximo = max(maximo, mejorPosicion)
                if minimo <= maximo:
                    break
            return mejorPosicion
        else:
            mejorPosicion = maxsize
            hijos = nodo.hijos(maximizeJugador)
            for hijo in hijos:
                v = self.minimaxalgoritmo(hijo, profundidad - 1, maximo, minimo, True)
                mejorPosicion = min(mejorPosicion, v)
                if minimo <= maximo:
                    break
            return mejorPosicion

    def ganadorMovimiento(self, nodo):
        if nodo.movimiento_type == "movimiento":
            if (nodo.movimientoX, nodo.movimientoY) in self.win_fila:
                return True
        return False

    def sfs(self, nodo, estado):
        opp = estado.jugadores[self.opp]
        if nodo.movimiento_type == "movimiento":
            minMovimientoCamino = minCaminoLen(nodo.movimientoX, nodo.movimientoY, self.win_fila, estado)
            minOppCamino = minCaminoLen(opp.x, opp.y, self.opp_fila, estado)
            return minOppCamino - minMovimientoCamino

#Declarando el nodo
class Nodo():
    def __init__(self, jugador_num, estado, movimiento_type, movimientoX=None, movimientoY=None):
        self.movimiento_type = movimiento_type
        self.movimientoX = movimientoX
        self.movimientoY = movimientoY
        self.jugador_num = jugador_num
        nuevo_estado = copy.deepcopy(estado)
        if self.movimiento_type == "movimiento":
            nuevo_estado.jugadores[self.jugador_num].x = self.movimientoX
            nuevo_estado.jugadores[self.jugador_num].y = self.movimientoY


        self.estado = nuevo_estado
        self.opp_num = nuevo_estado.jugadores[self.jugador_num].opp

    def hijos(self):
        hijos = []
        oponente_posible_movimientos = self.estado.jugadores[self.opp_num].posibleMovimientos(self.estado, True)
        for m in oponente_posible_movimientos:
            nodo = Nodo(self.opp_num, self.estado, "movimiento", m.x, m.y)
            hijos.append(nodo)
        return hijos

#Funcion que halla el caminito (el tamaño mas minimo)
def minCaminoLen(x, y, win_fila, estado):
    minCamino = maxsize
    for final in win_fila:
        camino_len = busqueda.camino((x, y), final, estado)
        if camino_len < minCamino:
            minCamino = camino_len
    return minCamino