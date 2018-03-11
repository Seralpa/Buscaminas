# -*- coding: UTF-8 -*-

from __future__ import print_function
from random import randint

COLS_NAME="abcdefghijklmnopqrstuvwxyz=+-:/"
ROWS_NAME="ABCDEFGHIJKLMNOPQRSTUVWXYZ@#$%&"
# Caracteres para dibujar cuadros
COE = u'\u2500' # ─
CNS = u'\u2502' # │
CES = u'\u250C' # ┌
CSO = u'\u2510' # ┐
CNE = u'\u2514' # └
CON = u'\u2518' # ┘
COES = u'\u252C' # ┬
CNES = u'\u251C' # ├
CONS = u'\u2524' # ┤
CONE = u'\u2534' # ┴
CSOM = u'\u2593' # ▒ 

def menuInicial(): #Este metodo imprime en pantalla un "menu de inicio" y devuelve la variable eleccion que luego el modulo principal usara para dirigir el flujo del prograna. 
    print(" BUSCAMINAS")
    print("------------") 
    print(" 1. Principiante (9x9, 10 minas)") 
    print(" 2. Intermedio (16x16, 40 minas)") 
    print(" 3. Experto (16x30, 99 minas)") 
    print(" 4. Leer de fichero") 
    print(" 5. Salir\n") 

    eleccion= int(raw_input("Escoja opcion: "))
    while eleccion<1 or 5<eleccion:
        eleccion= int(raw_input("Esa no es una opcion valida, vuelve a intentarlo."))
    return eleccion

def leerFichero():
    tablero=list()
    i,j=0,0
    fichero= raw_input("Introduzca el nombre del fichero: _")
    with open(fichero,'r') as f:
        f.readline
        for linea in f:
            tablero.append(list())
            for c in linea:
                if c=='.':
                    tablero[i].append(Cell(i,j))
                if c=='*':
                    tablero[i].append(Cell(i,j,True))
                else:
                    raise Exception("Error en el fichero")
                j+=1
            i+=1

def generarTablero(tamano,minas):
    tablero=list()
    for i in range(tamano[0]):
        tablero.append(list())
        for j in range(tamano[1]):
            tablero[i].append(Cell(i,j))
    for _ in range(minas):
        while True:
            i=randint(0,tamano[0])
            j=randint(0,tamano[1])
            if not tablero[i][j].has_mine:
                tablero[i][j].has_mine=True
                break
    return tablero
    

def jugar(tablero):
    pass

def mostarTablero(tablero):
    #TODO print("MINAS RESTANTES: "+minas_restantes+" | MARCADAS: "+minas_marcadas+" | TIEMPO: "+tiempo)
    print("  ",end='')
    for i in range(len(tablero[0])):
        print(" "+COLS_NAME[i],end='')

    print("\n  "+CES,end='')
    for i in range(len(tablero[1])-1):
        print(COE+COES,end='')
    print(COE+CSO)

    for i in range(len(tablero)):
        print(ROWS_NAME[i],end='')
        if i%2==0:
            print(" ",end='')
        for _ in range(5):
            print(CNS+" ",end='') #TODO Sustituir por el numero de minas
        print(CNS)
        if i<len(tablero)-1:
            if i%2==0:
                print(" "+CES,end='')
                for _ in range(len(tablero[i])):
                    print(CONE+COES,end='')
                print(CON)
            else:
                print(" "+CNE,end='')
                for _ in range(len(tablero[i])):
                    print(COES+CONE,end='')
                print(CSO)
    if len(tablero)%2!=0:
        print(" ",end='')
    print(" "+CNE,end='')
    for i in range(len(tablero[0])-1):
        print(""+COE+CONE,end='')
    print(COE+CON)

class Cell:
    def __init__(self,x,y,mina=False,abierta=False,marcada=False):
        self.is_open=abierta
        self.is_checked=marcada
        self.has_mine=mina
        self.x=x
        self.y=y

    def set_num_minas(self,tablero):
        self.num_minas=1
        pass
    
    def open_cell(self,tablero):
        if self.is_open or self.is_checked:
            raise Exception("Operacion invalida")

        if self.has_mine:
            #TODO explode()
            pass
        else:
            self.is_open=True
            self.set_num_minas(tablero)
            if self.num_minas<=0:
                #TODO abrir las celdas cercanas
                pass
    def __str__(self):
        return str(self.x)+' '+str(self.y)
