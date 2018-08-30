# -*- coding: UTF-8 -*-

from __future__ import print_function
from random import randint
import time

COLS_NAME="abcdefghijklmnopqrstuvwxyz=+-:"
ROWS_NAME="ABCDEFGHIJKLMNOPQRSTUVWXYZ@#$%"
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

def menuInicial(): 
    #Este metodo imprime en pantalla un "menu de inicio" y devuelve la variable eleccion que luego el modulo principal usara para dirigir el flujo del prograna. 
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
        linea=f.readline()
        if int(linea[0])>30 or int(linea[2])>30:
            raise Exception("Error en el fichero, tablero demasiado grande")
        for linea in f:
            tablero.append(list())
            j=0
            for c in linea.strip('\n'):
                if c=='.':
                    tablero[i].append(Cell(j,i))
                elif c=='*':
                    tablero[i].append(Cell(j,i,True))
                else:
                    raise Exception("Error en el fichero")
                j+=1
            i+=1
        return tablero

def generarTablero(tamano,minas):
    tablero=list()
    for i in range(tamano[0]):
        tablero.append(list())
        for j in range(tamano[1]):
            tablero[i].append(Cell(j,i))
    for _ in range(minas):
        i=randint(0,tamano[0]-1)
        j=randint(0,tamano[1]-1)
        while tablero[i][j].has_mine:
            i=randint(0,tamano[0]-1)
            j=randint(0,tamano[1]-1)
        tablero[i][j].has_mine=True
    return tablero
    
def jugar(tablero):
    first_move=True
    explosion,win=False,False
    total_minas=contarMinas(tablero)
    minas_marcadas=0
    start=time.time()
    while not explosion and not win:
        mostrarTablero(tablero,total_minas,minas_marcadas,time.time()-start)
        jugada=list(raw_input("Introduzca su jugada: _"))
        while len(jugada)!=0:
            setAllNumMinas(tablero)
            if len(jugada)<3:
                print("ENTRADA ERRONEA")
                break
            try:
                pos=(ROWS_NAME.index(jugada.pop(0)),COLS_NAME.index(jugada.pop(0)))
            except ValueError:
                print("ENTRADA ERRONEA")
                break
            accion=jugada.pop(0)
            if pos[0]>=len(tablero) or pos[1]>=len(tablero[0]) or (accion!='!' and accion!='*'):
                print("ENTRADA ERRONEA")
                break
            if accion=='!':
                if tablero[pos[0]][pos[1]].is_open:
                    print("NO SE PUEDE MARCAR UNA CELDA ABIERTA")
                    break
                if minas_marcadas==total_minas and not tablero[pos[0]][pos[1]].is_checked:
                    print("NO SE PUEDEN MARCAR MAS CELDAS QUE MINAS")
                    break
                if tablero[pos[0]][pos[1]].is_checked:
                    minas_marcadas-=1
                else:
                    minas_marcadas+=1
                tablero[pos[0]][pos[1]].is_checked=not tablero[pos[0]][pos[1]].is_checked
            elif accion=='*':
                if tablero[pos[0]][pos[1]].is_checked:
                    print("NO SE PUEDE ABRIR UNA CELDA MARCADA")
                    break
                else:
                    if tablero[pos[0]][pos[1]].is_open and tablero[pos[0]][pos[1]].num_minas>0:
                        print("CELDA YA ABIERTA. NO SE PUEDEN ABRIR LAS CELDAS VECINAS POR NUMERO INSUFICIENTE DE MARCAS")
                        break
                    else:
                        if tablero[pos[0]][pos[1]].open_cell(tablero)==-1:
                            explosion=True
            if explosion:
                if first_move:
                    explosion=False
                    swapMine(tablero,pos[0],pos[1])
                    if tablero[pos[0]][pos[1]].open_cell(tablero)==-1:
                        #solo se da en el caso de que todas las celdas sean minas
                        explosion=True
                else:
                    break
            if comprobarTablero(tablero):
                win=True
                break
            if accion=='*':
                first_move=False
    openAll(tablero)
    mostrarTablero(tablero,total_minas,minas_marcadas,time.time()-start)
    if win:
        #TODO Mostrar mensaje de victoria
        pass
    else:
        #TODO Mostrar mensaje de explosion
        pass

def swapMine(Tablero,i,j):
#Cambia una mina de una posicion i j a la primera casilla sin mina del tablero
    for row in Tablero:
        for c in row:
            if not c.has_mine:
                c.has_mine=True
                Tablero[i][j].has_mine=False
                return None

def setAllNumMinas(tablero):
    for row in tablero:
        for c in row:
            c.set_num_minas(tablero)

def openAll(tablero):
    for row in tablero:
        for c in row:
            c.is_open=True

