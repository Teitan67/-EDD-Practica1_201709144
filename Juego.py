
import curses
from ListaCircularDoble import ListaCircularDoble
from curses import KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP
from random import randint
import time

#Variables----------------------------------------------
x_ventana = 70
y_ventana = 20
VELOCIDAD = 100
USER =""
x_tablero = x_ventana - 2
y_tablero = y_ventana - 2
s_tamaño = 3
x_serpiente = s_tamaño + 1
y_serpiente = 3
listaD = ListaCircularDoble()

#Clases------------------------------------------------
class Cuerpo(object):
    def __init__(self, x, y, char='■'):
        self.x = x
        self.y = y
        self.char = char

    @property
    def coor(self):
        return self.x, self.y

class Serpiente(object):
    REV_DIR_MAP = {
        KEY_UP: KEY_DOWN, KEY_DOWN: KEY_UP,
        KEY_LEFT: KEY_RIGHT, KEY_RIGHT: KEY_LEFT,
    }

    def __init__(self, x, y, window):
        self.listaDoble = []
        self.PUNTAJE = 0
        self.timeout = VELOCIDAD

        for i in range(s_tamaño, 0, -1):
            self.listaDoble.append(Cuerpo(x - i, y))

        self.listaDoble.append(Cuerpo(x, y, 'O'))
        self.window = window
        self.direction = KEY_RIGHT
        self.xy_cola = (x, y)
        self.direccion_mapa = {
            KEY_UP: self.move_up,
            KEY_DOWN: self.move_down,
            KEY_LEFT: self.move_left,
            KEY_RIGHT: self.move_right
        }

    @property
    def puntaje(self):
        return ' Puntaje : {} '.format(self.PUNTAJE)

    def crecer(self, listaDoble):
        self.listaDoble.extend(listaDoble)

    def comer(self, bocadillo):
        bocadillo.reset()
        cuerpo = Cuerpo(self.xy_cola[0], self.xy_cola[1])
        self.listaDoble.insert(-1, cuerpo)
        self.PUNTAJE += 1
        if self.PUNTAJE  == 5:
            self.timeout -= 10
            self.window.timeout(self.timeout)

    @property
    def choque(self):
        return any([cuerpo.coor == self.cabeza.coor
                    for cuerpo in self.listaDoble[:-1]])

    def recarga(self):
        ultimo = self.listaDoble.pop(0)
        ultimo.x = self.listaDoble[-1].x
        ultimo.y = self.listaDoble[-1].y
        self.listaDoble.insert(-1, ultimo)
        self.xy_cola = (self.cabeza.x, self.cabeza.y)
        self.direccion_mapa[self.direction]()

    def change_direction(self, direction):
        if direction != Serpiente.REV_DIR_MAP[self.direction]:
            self.direction = direction

    def render(self):
        for cuerpo in self.listaDoble:
            self.window.addstr(cuerpo.y, cuerpo.x, cuerpo.char)

    @property
    def cabeza(self):
        return self.listaDoble[-1]

    @property
    def coor(self):
        return self.cabeza.x, self.cabeza.y

    def move_up(self):
        self.cabeza.y -= 1
        if self.cabeza.y < 1:
            self.cabeza.y = y_tablero

    def move_down(self):
        self.cabeza.y += 1
        if self.cabeza.y > y_tablero:
            self.cabeza.y = 1

    def move_left(self):
        self.cabeza.x -= 1
        if self.cabeza.x < 1:
            self.cabeza.x = x_tablero

    def move_right(self):
        self.cabeza.x += 1
        if self.cabeza.x > x_tablero:
            self.cabeza.x = 1

class Bocadillo(object):
    def __init__(self, window, char='&'):
        self.x = randint(1, x_tablero)
        self.y = randint(1, y_tablero)
        self.char = char
        self.window = window

    def render(self):
        self.window.addstr(self.y, self.x, self.char)

    def reset(self):
        self.x = randint(1, x_tablero)
        self.y = randint(1, y_tablero)



    
