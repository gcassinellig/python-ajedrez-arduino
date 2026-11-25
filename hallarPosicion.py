import numpy as numpy
import random

arraycodigos = numpy.array(
    [['8A', '8B', '8C', '8D', '8E', '8F', '8G', '8H'],
     ['7A', '7B', '7C', '7D', '7E', '7F', '7G', '7H'],
     ['6A', '6B', '6C', '6D', '6E', '6F', '6G', '6H'],
     ['5A', '5B', '5C', '5D', '5E', '5F', '5G', '5H'],
     ['4A', '4B', '4C', '4D', '4E', '4F', '4G', '4H'],
     ['3A', '3B', '3C', '3D', '3E', '3F', '3G', '3H'],
     ['2A', '2B', '2C', '2D', '2E', '2F', '2G', '2H'],
     ['1A', '1B', '1C', '1D', '1E', '1F', '1G', '1H']
]);

def hallarPosicion (seleccion):
    posicion = numpy.zeros((1,2),dtype=int);
    while posicion[0,0] < 8:
        if arraycodigos[posicion[0,0],posicion[0,1]] == seleccion:
            break;
        else:
            posicion[0,1] = posicion[0,1] + 1;
            if posicion[0,1] > 7:
                    posicion[0,1] = 0;
                    posicion[0,0] = posicion[0,0] + 1;
    return posicion;

def moverPieza (rango, posinicial, posfinal, tableroarray, piezainicial, piezafinal, capturanegro, capturablanco, jugadoractual, piezaatrapada):
    cont = 0;
    #Comprobamos si la posición final entra en el rango del caballo
    while cont < len(rango):
        #Obtener una posición temporal
        temppos = posinicial + rango[cont];
        #Si son iguales, mover la pieza
        if numpy.array_equiv(temppos, posfinal) == True:
            tableroarray[posfinal[0,0],posfinal[0,1]] = piezainicial;
            tableroarray[posinicial[0,0],posinicial[0,1]] = 0;
            #Si habia una pieza negra o blanca, aumentar el puntaje
            if (piezafinal < 0) & (piezainicial > 1):
                capturanegro = capturanegro + 1;
                piezaatrapada = 1;
            elif (piezafinal > 0) & (piezainicial < 1):
                capturablanco = capturablanco + 1;
                piezaatrapada = 1;
            #pasar el turno al otro equipo
            jugadoractual = jugadoractual + 1;
            if (jugadoractual > 2):
                jugadoractual = 1;
            break;
        else:
            cont = cont + 1;
    if cont == len(rango):
        print("\nError: Ese movimiento se encuentra fuera de rango")

def moverPieza2 (rango, posinicial, posfinal, tableroarray, piezainicial, piezafinal, capturanegro, capturablanco, stringerror, jugadoractual, piezaatrapada):
    cont = 0;
    #Comprobamos si la posición final entra en el rango del caballo
    while cont < len(rango):
        #Obtener una posición y pieza temporal
        temppos = posinicial + rango[cont];
        temppieza = tableroarray[temppos[0,0],temppos[0,1]];
        #Si son iguales y hay una pieza enemiga, mover la pieza
        if piezainicial > 0:
            #Si el camino está bloqueado, mostrar este mensaje
            if (numpy.array_equiv(temppos, posfinal) == False) & (temppieza != 0):
                print(stringerror);
                break;
            elif (numpy.array_equiv(temppos, posfinal) == True) & (temppieza <= 0):
                tableroarray[posfinal[0,0],posfinal[0,1]] = piezainicial;
                tableroarray[posinicial[0,0],posinicial[0,1]] = 0;
                #Si habia una pieza negra, aumentar el puntaje
                if piezafinal < 0:
                    capturanegro = capturanegro + 1;
                    piezaatrapada = 1;
                #pasar el turno al otro equipo
                jugadoractual = 2;
                break;
            else:
                cont = cont + 1;
        elif piezainicial < 0:
            #Si el camino está bloqueado, mostrar este mensaje
            if (numpy.array_equiv(temppos, posfinal) == False) & (temppieza != 0):
                print(stringerror);
                break;
            elif (numpy.array_equiv(temppos, posfinal) == True) & (temppieza >= 0):
                tableroarray[posfinal[0,0],posfinal[0,1]] = piezainicial;
                tableroarray[posinicial[0,0],posinicial[0,1]] = 0;
                #Si habia una pieza blanca, aumentar el puntaje
                if piezafinal > 0:
                    capturablanco = capturablanco + 1;
                    piezaatrapada = 1;
                #pasar el turno al otro equipo
                jugadoractual = 1;
                break;
            else:
                cont = cont + 1;

def PosicionRandom ():
    letra = chr(random.randint(ord('A'), ord('H')));
    numero = random.randint(1,8);
    posicion = str(numero) + str(letra);
    return posicion;