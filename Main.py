# -*- coding: UTF-8 -*-

from __future__ import print_function
from Metodos import *

while True:
    eleccion=menuInicial()
    if(eleccion<4):
        if(eleccion==1):
            tamano=(9,9)
            minas=10
        elif(eleccion==2):
            tamano=(16,16)
            minas=40 
        elif(eleccion==3):
            tamano=(16,30)
            minas=99
        tablero=generarTablero(tamano,minas)
    elif(eleccion==4):
        tablero=leerFichero()
    else: 
        exit()
    jugar(tablero)

