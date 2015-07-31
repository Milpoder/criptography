#-*- encoding: utf-8 -*-
#Práctica II Criptografía
#Cifrado de Flujo
#Autor: Pedro Luis Trigueros Mondéjar
#DNI: 53593707-G

from operator import xor #operador xor
import copy #copiar listas
from timeit import time
import binascii #pasar de binario a ascii

#Ejercicio 1. Escribe una función que determine si una secuencia de bits cumple los postulados de Golomb
#([2, §3.5]).

def Postulados_G(li):
    #determinamos si cumple el primer postulado
    primero = False
    if abs(li.count(1) - li.count(0)) <= 1: #Si la diferencia entre ceros y unos es de más de uno Falso
        primero = True
    if primero == False:
        print("No se cumple el primer postulado")
        return False
    #determinamos si se cumple el segundo postulado
    segundo = True
    # A la hora de buscar rachas hacer que el primer y último bit sean diferentes
    veces = 0
    for i in range(0,len(li)-1):
        if li[i] != li[i+1]:
            veces += 1
    if veces > 0: #si es 0 es que sólo hay una racha
        contador = 1
        rachas = []
        rachas1 = []
        for i in range (0,len(li)):
            rachas.append(0)
        
        while li[0] == li[len(li)-1]:
            for i in range(1,len(li)):#bucle que desplaza en una posición los bits
                    li[-i] = li[-i-1]
        for i in range (0,len(li)-1):#bucle que determina las rachas
            if li[i] == li[i+1] and i == (len(li)-2):
                rachas[contador+1] += 1
            if li[i] != li[i+1] and i == (len(li)-2):
                rachas[contador-1] += 1
            if li[i] != li[i+1]:
                rachas[contador] += 1
                contador = 1
            else:
                contador += 1
        
        for i in range(0,len(rachas)):
            if rachas[i] != 0:
                rachas1.append([rachas[i],i])#guardamos las rachas de la forma [(cantidad numeros),numero de racha]
        for i in range(0,len(rachas1)-1):
            a,b = rachas1[i],rachas1[i+1]
            if ((2*b[0] != a[0] and i != len(rachas1)-2)  or a[1]+1 != b[1] or (i == len(rachas1)-2 and b[0] != a[0]) or (2*b[0] != a[0] and i == len(rachas1)-2 and b[0] !=1 )):#comprobamos la condición
                segundo = False
        if segundo ==  False:
            print ("No se cumple el segundo postulado")
            return False
    else:
        print ("No se cumple el segundo postulado")
        #return False 
    #Determinamos si se cumple el tercer postulado
    tercero = True
    li2 = []
    hamming = []
    for i in range (0,len(li)):
        li2.append(li[i])
    for i in range(0,len(li)):
        veces1 = 0
        for i in range(0,len(li)):#bucle que desplaza en una posición los bits
            if i == 0:
                li2[0] = li2[len(li2)-1]
            else:
                li2[i] = li2[i-1]
        for i in range(0,len(li)):#calculamos la nueva distancia de hamming de la nueva lista con la original
            if li[i] != li2[i]:
                veces1 += 1
        hamming.append(veces1)#insertamos la distancia de hamming
    for i in range(0,len(hamming)-2):
        if hamming[i] != hamming[i+1]:#vemos si las distancias de hamming son iguales
            print ("No se cumple el tercer postulado")
            return False
    if primero == True and segundo == True and tercero == True:
        print("cumple los postulados")
        return True

#Ejercicio 2. Implementa registros lineales de desplazamiento con retroalimentación (LFSR, [1, Chapter6]). La entrada son los coeficientes del polinomio
#de conexión, la semilla, y la longitud de la secuencia de salida.
#Ilustra con ejemplos la dependencia del periodo de la semilla en el caso de polinomios reducibles, la independencia en el caso de polinomios irreducibles,
#y la maximalidad del periodo en el caso de polinomios primitivos.
#Comprueba que los ejemplos con polinomios primitivos que satisfacen los postulados de Golomb (en [1,§4.5.3] hay tablas de polinomios primitivos).
#Polinomios: x^3 + x + 1; x^2 + x + 1; x^8 + x^4 + x^3 + x^2 + 1

#introducir polinomios sin el primer término pero con el término independiente ej: x^3 + x + 1 [0,1,1] 
def LFSR(li,s,k):
    lis = s
    assert(len(li)==len(s))
    for i in range(0,k):
        sj = 0 #reinicio del feedback
        for j in range(1,len(li)+1): #para cada coeficiente del polinomio
            a = lis[j+i-1]*li[-j] #se hace un and
            sj = xor(sj,a) #se hace un xor
        lis += [sj]  #añadimos la semilla al final de la cadena
    return lis

