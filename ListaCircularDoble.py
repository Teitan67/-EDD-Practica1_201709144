from jugador import Jugador

class ListaCircularDoble:

    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.size=0

    def vacia(self):
        return self.primero==None
            
    def agregar_final(self, user,punt):
        if self.vacia():
            self.primero=self.ultimo=Jugador(user,punt)
        else:
            aux =self.ultimo
            self.ultimo=aux.siguiente=Jugador(user,punt)
            self.ultimo.anterior=aux
            self.primero.anterior=self.ultimo
            self.ultimo.siguiente=self.primero
        self.size+=1

    def agregar_inicio(self, user,punt):
        if self.vacia():
            self.primero=self.ultimo=Jugador(user,punt)
        else:
            aux= Jugador(user,punt)
            aux.siguiente=self.primero
            self.primero.anterior=aux
            self.primero=aux
            self.primero.anterior=self.ultimo
            self.ultimo.siguiente=self.primero
        self.size+=1

    def busqueda(self, user):
        aux=self.primero
        buscando=True
        while buscando:
            if aux.usuario==user:
                buscando=False
                return aux
                pass
            if aux.siguiente==self.primero or aux.siguiente==None :
                buscando=False
                return None
            pass
            aux=aux.siguiente
        pass
   
    def obtenerNodo(self):
        return  self.primero

    def obtenerTamaño(self):
        return self.size

    def existe(self, user):
        aux=self.primero
        buscando=True
        while buscando:
            if aux.usuario==user:
                buscando=False
                return True
                pass
            if aux.siguiente==self.primero or aux.siguiente==None :
                buscando=False
                return False
            pass
            aux=aux.siguiente
        pass

   
            

