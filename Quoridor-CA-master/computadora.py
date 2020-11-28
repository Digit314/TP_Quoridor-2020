
from regla import *
import busqueda
import random
import copy
from sys import maxsize
minint = -maxsize - 1

# Clase de interfaz BOT
class Quoribot(Jugador):
    def __init__(self, num):
        super(Quoribot, self).__init__(num)
        if self.jugador_num == 1:
            self.win_fila = [(0, 0), (1, 0), (2, 0), (3, 0),
                             (4, 0), (5, 0), (6, 0), (7, 0), (8, 0)]
            self.opp_fila = [(0, 8), (1, 8), (2, 8), (3, 8),
                             (4, 8), (5, 8), (6, 8), (7, 8), (8, 8)]
            self.opp = 0
        else:
            self.opp_fila = [(0, 0), (1, 0), (2, 0), (3, 0),
                             (4, 0), (5, 0), (6, 0), (7, 0), (8, 0)]
            self.win_fila = [(0, 8), (1, 8), (2, 8), (3, 8),
                             (4, 8), (5, 8), (6, 8), (7, 8), (8, 8)]
            self.opp = 1

#Algoritmo miniMax
class Min_max(Quoribot):
    def __init__(self, num):
        super(Min_max, self).__init__(num)

    def finalMovimiento(self, regla):
        movimientos = {}
        posible_paredes = self.posibleParedes(regla)
        posible_movimientos = self.posibleMovimientos(regla)
        print("Ingresa a finalMovimiento minMax")

        for m in posible_movimientos:
            node = Nodo(self.jugador_num, regla, "movimiento", None, m.x, m.y)
            movimientos[node] = self.miniMax(node, 0, True)
        for w in posible_paredes:
            node = Nodo(self.jugador_num, regla, "pared", w)
            movimientos[node] = self.miniMax(node, 0, True)

        movimiento = max(movimientos, key=movimientos.get)

        if movimiento.movimiento_type == "movimiento":
            self.movimiento(movimiento.movimientoX,
                            movimiento.movimientoY, regla)
        else:
            self.colocar_pared(regla, movimiento.pared)

    def miniMax(self, node, depth, maximizingJugador):
        if depth == 0 or self.ganadorMovimiento(node):
            return self.heuristica(node, node.regla)

        if maximizingJugador:
            bestValue = minint
            bestMovimiento = None
            hijos = node.hijos(maximizingJugador)
            for child in hijos:
                v = self.miniMax(child, depth - 1, False)
                bestValue = max(bestValue, v)
            return bestValue

        else:
            bestValue = maxsize
            hijos = node.hijos(maximizingJugador)
            for child in hijos:
                v = self.miniMax(child, depth - 1, True)
                bestValue = min(bestValue, v)
            return bestValue

    def ganadorMovimiento(self, node):
        if node.movimiento_type == "movimiento":
            if (node.movimientoX, node.movimientoY) in self.win_fila:
                return True
        return False

    def heuristica(self, node, regla):
        opp = regla.jugadores[self.opp]
        if node.movimiento_type == "movimiento":
            minMovimientoCamino = minCaminoLen(
                node.movimientoX, node.movimientoY, self.win_fila, regla)
            minOppCamino = minCaminoLen(opp.x, opp.y, self.opp_fila, regla)
            return minOppCamino - minMovimientoCamino
        else:
            regla.paredes = regla.paredes + [node.pared]
            minWinCamino = minCaminoLen(self.x, self.y, self.win_fila, regla)
            minOppCamino = minCaminoLen(opp.x, opp.y, self.opp_fila, regla)
            regla.paredes = regla.paredes[:-1]
            return minOppCamino - minWinCamino


class Nodo:
    def __init__(self, jugador_num, regla, movimiento_type, pared=None, movimientoX=None, movimientoY=None):
        self.movimiento_type = movimiento_type
        self.pared = pared
        self.movimientoX = movimientoX
        self.movimientoY = movimientoY
        self.jugador_num = jugador_num
        new_regla = copy.deepcopy(regla)
        if self.movimiento_type == "movimiento":
            new_regla.jugadores[self.jugador_num].x = self.movimientoX
            new_regla.jugadores[self.jugador_num].y = self.movimientoY
        else:
            new_regla.jugadores[self.jugador_num].colocar_pared(
                new_regla, self.pared)

        self.regla = new_regla
        self.opp_num = new_regla.jugadores[self.jugador_num].opp

    def hijos(self, maximizingJugador):
        hijos = []
        oponente_posible_movimientos = self.regla.jugadores[self.opp_num].posibleMovimientos(
            self.regla, True)
        oponente_posible_paredes = self.regla.jugadores[self.jugador_num].posibleParedes(
            self.regla, True)
        for m in oponente_posible_movimientos:
            node = Nodo(self.opp_num, self.regla, "movimiento", None, m.x, m.y)
            hijos.append(node)
        for w in oponente_posible_paredes:
            hijos.append(Nodo(self.opp_num, self.regla, "pared", w))
        return hijos


def minCaminoLen(x, y, win_fila, regla):
    minCamino = maxsize
    for fin in win_fila:
        camino_len = busqueda.camino((x, y), fin, regla)
        if camino_len < minCamino:
            minCamino = camino_len
    return minCamino