#Ejercicio 3. Un polinomio en varias variables con coeficientes en Z2 se puede expresar como suma de monomios, simplemente usando la propiedad distributiva.
#Cualquier monomio x^(e1)...x^(en) n , ei € N, es, como función, equivalente a un monomio de la forma x^(i1)...x(ir) (x^2 = x para todo x € Z2, los ij
#son precisamente los índices tales que ei j != 0). Por ejemplo, 1 + x^2(y + x) = 1 + x^3 + x^2y, es esta expresión es
#equivalente a 1+x+xy, por lo que la representamos mediante [[0,0],[1,0], [1,1]], que se corresponde con la lista de exponentes en las dos variables:
#x^0y^0 + x^1y^0 + x^1y^1. Así un polinomio en Z2 se puede representar por una lista monomios. Y cada monomio como una lista de 0 y 1, que corresponden
#con los exponentes de cada una de las variables que intervienen en el polinomio. Escribe una función que toma como argumentos una
#función polinómica f , una semilla s y un entero positivo k, y devuelve una secuencia de longitud k generada al aplicar a s el registro no lineal de
#desplazamiento con retroalimentación asociado a f . Encuentra el periodo de la NLFSR ( (x ^ y) v z )xor t con semilla 1011.
#El periodo comienza en la posición 10.

#ejemplo de entrada de polinomio x + x*y + y + z + 1 [[0,0,1][0,1,1][0,1,0][1,0,0] [0,0,0]]
def NLFSR(li,s,k):
    assert(len(li[0])==len(s))
    salida = []
    for i in s:#añadimos la semilla al principio de la salida
        salida.append(i)
    for i in range(0,k):
        sj =0 #reinicio del feedback
        for i in li:
            r = 1
            for j,k in zip(i,s):
                if j == 1:
                    r = r * k * j
            sj = xor(sj,r)#cálculo de la xor
        salida.append(sj)
        s = s + [sj] 
        for i in range(0,len(s)-1):#desplazamos los bits
            s[i] = s[i+1]
        s = s[:-1]#eliminamos el último
    return salida

#Ejercicio 4. Implementa el generador de Geffe ([1, 6.50]). Encuentra ejemplos donde el periodo de la salida es p1p2p3, con p1, p2 y p3 los periodos de los
#tres LFSRs usados en el generador de Geffe. Usa este ejercicio para construir un cifrado en flujo. Con entrada un mensaje m, construye una llave k con la
#misma longitud que m, y devuelve m xor k (donde xor significa suma componente a componente en Z2). El descifrado se hace de la misma forma:
#c  xor k (nótese que c xor k = (m xor k)=(m xor k) xor k = m xor (k xor k) = m, ya que x xor x = 0 en Z2).

def Geffe(li,li1,li2,s,s1,s2,k):
    #cálculo de los tres LFSR
    a = LFSR(li,s,k)
    b = LFSR(li1,s1,k)
    c = LFSR(li2,s2,k)
    salida = []
    #cálculo de el generador de Geffe
    for i,j,k in zip(a,b,c):
        x1 = i*j#primero multiplica a segundo
        x2 = j*k#primero multiplica a tercero
        x3 = k #tercero
        f = xor(xor(x1,x2),x3) #cálculo de la xor
        salida.append(f) #añadimos a la lista de salida
    return salida


def ascii_a_bin(char):
	ascii = ord(char)
	bin = []
	while (ascii > 0):
		if (ascii & 1) == 1:
			bin.append("1")
		else:
			bin.append("0")
		ascii = ascii >> 1
	bin.reverse()
	binary = "".join(bin)
	zerofix = (8 - len(binary)) * '0'
	return zerofix + binary

def Cifrado_flujo(m):
    binario = []
    list_bin = []
    for i in m:#convertimos texto a binario(list de string)
        binario.append(ascii_a_bin(i))
    #pasamos de list de string a list de int
    for i in binario:
        for j in i:
            if j == '0':
                list_bin.append(0)
            else:
                list_bin.append(1)
    k = Geffe([1],[1,1],[0,1,1],[0],[0,1],[1,0,1],len(list_bin))#polinomios primivitos que mcd es 1 ya que sería las rachas de la forma (2^n)-1
    salida = []
    for i,j in zip(list_bin,k):
        salida.append(xor(i,j))
    return salida

def Descifrado_flujo(m):
    binario = []
    k = Geffe([1],[1,1],[0,1,1],[0],[0,1],[1,0,1],len(m))#polinomios primivitos que mcd es 1 ya que sería las rachas de la forma (2^n)-1
    for i,j in zip(k,m):
        print(i,j)
        binario.append(xor(i,j))
    binario1 = []
    #pasamos de list de int a list de string
    for i in binario:
            if i == 0:
                binario1.append('0')
            else:
                binario1.append('1')
    s = ""
    for i in range(0,len(binario1)):#lo convertimos de lista a string
        s += binario1[i]

#Ejercicio 5. Dada una sucesión de bits periódica, determina la complejidad lineal de dicha sucesión, y el polinomio de conexión que la genera.
#Para esto, usa el algoritmo de Berlekamp-Massey ([1, Algorithm 6.30]).
#Haz ejemplos con sumas y productos de secuencias para ver qué ocurre con la complejidad lineal.

