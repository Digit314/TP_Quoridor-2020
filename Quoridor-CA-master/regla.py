from busqueda import *
import random


class Jugador(object):

    def __init__(self, jugador_num):
        self.paredes = 10
        self.jugador_num = jugador_num
        self.ganador_posicion = False

        if (jugador_num == 0):
            self.x = 4
            self.y = 0
            self.opp = 1
        elif (jugador_num == 1):
            self.x = 4
            self.y = 8
            self.opp = 0

        self.pared_opciones = []
        for i in range(8):
            for j in range(8):
                for k in ["horizontal", "vertical"]:
                    top_l = Casilla(i, j)
                    top_r = Casilla(i + 1, j)
                    bot_l = Casilla(i, j + 1)
                    bot_r = Casilla(i + 1, j + 1)
                    pared = Pared(top_l, top_r, bot_l, bot_r, k)
                    self.pared_opciones.append(pared)

    def movimiento(self, x, y, tablero):
        if self.legal_movimiento(x, y, tablero):
            self.x = x
            self.y = y
            if self.jugador_num == 0 and self.y == 8:
                self.ganador_posicion = True
            elif self.jugador_num == 1 and self.y == 0:
                self.ganador_posicion = True
        else:
            raise ("Movimento no permitido")

    def colocar_pared(self, tablero, pared):
        if self.legal_colocamiento(tablero, pared):
            self.paredes -= 1
            tablero.paredes.append(pared)
        else:
            raise ("No es valido colocar la pared")

    def legal_movimiento(self, x, y, tablero):
        # La ubicacion esta en el tablero
        if (x < 0 or x > 8 or y < 0 or y > 8):
            return False
        # El tablero no esta en el mismo recuadro
        if (self.x == x and self.y == y):
            return False
        # Verifica si hay camino fuera de la pared
        if (not self.legal_saltar(x, y, tablero) and (
                abs(self.y - y) > 1 or abs(self.x - x) > 1 or (abs(self.y - y) == 1 and abs(self.x - x) == 1))):
            return False
        # La ubicacion no esta ocupadada por el oponente
        if self.ocupado(x, y, tablero):
            return False
        # El movimiento no esta bloqueado por una pared
        if self.bloqueado(self.x, self.y, x, y, tablero):
            return False
        return True

    def ocupado(self, x, y, b):
        if (self.jugador_num == 0 and b.jugadores[1].x == x and b.jugadores[1].y == y):
            return True
        if (self.jugador_num == 1 and b.jugadores[0].x == x and b.jugadores[0].y == y):
            return True
        return False

    def legal_saltar(self, x, y, b):
        if self.jugador_num == 0:
            opp_num = 1
        else:
            opp_num = 0

        oppx = b.jugadores[opp_num].x
        oppy = b.jugadores[opp_num].y

        if (self.adyacente(self.x, self.y, oppx, oppy) and self.adyacente(oppx, oppy, x, y) and (
        not self.bloqueado(oppx, oppy, x, y, b))):
            if (not self.bloqueado(self.x, self.y, oppx, oppy, b)):
                logicalx = self.x
                logicaly = self.y
                if self.x < oppx:
                    logicalx = oppx + 1
                elif self.x > oppx:
                    logicalx = oppx - 1

                if self.y < oppy:
                    logicaly = oppy + 1
                elif self.y > oppy:
                    logicaly = oppy - 1

                if self.bloqueado(oppx, oppy, logicalx, logicaly, b) or (logicaly < 0) or (logicaly > 8) or (
                        logicalx < 0) or (logicalx > 8):
                    return True
                if x == logicalx and y == logicaly:
                    return True

        return False

    def bloqueado(self, x1, y1, x2, y2, tablero):
        for pared in tablero.paredes:
            if (pared.orientacion == "horizontal"):
                if (y1 < y2):
                    if (pared.top_l.y == y1 and (pared.top_l.x == x1 or (pared.top_l.x + 1) == x1)):
                        return True
                if (y1 > y2):
                    if (pared.top_l.y == y2 and (pared.top_l.x == x2 or (pared.top_l.x + 1) == x2)):
                        return True
            if (pared.orientacion == "vertical"):
                if (x1 < x2):
                    if (pared.top_l.x == x1 and (pared.top_l.y == y1 or (pared.top_l.y + 1) == y1)):
                        return True
                if (x1 > x2):
                    if (pared.top_l.x == x2 and (pared.top_l.y == y2 or (pared.top_l.y + 1) == y2)):
                        return True
        return False

    def adyacente(self, x1, y1, x2, y2):
        if ((abs(x1 - x2) == 1 and abs(y1 - y2) == 0) or (abs(y1 - y2) == 1 and abs(x1 - x2) == 0)):
            return True
        return False

    def legal_colocamiento(self, tablero, pared):
        # pared.print_pared()
        # Jugador tiene suficientes paredes
        if self.paredes == 0:
            return False
        # Se encuentra en el tablero
        if (pared.top_l.x < 0 or pared.top_l.x > 8 or pared.top_l.y < 0 or pared.top_l.y > 8):
            return False
        # Posicion no choca
        for w in tablero.paredes:
            if w.orientacion == "horizontal" and pared.orientacion == "horizontal":
                if w.top_l.y == pared.top_l.y and ((w.top_l.x == pared.top_l.x) or (w.top_l.x - 1 == pared.top_l.x) or (
                        w.top_l.x + 1 == pared.top_l.x)):
                    return False
            if w.orientacion == "vertical" and pared.orientacion == "vertical":
                if w.top_l.x == pared.top_l.x and ((w.top_l.y == pared.top_l.y) or (w.top_l.y - 1 == pared.top_l.y) or (
                        w.top_l.y + 1 == pared.top_l.y)):
                    return False
            if (w.top_l.x == pared.top_l.x and w.top_l.y == pared.top_l.y):
                return False
        # Posicion no encierra completamente al jugador oponente
        if not self.camino_existe(tablero, pared):
            return False

        return True

    def camino_existe(self, tablero, pared):
        tablero.paredes = tablero.paredes + [pared]
        p1_camino = False
        p2_camino = False
        win_fila1 = [(0, 8), (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8)]
        win_fila2 = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0)]

        for casilla in win_fila1:
            if BFS((tablero.jugadores[0].x, tablero.jugadores[0].y), casilla, tablero):
                p1_camino = True
        for casilla in win_fila2:
            if BFS((tablero.jugadores[1].x, tablero.jugadores[1].y), casilla, tablero):
                p2_camino = True
        tablero.paredes = tablero.paredes[:-1]
        return (p1_camino and p2_camino)

    def posibleMovimientos(self, regla, oponente=False):
        movimientos = []
        if not oponente:
            movimientos.append(Casilla(self.x, self.y - 1))
            movimientos.append(Casilla(self.x, self.y + 1))
            movimientos.append(Casilla(self.x + 1, self.y))
            movimientos.append(Casilla(self.x - 1, self.y))
            movimientos.append(Casilla(self.x, self.y - 2))
            movimientos.append(Casilla(self.x, self.y + 2))
            movimientos.append(Casilla(self.x - 2, self.y))
            movimientos.append(Casilla(self.x + 2, self.y))
            movimientos.append(Casilla(self.x - 1, self.y - 1))
            movimientos.append(Casilla(self.x + 1, self.y + 1))
            movimientos.append(Casilla(self.x + 1, self.y - 1))
            movimientos.append(Casilla(self.x - 1, self.y + 1))

            result = []
            for m in movimientos:
                if self.legal_movimiento(m.x, m.y, regla):
                    result.append(m)
        else:
            opp = regla.jugadores[self.opp]
            movimientos.append(Casilla(opp.x, opp.y - 1))
            movimientos.append(Casilla(opp.x, opp.y + 1))
            movimientos.append(Casilla(opp.x + 1, opp.y))
            movimientos.append(Casilla(opp.x - 1, opp.y))
            movimientos.append(Casilla(opp.x, opp.y - 2))
            movimientos.append(Casilla(opp.x, opp.y + 2))
            movimientos.append(Casilla(opp.x - 2, opp.y))
            movimientos.append(Casilla(opp.x + 2, opp.y))
            movimientos.append(Casilla(opp.x - 1, opp.y - 1))
            movimientos.append(Casilla(opp.x + 1, opp.y + 1))
            movimientos.append(Casilla(opp.x + 1, opp.y - 1))
            movimientos.append(Casilla(opp.x - 1, opp.y + 1))

            result = []
            for m in movimientos:
                if opp.legal_movimiento(m.x, m.y, regla):
                    result.append(m)

        return result

    def posibleParedes(self, regla, oponente=False):
        paredes = []
        print('Ingresa a posible paredes')
        if not oponente:
            for pared in self.pared_opciones:
                if self.legal_colocamiento(regla, pared):
                    paredes.append(pared)
        else:
            opp = regla.jugadores[self.opp]
            for pared in self.pared_opciones:
                if opp.legal_colocamiento(regla, pared):
                    paredes.append(pared)

        return paredes

    def print_jugador(self):
        return "Ubicacion jugador: (%d, %d)\nParedes restantes: %d\n" % (self.x, self.y, self.paredes)


