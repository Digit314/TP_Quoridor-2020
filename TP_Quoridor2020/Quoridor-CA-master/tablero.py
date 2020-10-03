import tkinter
import math
import time
from sys import argv
from pip._vendor.distlib.compat import raw_input
from reglas import *

CASILLA_SIZE = 50
JUGADOR_SIZE = int(.8 * CASILLA_SIZE)
CASILLA_PADDING = 10
BORDER = 40
NUM_FILAS = 9 #NUM_FILAS = int(input("INGRESE NUMERO DE CASILLAS: "))
NUM_COLUMNAS = int(NUM_FILAS)
CONTROL_WIDTH = 100
COLORS = {'bg': '#FDFDFD', 'casilla': '#5ACFA5', 'panel': '#271717', 'text': '#ffffff', 'jugadores': ['#17A2A7', '#E5164B'], 'jugadores-sombras': ['#91355C', '#7A14DF']}
ALIAS = raw_input("Nombre:  ")
JUGADORES = [ALIAS, 'Bot01']

class Tablero():
	def __init__(self):
		self.root = None
		self.canvas = None
		self.width = 0
		self.height = 0
		self.jugadores = [ALIAS, None]
		self.casillas = []
		self.movimiento = None
		self.jugador_sombra = None
		self.turno = 0
		self.reglas = None
		self.computadora_count = '0'
		self.actual_element = None
		for _ in range(NUM_COLUMNAS):
			self.casillas.append(list(range(NUM_FILAS)))

	def nuevoJuego(self, computadora_count):
		if self.root:
			self.root.destroy()
		self.root = tkinter.Tk()
		self.root.title("Quoridor 2020")
		self.root.bind("<Escape>", lambda e: self.handleSalir())
		self.root.bind("<Enter>", lambda e: self.setMovimiento("movimientoPawn")) # "m"
		self.root.bind("<Motion>", lambda e: self.handleMotion(e.x, e.y))
		self.root.bind("<Button-1>", lambda e: self.handleClick(e.x, e.y))
		self.height = (NUM_FILAS*CASILLA_SIZE) + (NUM_FILAS*CASILLA_PADDING) + (2*BORDER)
		self.width = self.height + CONTROL_WIDTH
		self.canvas = tkinter.Canvas(self.root, width=self.width, height=self.height, background=COLORS['bg'])
		self.canvas.pack()
		self.dibujarCasillas()
		self.estado = Reglas(computadora_count)
		self.computadora_count = computadora_count
		self.turno = self.estado.actual
		self.dibujarJugadores()
		self.root.mainloop()

	def dibujarCasillas(self):
		for j in range(NUM_FILAS):
			for i in range(NUM_COLUMNAS):
				x = BORDER + CASILLA_PADDING/2 + i*(CASILLA_SIZE+CASILLA_PADDING)
				y = BORDER + CASILLA_PADDING/2 + j*(CASILLA_SIZE+CASILLA_PADDING)
				casilla = self.canvas.create_rectangle(x,y, x+CASILLA_SIZE, y+CASILLA_SIZE, fill=COLORS['casilla'])
				self.casillas[j][i] = casilla

	def dibujarJugadores(self, sombra=False):
		for k in range(len(JUGADORES)):
			jugador = self.estado.jugadores[k]
			fila = jugador.x
			columna = jugador.y
			self.dibujarJugador(fila, columna, k, jugador, sombra)

	def dibujarJugador(self, fila, columna, num, jugador, sombra):
		x, y = gridToCoords(fila,columna)
		if not sombra and self.jugadores[num]:
			self.canvas.delete(self.jugadores[num])
			self.jugadores[num] = None
		elif sombra and self.jugador_sombra:
			self.canvas.delete(self.jugador_sombra)
		color = COLORS['jugadores'][num]
		if sombra:
			color = COLORS['jugadores-sombras'][num]
		radius = JUGADOR_SIZE/2
		pawn = self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill=color, outline="")
		if not sombra:
			self.jugadores[num] = pawn
		else:
			self.jugador_sombra = pawn

	def setMovimiento(self, movimiento):
		self.movimiento = movimiento
		self.refresh()

	def handleSalir(self):
		self.root.destroy()

	def handleMotion(self, x, y):
		if self.computadora_count == '2' or (self.turno == 1 and self.computadora_count == '1'):
				return
		i, j = coordsToGrid(x,y)
		if self.movimiento == 'movimientoPawn':
			if self.estado.jugadores[self.turno].legal_movimiento(i,j,self.estado):
				self.dibujarJugador(i, j, self.turno, self.estado.jugadores[self.turno], True)
			elif self.jugador_sombra != None:
				self.canvas.delete(self.jugador_sombra)

	def handleClick(self, x, y):
		if (self.computadora_count == '2'):
			while not self.estado.jugadores[0].posicion_ganadora and not self.estado.jugadores[1].posicion_ganadora:
				self.estado.jugadores[self.turno].finalMovimiento(self.estado)
				self.sigTurno()
				self.refresh()
				time.sleep(.5)
		else:
			i, j = coordsToGrid(x,y)
			if self.movimiento == 'movimientoPawn':
				if self.estado.jugadores[self.turno].legal_movimiento(i,j,self.estado):
					self.estado.jugadores[self.turno].movimiento(i,j,self.estado)
					self.sigTurno()
					self.refresh()
			if self.handleGanador():
				return
			if self.turno == 1 and self.computadora_count == '1':
				self.estado.jugadores[self.turno].finalMovimiento(self.estado)
				self.sigTurno()
				self.refresh()
				time.sleep(.5)

	def handleGanador(self):
		ganador = False
		for p in self.estado.jugadores:
			if p.posicion_ganadora:
				x = self.width - CONTROL_WIDTH/2 - BORDER
				y = self.height/2
				i =  JUGADORES[p.jugador_num] + " wins "
				self.canvas.create_text((x,y), text=i, justify='center', width=CONTROL_WIDTH, font=("Arial", 14, "bold"))
				ganador = True
				break
		if ganador:
			self.root.unbind("<Motion>")
			self.root.unbind("<Button-1>")
		return ganador

	def refresh(self):
		self.clearSombra()
		self.dibujarJugadores()
		self.root.update()
		self.handleGanador()

	def sigTurno(self):
		self.estado.sigTurno()
		self.turno = self.estado.actual

	def clearSombra(self):
		if self.jugador_sombra != None:
			self.canvas.delete(self.jugador_sombra)
			self.jugador_sombra = None

##Escribe los valores de x e y y los retorna como coordenadas precisas de pixeles
def gridToCoords(i, j):
	if (0<=i<=8) and (0<=j<=8):
		x = BORDER + CASILLA_PADDING/2 + (i)*(CASILLA_SIZE+CASILLA_PADDING)
		y = BORDER + CASILLA_PADDING/2 + (j)*(CASILLA_SIZE+CASILLA_PADDING)
		return (x+(CASILLA_SIZE/2)), (y+(CASILLA_SIZE/2))
	else:
		return None, None

def coordsToGrid(x, y):
	x -= BORDER
	y -= BORDER
	i = int(math.floor(float(x)/(CASILLA_SIZE+CASILLA_PADDING)))
	j = int(math.floor(float(y)/(CASILLA_SIZE+CASILLA_PADDING)))
	if (0<=i<=8) and (0<=j<=8):
		return i, j
	else:
		return None, None

if __name__ == '__main__':
	tablero = Tablero()
	if len(argv) == 2:
		if argv[1] == '1':
			tablero.nuevoJuego('1')
		elif argv[1] == '2':
			tablero.nuevoJuego('2')
	else:
		tablero.nuevoJuego('0')