import curses
from ListaCircularDoble import ListaCircularDoble
from curses import KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP
from random import randint
import time

lista = ListaCircularDoble()

lista.agregar_final(12,1)
lista.agregar_final(13,1)
lista.agregar_final(4,2)
lista.agregar_final(2,2)
lista.agregar_final(9,2)
lista.agregar_final(1,0)
lista.agregar_final(1,9)
lista.agregar_final(7,8)

aux=lista.obtenerNodo()
stdscr = curses.initscr() 
window = curses.newwin(20,70,2,5) 
window.keypad(True)        
i=""
while i!=0:
	i=window.getch()
	if i=="6":
		aux=aux.siguiente
		window.addstr(5,5, i)
		pass
	pass
#aux=aux.siguiente