def Berlekamp_Massey(li):
    #inicializamos dos listas de tamaño li que todos los elementos son cero excepto en la posición 0
    f , g = [],[]
    f.append(1)
    g.append(1)
    z = 0
    k = 0
    while li[z] != 1:
        k+=1
        z+=1
    for i in range(1,k-1):
        f.append(0)
        g.append(0)
    f.append(1)
    g.append(0)
    for i in range(k+1,len(li)+1):
        f.append(0)
        g.append(0)
    l,a,b,r = k+1,k,0,k+1
    while r < len(li):
        d = 0
        for i in range(0,l+1):
            d = xor(d,f[i] * li[i+r-l])
        if d == 0:
            b += 1
        if d == 1:
            if 2*l > r:
                for i in range(0,l):
                    f[i] = (f[i] + g[i+(b-a)]) % 2
                b += 1
            if 2*l <= r:
                aux = copy.copy(f)
                for i in range(0,r+l):
                    f[i] = (aux[i+(a-b)] + g[i]) % 2
                l = r-l +1
                g = copy.copy(aux)
                a = b
                b = r - l + 1
        r += 1
    return l,f

def Sum_LFSR(li,li1,s,s1,k):
    salida = []
    a = LFSR(li,s,k)
    b = LFSR(li1,s1,k)
    for i,j in zip(a,b):
        salida.append(xor(i,j))
    return salida

def Mul_LFSR(li,li1,s,s1,k):
    salida = []
    a = LFSR(li,s,k)
    b = LFSR(li1,s1,k)
    for i,j in zip(a,b):
        salida.append(xor(i,j))
    return salida
    

def main():
    salir = False
    while salir == False:
        print("Seleccione lo que desea ejecutar: \n")
        print("1: Postulados de Golomb.")
        print("2: LFSR. ")
        print("3: NLFSR. ")
        print("4: Cifrado de Flujo. ")
        print("5: Berlekamp Massey. ")
        print("6: salir")
        seleccion = input()
        if seleccion == "1":
            print("##################POSTULADOS DE GOLOMB################## \n")
            print("Introduce bits a comprobar: \n")
            a = input()
            li = []
            for i in a:
                li.append(int(i))
            start_time = time.time()
            salida = Postulados_G(li)
            elapsed_time = time.time() - start_time
            print("Elapsed time: %0.10f seconds." % elapsed_time)
        if seleccion == "2":
            print("##################LFSR################## \n")
            print("Introduce Polinomio(ej: x^3 + x + 1 = 0,1,1): \n")
            a = input()
            li = []
            for i in a:
                li.append(int(i))
            print("Introduce la semilla: \n")
            b = input()
            s = []
            for i in a:
                s.append(int(i))
            print("Introduce la longitud")
            k = int(input())
            start_time = time.time()
            salida = NLFSR(li,s,k)
            print("La salida del NLFSR es: \n",salida)
            elapsed_time = time.time() - start_time
            print("Elapsed time: %0.10f seconds." % elapsed_time)
        if seleccion == "3":
            print("##################NLFSR################## \n")
            print("Vamos a introducir el Polinomio(ej: x + x*y + y + z + 1 [[0,0,1][0,1,1][0,1,0][1,0,0] [0,0,0]]): \n")
            print("Indica la cantidad de términos: ")
            n = int(input())
            init = []
            for i in range(0,n):
                print("Introduce el término ",i+1)
                a = input()
                li = []
                for i in a:
                    li.append(int(i))
                init.append(li)
            print("Introduce la semilla: \n")
            b = input()
            s = []
            for i in a:
                s.append(int(i))
            print("Introduce la longitud")
            k = int(input())
            start_time = time.time()
            salida = NLFSR(init,s,k)
            print("La salida del LFSR es: \n",salida)
            elapsed_time = time.time() - start_time
            print("Elapsed time: %0.10f seconds." % elapsed_time)
        elif seleccion == "4":
            print("##################CIFRADO DE FLUJO################## \n")
            print("Introduce mensaje a cifrar: \n")
            m = input()
            start_time = time.time()
            salida = Cifrado_flujo(m)
            print("La salida del cifrado de flujo es: \n",salida)
            elapsed_time = time.time() - start_time
            print("Elapsed time: %0.10f seconds." % elapsed_time)
        elif seleccion == "5":
            print("##################BERLEKAMP MASSEY################## \n")
            print("Introduce una sucaesión de bits periódica: \n")
            a = input()
            li = []
            for i in a:
                li.append(int(i))
            start_time = time.time()
            salida = Berlekamp_Massey(li)
            print("La complejidad lineal del polinomio es: \n",salida[0])
            print("El polinio es: \n",salida[1])
            elapsed_time = time.time() - start_time
            print("Elapsed time: %0.10f seconds." % elapsed_time)
        elif seleccion == "6":
            salir = True
        else:
            print("Selección incorrecta \n")
if __name__ == "__main__":
    main()