#Funciones---------------------------------------------------
def juego(user):
    curses.initscr()
    curses.flash()
    window = curses.newwin(y_ventana, x_ventana, 2, 5)
    window.timeout(VELOCIDAD)
    window.keypad(1)
    curses.noecho()
    curses.curs_set(0)
    window.border(0)

    serpiente = Serpiente(x_serpiente, y_serpiente, window)
    bocadillo = Bocadillo(window, '+')

    while True:
        window.clear()
        window.border(0)
        serpiente.render()
        bocadillo.render()
        window.addstr(0,0, '[ESC] Inicio')
        window.addstr(0,30, '  JUGAR  ') 
        window.addstr(19,30, ' Usuario: '+user+'  ')    
        window.addstr(0, 55, serpiente.puntaje)
        event = window.getch()

        if event == 27:
            break

        if event in [KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT]:
            serpiente.change_direction(event)

        if serpiente.cabeza.x == bocadillo.x and serpiente.cabeza.y == bocadillo.y:
            serpiente.comer(bocadillo)

        serpiente.recarga()
        if serpiente.choque:
            key = -1
            while key != 27:
                key = window.getch()
                nodo=listaD.busqueda(user)
                if nodo!=None:
                    nodo.puntaje=serpiente.puntaje
                window.addstr(10,30, 'GAME OVER')
            break 

def generar_menu(win):
    generar_titulo(win,' Menu Principal ')      
    win.addstr(7,21, '1.  Jugar')            
    win.addstr(8,21, '2.  Puntaje')      
    win.addstr(9,21, '3.  Seleccionar usuario') 
    win.addstr(10,21, '4.  Reportes')         
    win.addstr(11,21, '5.  Carga masiva')    
    win.addstr(12,21, '6.  Salir')            
    win.timeout(-1)                        

def generar_titulo(win,var):
    win.clear()                         
    win.border(0)                       
    x_start = round((67-len(var))/2)   
    win.addstr(0,x_start,var)
    window.addstr(0,0, '[ESC] Inicio')
    window.addstr(19,30, ' Usuario: '+USER+'  ')            

def wait_esc(win):
    key = window.getch()
    while key!=27:
        key = window.getch()

def genear_Usuario(window):
    NoTerminado= True
    usuario=""
    i=0
    L=0
    window.addstr(8,20,'Ingrese nombre de usuario')
    window.addstr(15,27,'5 letras')
    while NoTerminado:
        caracter=window.getkey()
        if caracter!="\n":
            usuario=usuario+caracter
            window.addstr(12,29+i,caracter)
            i=i+1
            pass
        elif caracter=="\n" and len(usuario)==5:
            L=5
        if len(usuario)==5:
            window.addstr(5,15,'PRESIONA CUALQUIER TECLA PARA JUGAR')
            curses.flash();
            pass
        if len(usuario)+L>=6:
            #AQUI SE GUARDA

            listaD.agregar_final(usuario,0)
            return usuario
            NoTerminado= False
            pass
    return usuario
def impresion():
    aux=listaD.obtenerNodo()
    event=window.getch()
    if event=="d" and aux.siguiente!=None:
        aux=aux.siguiente
        pass
    elif event=="a" and aux.siguiente!=None:
        aux=aux.anterior
        pass
    imprimirUsuarios(aux)
def imprimirUsuarios(Nodo):
    aux=Nodo
    tamaño=listaD.obtenerTamaño()
    User1=User2=User3="VACIO"

    if tamaño!=0:
        User2=aux.usuario
        if aux.siguiente!=None:
            User3=aux.siguiente.usuario
            User1=aux.anterior.usuario
            pass
        pass

    window.addstr(10,33,User2)
    window.addstr(10,23,'<---->')
    window.addstr(10,40,'<---->')
    window.addstr(11,16,User1)
    window.addstr(11,47,User3)

#Principal------------------------------------------------
if __name__ == '__main__':
    stdscr = curses.initscr() 
    window = curses.newwin(20,70,2,5) 
    window.keypad(True)     
    curses.noecho()        
    curses.curs_set(0)      
    generar_menu(window)      
    keystroke = -1

    while(keystroke==-1):
        keystroke = window.getch() 
        if(keystroke==49): 
            window.clear()
            if USER=="":
                
                juego(genear_Usuario(window))
                wait_esc(window)
                generar_menu(window)
                keystroke=-1
                pass
            else:
                juego(USER)
                wait_esc(window)
                generar_menu(window)
                keystroke=-1
        elif(keystroke==50):
            generar_titulo(window, ' Puntuaciones ')
            wait_esc(window)
            generar_menu(window)
            keystroke=-1
        elif(keystroke==51):
            generar_titulo(window, ' Seleccion de usuario ')
            impresion()
            wait_esc(window)
            generar_menu(window)
            keystroke=-1
        elif(keystroke==52):
            generar_titulo(window, ' Reportes ')
            wait_esc(window)
            generar_menu(window)
            keystroke=-1
        elif(keystroke==53):
            generar_titulo(window,' Carga masiva ')
            wait_esc(window)
            generar_menu(window)
            keystroke=-1
        elif(keystroke==54):
            pass
        else:
            keystroke=-1

    curses.endwin() 