class Casilla:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def print_casilla(self):
        return "Casilla ubicacion: (%d, %d)" % (self.x, self.y)


class Pared:

    def __init__(self, top_l, top_r, bot_l, bot_r, orientacion):
        self.top_l = top_l
        self.top_r = top_r
        self.bot_l = bot_l
        self.bot_r = bot_r
        self.orientacion = orientacion

    def print_pared(self):
        print("Pared Inicio")
        print("Arriba" + self.top_l.print_casilla())
        print("Abajo" + self.top_r.print_casilla())
        print("Izquierda" + self.bot_l.print_casilla())
        print("Derecha" + self.bot_r.print_casilla())
        print("Pared Fin")


class Regla:

    def __init__(self, bot_cont='0'):
        import computadora
        if bot_cont == '1':
            self.jugadores = [Jugador(0), computadora.Min_max(1)]
        elif bot_cont == '2':
            self.jugadores = [computadora.Min_max(0), computadora.Min_max(1)]
        else:
            self.jugadores = [Jugador(0), Jugador(1)]
        self.paredes = []
        self.casillas = [[], [], [], [], [], [], [], [], []]
        self.actual = 0
        self.actual = random.randint(0, 1)

        for i in range(0, 8):
            for j in range(0, 8):
                self.casillas[i].append(Casilla(i, j))

    def printTablero(self):
        print(self.casillas)

    def sigTurno(self):
        if self.actual == 0:
            self.actual = 1
        else:
            self.actual = 0