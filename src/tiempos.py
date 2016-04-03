"""
parametros:
    problema
    granularidad
    ultimo
    cantidad_muestras
"""
import random
import sys
import os
import subprocess

import matplotlib.pyplot as plt
import numpy as np
import math

archivo = "data.in"

problema = int(sys.argv[1])
granularidad = int(sys.argv[2])
ultimo = int(sys.argv[3])
cantidad_muestras = int(sys.argv[4])


def generar1(tamanio_muestra):
    f = open(archivo, "w")
    f.write(str(tamanio_muestra))

def generar2(tamanio_muestra):
    f = open(archivo, "w")
    n = tamanio_muestra
    MAXIMO_T = n
    MAXIMA_COORD = n*n
    f.write(str(n) + " " + str(random.randint(1, MAXIMO_T)) + "\n")
    xs = random.sample(range(MAXIMA_COORD), n)
    ys = random.sample(range(MAXIMA_COORD), n)
    xs.sort(reverse = True)
    ys.sort()
    for x, y in zip(xs, ys):
        f.write(str(x) + " " + str(y) + "\n")


def generar3promedio(tamanio_muestra):
    f = open(archivo, "w")
    n = tamanio_muestra
    MAXIMO_T = n
    MAXIMA_COORD = 2 * n
    f.write(str(n) + "\n")
    puntos = []
    for _ in range(n):
        punto = (random.randint(1, MAXIMA_COORD), random.randint(1, MAXIMA_COORD))
        if punto not in puntos:
            puntos.append(punto)
    for x, y in puntos:
        f.write(str(x) + " " + str(y) + "\n")

def generar3mejor(tamanio_muestra):
    f = open(archivo, "w")
    n = tamanio_muestra
    f.write(str(n) + "\n")
    for i in range(n):
        f.write(str(i+1) + " " + str(i+1) + "\n")

def generar3peor(tamanio_muestra):
    f = open(archivo, "w")
    n = tamanio_muestra
    f.write(str(n) + "\n")
    for i in range(n):
        angle = 2 * math.pi * random.random()
        x = (float(n) / 2) *  math.cos(angle) + n
        y = (float(n) / 2) *  math.sin(angle) + n
        f.write(str(int(x)) + " " + str(int(y)) + "\n")

def correr_programa(binario):
    p = subprocess.Popen("cat " + archivo + " | " + binario,
                         shell = True,
                         stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = p.communicate()
    return 1000000 * float(err)

def mean(xs):
    if len(xs) == 0:
        return 0.0
    else:
        suma = 0.0
        for x in xs:
            suma += x
        return suma / len(xs)

def median(xs):
    xs.sort()
    return xs[len(xs) / 2]

binarios = ["", "./problema1", "./problema2", "./problema3"]

def tiempo_normalizado(problema, tiempo, n):
    if problema == 1:
        return tiempo / (n * math.log(n))
    elif problema == 2:
        return tiempo / n
    elif problema == 3:
        return tiempo / n**(n+2)

def encontrar_k(problema, puntos):
    ks = []
    puntos = puntos[1:-6]

    for n, tiempo in puntos:
        ks.append(tiempo_normalizado(problema, tiempo, n))
    return mean(ks)


def main():
    datos = []
    posiciones = []
    for tamanio_muestra in range(0, ultimo, granularidad):
        if tamanio_muestra == 0: tamanio_muestra = 1
        print tamanio_muestra
        posiciones.append(float(tamanio_muestra))
        tiempos = []
        for seed in range(cantidad_muestras):
            mediciones = 2
            mediciones_vector = []
            random.seed(seed)
            if problema == 1:
                generar1(tamanio_muestra)
            elif problema == 2:
                generar2(tamanio_muestra)
            elif problema == 3:
                generar3mejor(tamanio_muestra)
            for medicion in range(mediciones):
                mediciones_vector.append(correr_programa(binarios[problema]))
            tiempos.append(min(mediciones_vector))
        datos.append(tiempos)
    plt.figure()
    puntos = zip(map(float, posiciones), map(median, datos))
    #k = encontrar_k(problema, puntos)
    k = 0.05
    fit = []
    if problema == 1:
        fit = map(lambda n: k * n * math.log(n), posiciones)
    elif problema == 2:
        fit = map(lambda n: k * n, posiciones)
    elif problema == 3:
        #fit = map(lambda n: k * n**(n+2), posiciones
        fit = map(lambda n: k * n * n * n, posiciones)
    print [x[1] for x in puntos]
    print fit

    posiciones_ints = map(int, posiciones)
    plt.plot(posiciones_ints, map(lambda (n, tiempo): tiempo / (n*n*n),
        zip(posiciones_ints, map(median, datos))), label="Algoritmo con poda")
    plt.legend(loc=2)
    plt.xlabel("Tamano de la entrada")
    plt.ylabel("Tiempo (us) / n^3")
    plt.ylim([0, 0.1])
    """
    posiciones_ints = map(int, posiciones)
    plt.plot(posiciones_ints, map(median, datos),
            label="Nuestro algoritmo")
    plt.plot(posiciones_ints, map(lambda x: 1.1 * x, fit),
            label="{0:.2f}".format(k * 1.1)+" n log n", linestyle='--')
    plt.plot(posiciones_ints, map(lambda x: 0.9 * x, fit),
            label="{0:.2f}".format(k * 0.9)+" n log n", linestyle='--')
    #plt.boxplot(datos, positions=posiciones_ints, widths=granularidad/2.0,
    #            showfliers=False)
    plt.legend(loc=2)
    plt.xlabel("Tamano de la entrada")
    plt.ylabel("Tiempo (us)")
    """
    plt.savefig("foo.pdf")


main()
os.remove(archivo)