def contarMinas(tablero):
    cont=0
    for row in tablero:
        for c in row:
            if c.has_mine:
                cont+=1
    return cont

def comprobarTablero(tablero):
    for row in tablero:
        for c in row:
            if (not c.is_open and not c.has_mine) or (c.has_mine and not c.is_checked):
                return False
    return True

def mostrarTablero(tablero,total_minas,minas_marcadas,tiempo):
    print("MINAS RESTANTES: "+str(total_minas-minas_marcadas)+" | MARCADAS: "+str(minas_marcadas)+" | TIEMPO: "+str(tiempo))
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
        for c in tablero[i]:
            print(CNS,end='')
            if c.is_checked and (not c.is_open or c.has_mine):
                print("X",end='')
            elif not c.is_open and not c.is_checked:
                print(CSOM,end='')
            elif c.is_open and c.is_checked and not c.has_mine:
                print("#",end='')
            elif c.is_open and not c.is_checked and c.has_mine:
                print("*",end='')
            elif c.num_minas<0:
                print("?",end='')
            elif c.num_minas==0:
                print(" ",end='')
            else:
                print(c.num_minas,end='')
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
        self.num_minas=0
        if self.y!=0:
            if tablero[self.y-1][self.x].has_mine:
                self.num_minas+=1
            if tablero[self.y-1][self.x].is_checked:
                self.num_minas-=1
        
        if self.x!=0:
            if tablero[self.y][self.x-1].has_mine:
                self.num_minas+=1
            if tablero[self.y][self.x-1].is_checked:
                self.num_minas-=1

        if self.x!=len(tablero[0])-1:
            if tablero[self.y][self.x+1].has_mine:
                self.num_minas+=1
            if tablero[self.y][self.x+1].is_checked:
                self.num_minas-=1

        if self.y!=len(tablero)-1:
            if tablero[self.y+1][self.x].has_mine:
                self.num_minas+=1
            if tablero[self.y+1][self.x].is_checked:
                self.num_minas-=1

        if self.y%2==0:
            if self.x!=len(tablero[0])-1 and self.y!=0:
                if tablero[self.y-1][self.x+1].has_mine:
                    self.num_minas+=1
                if tablero[self.y-1][self.x+1].is_checked:
                    self.num_minas-=1
            
            if self.y!=len(tablero)-1 and self.x!=len(tablero[0])-1:
                if tablero[self.y+1][self.x+1].has_mine:
                    self.num_minas+=1
                if tablero[self.y+1][self.x+1].is_checked:
                    self.num_minas-=1
        else:
            if self.x!=0 and self.y!=0:
                if tablero[self.y-1][self.x-1].has_mine:
                    self.num_minas+=1
                if tablero[self.y-1][self.x-1].is_checked:
                    self.num_minas-=1

            if self.y!=len(tablero)-1 and self.x!=0:
                if tablero[self.y+1][self.x-1].has_mine:
                    self.num_minas+=1
                if tablero[self.y+1][self.x-1].is_checked:
                    self.num_minas-=1
    
    def open_cell(self,tablero):
        if self.is_checked:
            return 0
        if self.has_mine:
            return -1
        else:
            self.is_open=True
            if self.num_minas<=0:   #abrir recursivamente
                if self.y!=0 and not tablero[self.y-1][self.x].is_open:
                    if tablero[self.y-1][self.x].open_cell(tablero)==-1:
                        return -1
        
                if self.x!=0 and not tablero[self.y][self.x-1].is_open:
                    if tablero[self.y][self.x-1].open_cell(tablero)==-1:
                        return -1

                if self.x!=len(tablero[0])-1 and not tablero[self.y][self.x+1].is_open:
                    if tablero[self.y][self.x+1].open_cell(tablero)==-1:
                        return -1

                if self.y!=len(tablero)-1 and not tablero[self.y+1][self.x].is_open:
                        if tablero[self.y+1][self.x].open_cell(tablero)==-1:
                            return -1
                if self.y%2==0:
                    if self.x!=len(tablero[0])-1 and self.y!=0 and not tablero[self.y-1][self.x+1].is_open:
                        if tablero[self.y-1][self.x+1].open_cell(tablero)==-1:
                            return -1

                    if self.y!=len(tablero)-1 and self.x!=len(tablero[0])-1 and not tablero[self.y+1][self.x+1].is_open:
                        if tablero[self.y+1][self.x+1].open_cell(tablero)==-1:
                            return -1
                else:
                    if self.x!=0 and self.y!=0 and not tablero[self.y-1][self.x-1].is_open:
                        if tablero[self.y-1][self.x-1].open_cell(tablero)==-1:
                            return -1

                    if self.y!=len(tablero)-1 and self.x!=0 and not tablero[self.y+1][self.x-1].is_open:
                        if tablero[self.y+1][self.x-1].open_cell(tablero)==-1:
                            return -1
