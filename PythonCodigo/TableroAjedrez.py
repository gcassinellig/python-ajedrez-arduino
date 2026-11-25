#Borramos las variables de las sesiones anteriores
globals().clear();

#Importamos las librerias y funciones a utilizar
import numpy as numpy
import serial, time
from hallarPosicion import hallarPosicion
from hallarPosicion import moverPieza
from hallarPosicion import moverPieza2
from hallarPosicion import PosicionRandom



#nota: formato de los arrays: posicionY, posicionX
#Creamos los rangos en los que se puede mover el caballo
rangocaballo = [
    [-2,-1],[-1,-2],[1,-2],[2,-1],[2,1],[1,2],[-1,2],[-2,1]
];
#Creamos los rangos en los que se puede mover el rey
rangorey = [
    [-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]
];
#Creamos los rangos en los que se puede mover el alfil y la dama
#Diagonal (arriba, izquierda)
rangoDUL = [
    [-1,-1],[-2,-2],[-3,-3],[-4,-4],[-5,-5],[-6,-6],[-7,-7]
];
#Diagonal (arriba, derecha)
rangoDUR = [
    [-1,1],[-2,2],[-3,3],[-4,4],[-5,5],[-6,6],[-7,7]
];
#Diagonal (abajo, izquierda)
rangoDDL = [
    [1,-1],[2,-2],[3,-3],[4,-4],[5,-5],[6,-6],[7,-7]
];
#Diagonal (abajo, derecha)
rangoDDR = [
    [1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7]
];
#Creamos los rangos en los que se puede mover la torre y la dama
#Arriba
rangoU = [
    [-1,0],[-2,0],[-3,0],[-4,0],[-5,0],[-6,0],[-7,0]
];
#Izquierda
rangoL = [
    [0,-1],[0,-2],[0,-3],[0,-4],[0,-5],[0,-6],[0,-7]
];
#Abajo
rangoD = [
    [1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[7,0]
];
#Derecha
rangoR = [
    [0,1],[0,2],[0,3],[0,4],[0,5],[0,6],[0,7]
];
#Creamos los rangos normales del peón
rangopeonmovB = [
    [-1,0],[-2,0]
];
rangopeonmovN = [
    [1,0],[2,0]
];
#Creamos los rangos de ataque del peón
rangopeonataqueB = [
    [-1,-1],[-1,1]
];
rangopeonataqueN = [
    [1,-1],[1,1]
];

#Establecemos los valores de cada pieza para poder distinguirlas
peon = 1;
caballo = 3;
alfil = 4;
torre = 5;
dama = 10;
rey = 20;
#creamos el tablero
tableroarray = numpy.zeros((8,8),dtype=int);

#Ordenamos el tablero. El lado de arriba es negro y el de abajo es blanco
#Colocamos los peones
tableroarray[6,range(0,8)] = peon;
tableroarray[1,range(0,8)] = peon * -1;

#Colocamos los caballos
tableroarray[7,(1,6)] = caballo;
tableroarray[0,(1,6)] = caballo * -1;

#Colocamos los alfiles
tableroarray[7,(2,5)] = alfil;
tableroarray[0,(2,5)] = alfil * -1;

#Colocamos las torres
tableroarray[7,(0,7)] = torre;
tableroarray[0,(0,7)] = torre * -1;

#Colocamos las damas
tableroarray[7,3] = dama;
tableroarray[0,3] = dama * -1;

#Finalmente, colocamos los reyes
tableroarray[7,4] = rey;
tableroarray[0,4] = rey * -1;

#Creamos variables relacionadas a la partida
juegoactivo = 1;
capturablanco = 0;
capturanegro = 0;
j1_equipo = 0;   #1: blanco, 2, negro
j2_equipo = 0;
j1_control = 0;     #1: humano, 2: IA
j2_control = 0;
jugadoractual = 1;
startMarker = '<'
endMarker = '>'
dataStarted = False
dataBuf = ""
messageComplete = False

def recvLikeArduino():
    global startMarker, endMarker, dataStarted, dataBuf, messageComplete

    if arduino.inWaiting() > 0 and messageComplete == False:
        x = arduino.read().decode() # decode needed for Python3
        
        if dataStarted == True:
            if x != endMarker:
                dataBuf = dataBuf + x
            else:
                dataStarted = False
                messageComplete = True
        elif x == startMarker:
            dataBuf = ''
            dataStarted = True
    
    if (messageComplete == True):
        messageComplete = False
        return dataBuf
    else:
        return "XXX"

print("|          AJEDREZ           |")
print("Programado por el grupo Blanco")
print("------------------------------")

equipovalido = 0;
while equipovalido == 0:
    print("Elija que equipo representará")
    j1_equipo = int(input("Blanco (1) o negro (2): "))
    if (j1_equipo < 1) | (j1_equipo > 2):
        print("Error: El número de opción no es valido")
    else:
        if j1_equipo == 1:
            j2_equipo = 2;
        else:
            j2_equipo = 1;
            jugadoractual = 2;
        equipovalido = 1;

controlvalidado = 0;
while controlvalidado == 0:
        print("Elija quien controlará al jugador 1:")
        j1_control = int(input("Humano (1) o I.A. (2): "))
        if (j1_control < 1) | (j1_control > 2):
            print("Error: El número de opción no es valido")
        else:
            print("Elija quien controlará al jugador 2:")
            j2_control = int(input("Humano (1) o I.A. (2): "))
            if (j2_control < 1) | (j2_control > 2):
                print("Error: El número de opción no es valido")
            else:
                controlvalidado = 1;

usarbrazo = 0;
while usarbrazo == 0:
    print("¿Desea que el brazo robot imite las jugadas?")
    usarbrazo = int(input("Si (1) o No (2): "))
    if (usarbrazo < 1) | (usarbrazo > 2):
        print("Error: El número de opción no es valido")

while juegoactivo == 1:
    #Mostramos el tablero en pantalla
    if ((j1_control == 1) & (jugadoractual == 1)) | ((j2_control == 1) & (jugadoractual == 2)):
        print("\n\n\n\n\n¡Presione Ctrl + C para finalizar el juego!")
        print("\nPiezas blancas capturadas = ",capturablanco);
        print("Piezas negras capturadas = ",capturanegro);
        if (jugadoractual == 1):
            print("\nEs el turno del equipo blanco");
        else:
            print("\nEs el turno del equipo negro");
        print(tableroarray);
    #Comprobamos que los códigos ingresados sean validos
    codigosvalidos = 0;
    while codigosvalidos == 0:
        # si el jugador es humano
        if ((j1_control == 1) & (jugadoractual == 1)) | ((j2_control == 1) & (jugadoractual == 2)):
            selec1 = input("\nIngresar el código del cuadro que desea seleccionar:");
            posinicial = hallarPosicion(selec1);
            selec2 = input("\nIngresar el código del cuadro donde se colocará la pieza:");
            posfinal = hallarPosicion(selec2);
            if (posinicial[0,0] == 8) | (posfinal[0,0] == 8):
                print("\nError: Uno de los códigos ingresados es incorrecto. Por favor ingresarlos de nuevo.");
            else:
                codigosvalidos = 1;
        # si el jugador es una IA
        else:
            print("\nPensando...");
            selec1 = PosicionRandom();
            posinicial = hallarPosicion(selec1);
            selec2 = PosicionRandom();
            posfinal = hallarPosicion(selec2);
            codigosvalidos = 1;
            
    #Obtenemos las piezas dentro de los cuadros
    piezainicial = tableroarray[posinicial[0,0],posinicial[0,1]];
    piezafinal = tableroarray[posfinal[0,0],posfinal[0,1]];
    piezaatrapada = 0;
    #Procedemos a validar las reglas basicas de ajedrez
    if ((j1_control == 1) & (jugadoractual == 1)) | ((j2_control == 1) & (jugadoractual == 2)):
        print("\nValidando la jugada:");
    if ((piezainicial < 0) & (jugadoractual == 1)) | ((piezainicial > 0) & (jugadoractual == 2)):
        if ((j1_control == 1) & (jugadoractual == 1)) | ((j2_control == 1) & (jugadoractual == 2)):
            print("\nError: La pieza inicial no puede ser del equipo opuesto");
    elif numpy.array_equiv(posinicial, posfinal) == True:
        if ((j1_control == 1) & (jugadoractual == 1)) | ((j2_control == 1) & (jugadoractual == 2)):
            print("\nError: No se está moviendo la pieza a ninguna parte");
    elif piezainicial == 0:
        if ((j1_control == 1) & (jugadoractual == 1)) | ((j2_control == 1) & (jugadoractual == 2)):
            print("\nError: No se está moviendo ninguna pieza");
    elif ((piezainicial > 0) & (piezafinal > 0)) | ((piezainicial < 0) & (piezafinal < 0)):
        if ((j1_control == 1) & (jugadoractual == 1)) | ((j2_control == 1) & (jugadoractual == 2)):
            print("\nError: No se puede ocupar una pieza del mismo equipo");
    #Comprobamos si el rey está en riesgo
    #Una vez validamos los aspectos básicos, procedemos a validar el movimiento
    #de las piezas
    else:
        #peón (blanco)
        if piezainicial == 1:
            #Primero vemos si el peón está atacando una pieza enemiga
            distancia = posfinal - posinicial;
            cont = 0;
            promocion = 0;
            while cont < len(rangopeonataqueB):
                if numpy.array_equiv(rangopeonataqueB[cont], distancia) == True:
                    temppieza = tableroarray[posfinal[0,0],posfinal[0,1]];
                    if temppieza < 0:
                        tableroarray[posfinal[0,0],posfinal[0,1]] = piezainicial;
                        tableroarray[posinicial[0,0],posinicial[0,1]] = 0;
                        capturanegro = capturanegro + 1;
                        piezaatrapada = 1;
                        if posfinal[0,0] == 0:
                            promocion = 1;
                        #pasar el turno al otro equipo
                        jugadoractual = 2;
                else:
                    cont = cont + 1;
            #Si no está atacando, entonces vemos si se está moviendo
            if cont == len(rangopeonataqueB):
                #Establecer el rango del peón
                limiterango = 1;
                if posinicial[0,0] == 6:
                    limiterango = 2;    #Cambiar a 2 si está en la posición inicial
                cont = 0;
                while cont < limiterango:
                    temppos = posinicial + rangopeonmovB[cont];
                    temppieza = tableroarray[temppos[0,0],temppos[0,1]];
                    if (numpy.array_equiv(temppos, posfinal) == False) & (temppieza != 0):
                        print("\nError: El camino del peón se encuentra bloqueado.");
                        break;
                    elif (numpy.array_equiv(temppos, posfinal) == True) & (temppieza == 0):
                        tableroarray[posfinal[0,0],posfinal[0,1]] = piezainicial;
                        tableroarray[posinicial[0,0],posinicial[0,1]] = 0;
                        if posfinal[0,0] == 0:
                            promocion = 1;
                        #pasar el turno al otro equipo
                        jugadoractual = 2;
                        break;
                    else:
                        cont = cont + 1;
                if cont == limiterango:
                    print("\nError: Ese movimiento se encuentra fuera de rango");
            #Si el peón alcanza la octava fila, promoverlo
            while promocion == 1:
                print("\nTu peón será promovido. Elegir la pieza en la que se va a convertir:");
                selecpeon = int(input("Caballo (3), Alfil (4), Torre (5) o Dama (10): "));
                if (selecpeon == 3) | (selecpeon == 4) | (selecpeon == 5) | (selecpeon == 10):
                    tableroarray[posfinal[0,0],posfinal[0,1]] = selecpeon;
                    promocion = 2;
                else:
                    print("\nError: El código ingresado es incorrecto. Por favor ingresarlo de nuevo.");
        #caballo (blanco)
        elif piezainicial == 3:
            moverPieza (rangocaballo, posinicial, posfinal, tableroarray, piezainicial, piezafinal, capturanegro, capturablanco, jugadoractual)
        #alfil (blanco)
        elif piezainicial == 4:
            #Obtenemos la distancia entre las dos posiciones
            distancia = posfinal - posinicial;
            stringerror = "\nError: El camino del alfil está bloqueado";
            cont = 0;
            while cont < len(rangoDUL):
                if numpy.array_equiv(rangoDUL[cont], distancia) == True:
                    moverPieza2 (rangoDUL, posinicial, posfinal, tableroarray, piezainicial, piezafinal, capturanegro, capturablanco, stringerror, jugadoractual, piezaatrapada);
                    break;
                else:
                    cont = cont + 1;
            if cont == len(rangoDUL):
                cont = 0;
                while cont < len(rangoDUR):
                    if numpy.array_equiv(rangoDUR[cont], distancia) == True:
                        moverPieza2 (rangoDUR, posinicial, posfinal, tableroarray, piezainicial, piezafinal, capturanegro, capturablanco, stringerror, jugadoractual, piezaatrapada);
                        break;
                    else:
                        cont = cont + 1;
                if cont == len(rangoDUR):
                    cont = 0;
                    while cont < len(rangoDDL):
                        if numpy.array_equiv(rangoDDL[cont], distancia) == True:
                            moverPieza2 (rangoDDL, posinicial, posfinal, tableroarray, piezainicial, piezafinal, capturanegro, capturablanco, stringerror, jugadoractual, piezaatrapada);
                            break;
                        else:
                            cont = cont + 1;
                    if cont == len(rangoDDL):
                        cont = 0;
                        while cont < len(rangoDDR):
                            if numpy.array_equiv(rangoDDR[cont], distancia) == True:
                                moverPieza2 (rangoDDR, posinicial, posfinal, tableroarray, piezainicial, piezafinal, capturanegro, capturablanco, stringerror, jugadoractual, piezaatrapada);
                                break;
                            else:
                                cont = cont + 1;
                        if cont == len(rangoDDR):
                            print("\nError: Ese movimiento se encuentra fuera de rango");
        #torre (blanco)
        elif piezainicial == 5:
            #Obtenemos la distancia entre las dos posiciones
            distancia = posfinal - posinicial;
            stringerror = "\nError: El camino de la torre está bloqueado";
            cont = 0;
            while cont < len(rangoU):
                if numpy.array_equiv(rangoU[cont], distancia) == True:
                    moverPieza2 (rangoU, posinicial, posfinal, tableroarray, piezainicial, piezafinal, capturanegro, capturablanco, stringerror, jugadoractual, piezaatrapada);
                    break;
                else:
                    cont = cont + 1;
            if cont == len(rangoU):
                cont = 0;
                while cont < len(rangoL):
                    if numpy.array_equiv(rangoL[cont], distancia) == True:
                        moverPieza2 (rangoL, posinicial, posfinal, tableroarray, piezainicial, piezafinal, capturanegro, capturablanco, stringerror, jugadoractual, piezaatrapada);
                        break;
                    else:
                        cont = cont + 1;
                if cont == len(rangoL):
                    cont = 0;
                    while cont < len(rangoD):
                        if numpy.array_equiv(rangoD[cont], distancia) == True:
                            moverPieza2 (rangoD, posinicial, posfinal, tableroarray, piezainicial, piezafinal, capturanegro, capturablanco, stringerror, jugadoractual, piezaatrapada);
                            break;
                        else:
                            cont = cont + 1;
                    if cont == len(rangoD):
                        cont = 0;
                        while cont < len(rangoR):
                            if numpy.array_equiv(rangoR[cont], distancia) == True:
                                moverPieza2 (rangoR, posinicial, posfinal, tableroarray, piezainicial, piezafinal, capturanegro, capturablanco, stringerror, jugadoractual, piezaatrapada);
                                break;
                            else:
                                cont = cont + 1;
                        if cont == len(rangoR):
                            print("\nError: Ese movimiento se encuentra fuera de rango");
        #dama (blanco)
        elif piezainicial == 10:
            #Obtenemos la distancia entre las dos posiciones
            distancia = posfinal - posinicial;
            stringerror = "\nError: El camino de la dama está bloqueado";
            cont = 0;
            while cont < len(rangoDUL):
                if numpy.array_equiv(rangoDUL[cont], distancia) == True:
                    moverPieza2 (rangoDUL, posinicial, posfinal, tableroarray, piezainicial, piezafinal, capturanegro, capturablanco, stringerror, jugadoractual, piezaatrapada);
                    break;
                else:
                    cont = cont + 1;
            if cont == len(rangoDUL):
                cont = 0;
                while cont < len(rangoU):
                    if numpy.array_equiv(rangoU[cont], distancia) == True:
                        moverPieza2 (rangoU, posinicial, posfinal, tableroarray, piezainicial, piezafinal, capturanegro, capturablanco, stringerror, jugadoractual, piezaatrapada);
                        break;
                    else:
                        cont = cont + 1;
                if cont == len(rangoU):
                    cont = 0;
                    while cont < len(rangoDUR):
                        if numpy.array_equiv(rangoDUR[cont], distancia) == True:
                            moverPieza2 (rangoDUR, posinicial, posfinal, tableroarray, piezainicial, piezafinal, capturanegro, capturablanco, stringerror, jugadoractual, piezaatrapada);
                            break;
                        else:
                            cont = cont + 1;
                    if cont == len(rangoDUR):
                        cont = 0;
                        while cont < len(rangoR):
                            if numpy.array_equiv(rangoR[cont], distancia) == True:
                                moverPieza2 (rangoR, posinicial, posfinal, tableroarray, piezainicial, piezafinal, capturanegro, capturablanco, stringerror, jugadoractual, piezaatrapada);
                                break;
                            else:
                                cont = cont + 1;
                        if cont == len(rangoR):
                            cont = 0;
                            while cont < len(rangoDDR):
                                if numpy.array_equiv(rangoDDR[cont], distancia) == True:
                                    moverPieza2 (rangoDDR, posinicial, posfinal, tableroarray, piezainicial, piezafinal, capturanegro, capturablanco, stringerror, jugadoractual, piezaatrapada);
                                    break;
                                else:
                                    cont = cont + 1;
                            if cont == len(rangoDDR):
                                cont = 0;
                                while cont < len(rangoD):
                                    if numpy.array_equiv(rangoD[cont], distancia) == True:
                                        moverPieza2 (rangoD, posinicial, posfinal, tableroarray, piezainicial, piezafinal, capturanegro, capturablanco, stringerror, jugadoractual, piezaatrapada);
                                        break;
                                    else:
                                        cont = cont + 1;
                                if cont == len(rangoD):
                                    cont = 0;
                                    while cont < len(rangoDDL):
                                        if numpy.array_equiv(rangoDDL[cont], distancia) == True:
                                            moverPieza2 (rangoDDL, posinicial, posfinal, tableroarray, piezainicial, piezafinal, capturanegro, capturablanco, stringerror, jugadoractual, piezaatrapada);
                                            break;
                                        else:
                                            cont = cont + 1;
                                    if cont == len(rangoDDL):
                                        cont = 0;
                                        while cont < len(rangoL):
                                            if numpy.array_equiv(rangoL[cont], distancia) == True:
                                                moverPieza2 (rangoL, posinicial, posfinal, tableroarray, piezainicial, piezafinal, capturanegro, capturablanco, stringerror, jugadoractual, piezaatrapada);
                                                break;
                                            else:
                                                cont = cont + 1;
                                        if cont == len(rangoL):
                                            print("\nError: Ese movimiento se encuentra fuera de rango");
        #rey (blanco)
        elif piezainicial == 20:
            moverPieza (rangorey, posinicial, posfinal, tableroarray, piezainicial, piezafinal, capturanegro, capturablanco, jugadoractual)
        #peón (negro)
        elif piezainicial == -1:
            #Primero vemos si el peón está atacando una pieza enemiga
            distancia = posfinal - posinicial;
            cont = 0;
            promocion = 0;
            while cont < len(rangopeonataqueN):
                if numpy.array_equiv(rangopeonataqueN[cont], distancia) == True:
                    temppieza = tableroarray[posfinal[0,0],posfinal[0,1]];
                    if temppieza > 0:
                        tableroarray[posfinal[0,0],posfinal[0,1]] = piezainicial;
                        tableroarray[posinicial[0,0],posinicial[0,1]] = 0;
                        capturablanco = capturablanco + 1;
                        piezaatrapada = 1;
                        if posfinal[0,0] == 7:
                            promocion = 1;
                        #pasar el turno al otro equipo
                        jugadoractual = 1;
                        break;
                else:
                    cont = cont + 1;
            #Si no está atacando, entonces vemos si se está moviendo
            if cont == len(rangopeonataqueN):
                #Establecer el rango del peón
                limiterango = 1;
                if posinicial[0,0] == 1:
                    limiterango = 2;    #Cambiar a 2 si está en la posición inicial
                cont = 0;
                while cont < limiterango:
                    temppos = posinicial + rangopeonmovN[cont];
                    temppieza = tableroarray[temppos[0,0],temppos[0,1]];
                    if (numpy.array_equiv(temppos, posfinal) == False) & (temppieza != 0):
                        print("\nError: El camino del peón se encuentra bloqueado.");
                        break;
                    elif (numpy.array_equiv(temppos, posfinal) == True) & (temppieza == 0):
                        tableroarray[posfinal[0,0],posfinal[0,1]] = piezainicial;
                        tableroarray[posinicial[0,0],posinicial[0,1]] = 0;
                        if posfinal[0,0] == 7:
                            promocion = 1;
                        #pasar el turno al otro equipo
                        jugadoractual = 1;
                        break;
                    else:
                        cont = cont + 1;
                if cont == limiterango:
                    print("\nError: Ese movimiento se encuentra fuera de rango");
            #Si el peón alcanza la octava fila, promoverlo
            while promocion == 1:
                print("\nTu peón será promovido. Elegir la pieza en la que se va a convertir:");
                selecpeon = int(input("Caballo (3), Alfil (4), Torre (5) o Dama (10): "));
                if (selecpeon == 3) | (selecpeon == 4) | (selecpeon == 5) | (selecpeon == 10):
                    tableroarray[posfinal[0,0],posfinal[0,1]] = selecpeon * -1;
                    promocion = 2;
                else:
                    print("\nError: El código ingresado es incorrecto. Por favor ingresarlo de nuevo.");
        #caballo (negro)
        elif piezainicial == -3:
            moverPieza (rangocaballo, posinicial, posfinal, tableroarray, piezainicial, piezafinal, capturanegro, capturablanco, jugadoractual, piezaatrapada);
        #alfil (negro)
        elif piezainicial == -4:
            #Obtenemos la distancia entre las dos posiciones
            distancia = posfinal - posinicial;
            stringerror = "\nError: El camino del alfil está bloqueado";
            cont = 0;
            while cont < len(rangoDUL):
                if numpy.array_equiv(rangoDUL[cont], distancia) == True:
                    moverPieza2 (rangoDUL, posinicial, posfinal, tableroarray, piezainicial, piezafinal, capturanegro, capturablanco, stringerror, jugadoractual, piezaatrapada);
                    break;
                else:
                    cont = cont + 1;
            if cont == len(rangoDUL):
                cont = 0;
                while cont < len(rangoDUR):
                    if numpy.array_equiv(rangoDUR[cont], distancia) == True:
                        moverPieza2 (rangoDUR, posinicial, posfinal, tableroarray, piezainicial, piezafinal, capturanegro, capturablanco, stringerror, jugadoractual, piezaatrapada);
                        break;
                    else:
                        cont = cont + 1;
                if cont == len(rangoDUR):
                    cont = 0;
                    while cont < len(rangoDDL):
                        if numpy.array_equiv(rangoDDL[cont], distancia) == True:
                            moverPieza2 (rangoDDL, posinicial, posfinal, tableroarray, piezainicial, piezafinal, capturanegro, capturablanco, stringerror, jugadoractual, piezaatrapada);
                            break;
                        else:
                            cont = cont + 1;
                    if cont == len(rangoDDL):
                        cont = 0;
                        while cont < len(rangoDDR):
                            if numpy.array_equiv(rangoDDR[cont], distancia) == True:
                                moverPieza2 (rangoDDR, posinicial, posfinal, tableroarray, piezainicial, piezafinal, capturanegro, capturablanco, stringerror, jugadoractual, piezaatrapada);
                                break;
                            else:
                                cont = cont + 1;
                        if cont == len(rangoDDR):
                            print("\nError: Ese movimiento se encuentra fuera de rango");
        #torre (negro)
        elif piezainicial == -5:
            #Obtenemos la distancia entre las dos posiciones
            distancia = posfinal - posinicial;
            stringerror = "\nError: El camino de la torre está bloqueado";
            cont = 0;
            while cont < len(rangoU):
                if numpy.array_equiv(rangoU[cont], distancia) == True:
                    moverPieza2 (rangoU, posinicial, posfinal, tableroarray, piezainicial, piezafinal, capturanegro, capturablanco, stringerror, jugadoractual, piezaatrapada);
                    break;
                else:
                    cont = cont + 1;
            if cont == len(rangoU):
                cont = 0;
                while cont < len(rangoL):
                    if numpy.array_equiv(rangoL[cont], distancia) == True:
                        moverPieza2 (rangoL, posinicial, posfinal, tableroarray, piezainicial, piezafinal, capturanegro, capturablanco, stringerror, jugadoractual, piezaatrapada);
                        break;
                    else:
                        cont = cont + 1;
                if cont == len(rangoL):
                    cont = 0;
                    while cont < len(rangoD):
                        if numpy.array_equiv(rangoD[cont], distancia) == True:
                            moverPieza2 (rangoD, posinicial, posfinal, tableroarray, piezainicial, piezafinal, capturanegro, capturablanco, stringerror, jugadoractual, piezaatrapada);
                            break;
                        else:
                            cont = cont + 1;
                    if cont == len(rangoD):
                        cont = 0;
                        while cont < len(rangoR):
                            if numpy.array_equiv(rangoR[cont], distancia) == True:
                                moverPieza2 (rangoR, posinicial, posfinal, tableroarray, piezainicial, piezafinal, capturanegro, capturablanco, stringerror, jugadoractual, piezaatrapada);
                                break;
                            else:
                                cont = cont + 1;
                        if cont == len(rangoR):
                            print("\nError: Ese movimiento se encuentra fuera de rango");
        #dama (negro)
        elif piezainicial == -10:
            #Obtenemos la distancia entre las dos posiciones
            distancia = posfinal - posinicial;
            stringerror = "\nError: El camino de la dama está bloqueado";
            cont = 0;
            while cont < len(rangoDUL):
                if numpy.array_equiv(rangoDUL[cont], distancia) == True:
                    moverPieza2 (rangoDUL, posinicial, posfinal, tableroarray, piezainicial, piezafinal, capturanegro, capturablanco, stringerror, jugadoractual, piezaatrapada);
                    break;
                else:
                    cont = cont + 1;
            if cont == len(rangoDUL):
                cont = 0;
                while cont < len(rangoU):
                    if numpy.array_equiv(rangoU[cont], distancia) == True:
                        moverPieza2 (rangoU, posinicial, posfinal, tableroarray, piezainicial, piezafinal, capturanegro, capturablanco, stringerror, jugadoractual, piezaatrapada);
                        break;
                    else:
                        cont = cont + 1;
                if cont == len(rangoU):
                    cont = 0;
                    while cont < len(rangoDUR):
                        if numpy.array_equiv(rangoDUR[cont], distancia) == True:
                            moverPieza2 (rangoDUR, posinicial, posfinal, tableroarray, piezainicial, piezafinal, capturanegro, capturablanco, stringerror, jugadoractual, piezaatrapada);
                            break;
                        else:
                            cont = cont + 1;
                    if cont == len(rangoDUR):
                        cont = 0;
                        while cont < len(rangoR):
                            if numpy.array_equiv(rangoR[cont], distancia) == True:
                                moverPieza2 (rangoR, posinicial, posfinal, tableroarray, piezainicial, piezafinal, capturanegro, capturablanco, stringerror, jugadoractual, piezaatrapada);
                                break;
                            else:
                                cont = cont + 1;
                        if cont == len(rangoR):
                            cont = 0;
                            while cont < len(rangoDDR):
                                if numpy.array_equiv(rangoDDR[cont], distancia) == True:
                                    moverPieza2 (rangoDDR, posinicial, posfinal, tableroarray, piezainicial, piezafinal, capturanegro, capturablanco, stringerror, jugadoractual, piezaatrapada);
                                    break;
                                else:
                                    cont = cont + 1;
                            if cont == len(rangoDDR):
                                cont = 0;
                                while cont < len(rangoD):
                                    if numpy.array_equiv(rangoD[cont], distancia) == True:
                                        moverPieza2 (rangoD, posinicial, posfinal, tableroarray, piezainicial, piezafinal, capturanegro, capturablanco, stringerror, jugadoractual, piezaatrapada);
                                        break;
                                    else:
                                        cont = cont + 1;
                                if cont == len(rangoD):
                                    cont = 0;
                                    while cont < len(rangoDDL):
                                        if numpy.array_equiv(rangoDDL[cont], distancia) == True:
                                            moverPieza2 (rangoDDL, posinicial, posfinal, tableroarray, piezainicial, piezafinal, capturanegro, capturablanco, stringerror, jugadoractual, piezaatrapada);
                                            break;
                                        else:
                                            cont = cont + 1;
                                    if cont == len(rangoDDL):
                                        cont = 0;
                                        while cont < len(rangoL):
                                            if numpy.array_equiv(rangoL[cont], distancia) == True:
                                                moverPieza2 (rangoL, posinicial, posfinal, tableroarray, piezainicial, piezafinal, capturanegro, capturablanco, stringerror, jugadoractual, piezaatrapada);
                                                break;
                                            else:
                                                cont = cont + 1;
                                        if cont == len(rangoL):
                                            print("\nError: Ese movimiento se encuentra fuera de rango");
        #rey (negro)
        elif piezainicial == -20:
            moverPieza (rangorey, posinicial, posfinal, tableroarray, piezainicial, piezafinal, capturanegro, capturablanco, jugadoractual)
    #si se va a usar el brazo
    if (usarbrazo == 1):
        #iniciamos la conexion con Arduino
        puertocom = 'COM7'
        selec1 = '<'+ selec1 + '>'
        selec2 = '<' + selec2 + '>'
        arduino = serial.Serial(port=puertocom,baudrate=115200,timeout=0,rtscts=True);
        time.sleep(2);
        print("Intentando conectar con Arduino...")
        #Intentamos hallar una linea especifica en el Arduino
        msg = ""
        while msg.find("Arduino reportandose") == -1:
            msg = recvLikeArduino()
            if not (msg == 'XXX'): 
                print(msg)
        
        #si se atrapó una pieza
        if (piezaatrapada == 1):
            #deshacerse de la pieza a eliminar (arreglar esta parte)
            arduino.write(selec1.encode());
            arduino.write("<FF>".encode());
            time.sleep(10);
            arduino.close();
            arduino = serial.Serial(port=puertocom,baudrate=115200,timeout=0,rtscts=True);
            time.sleep(2);
            print("Intentando conectar de nuevo con Arduino...")
            #Intentamos hallar una linea especifica en el Arduino
            msg = ""
            while msg.find("Arduino reportandose") == -1:
                msg = recvLikeArduino()
                if not (msg == 'XXX'): 
                    print(msg)
            arduino.write(selec1.encode('utf-8'));
            arduino.write(selec2.encode('utf-8'));
            time.sleep(10);
            arduino.close();
        else:
            arduino.write(selec1.encode('utf-8'));
            arduino.write(selec2.encode('utf-8'));
            time.sleep(10);
            arduino.close();
