#-*- encoding: utf-8 -*-
#páginas de pruebas
#http://www.numbertheory.org/php/php.html
#http://primes.utm.edu/
#Autor: Pedro Luis Trigueros Mondéjar
#DNI: 53593707-G
from random import randint
from timeit import time
import math


#Ejercicio 1 Implementa el algoritmo extendido de Euclides para el cálculo del máximo común divisor: dados
#dos enteros a y b, encuentra u, v ∈ Z tales que au +bv es el máximo común divisor de a y b

def intercambiar(a,b):
    a , b = b , a
    return a,b

def Bezout(a,b):
##    if a<b: #si un número es mayor que otro se intercambian
##        inter = intercambiar(a,b)
##        a , b = (inter[0] , inter[1])
    if b==0: 
        return (1, 0, a)
    else: 
        x , y = (a,b)
        valoru, valorv = (0,1) #rellenamos la tabla al inicio
        valoru1 , valorv1 = (1,0)
        valoru2 , valorv2 = (0,1)
        resto = x % y #calculamos el primer resto
        c=0
        while resto!=0:
             c = (x // y) #cálculo del cociente seleccionando la parte entera
             #calculamos los nuevos valores de la tabla solapando los anteriores
             valoru = valoru1 - ( c * valoru2) 
             valorv = valorv1 - ( c * valorv2)
             valoru1 , valorv1 = (valoru2 , valorv2) 
             valoru2 , valorv2 = (valoru , valorv)
             x , y = (y , resto)
             resto= x % y #vamos calculando los demás restos
        if y < 0:
            return -valoru,-valorv,-y
        else:
            return valoru,valorv,y
    
#Ejercicio 2. Usando el ejercicio anterior, escribe una función que calcule a^(−1) mod b
#para cualesquiera a,b enteros que sean primos relativos

def inverso_modular(a,b):
    #utilizamos Bezout
    valor = Bezout(a,b)
    # si el mcd es distinto de 1 no son primos relativos
    if valor[2]!=1:
        raise ValueError
    else:
        #si no, el inverso es la u
        inverso = valor[0] % b
        return inverso
    
#Ejercicio 3. Escribe una función que calcule a ^ b mod n para cualesquiera a, b y n enteros positivos.
#La implementación debería tener en cuenta la representación binaria de b ([1, Algorithm 2.143]).
    
def potencia_mod(a,b,n):
    producto=1
    ta=a
    for i in range(0,b.bit_length()):#longitud de bits en b
        valor = b >> i & 1 #trasladamos i bits y comprobamos si vale 1
        if valor == 1: 
            producto *= ta #multiplicas si valor es distinto de 0 para que se obtenga productorio(a^((2^i)^bi))
            producto %= n
        ta = ta * ta #vas multiplicando a^(2^i) que con el bucle es 1,2,4,8,...
        ta %= n
    return producto    

#Ejercicio 4. Dado un entero p, escribe una función para determinar si p es (probablemente) primo usando el
#método de Miller-Rabin ([3, C.9.5]).

def descomposicion(m):
    u=0
    s=m
    while s % 2 == 0: #se va dividiendo el número hasta que de un impar
        u += 1 #se va sumando 1 al exponente
        s = s//2 #se divide entre 2
    return u,s


def Miller_Rabin(a,des,s,p):
    a = potencia_mod(a,s,p) #calculamos la potencia del número en mod p
    if a==1 or a == p-1: #comprobamos si puede ser un posible primo
        return True
    else:
        for i in range(1,des):
            a = (a * a) % p #cuadrado del número módulo p
            if a == p-1: #Es primo
                return True
            if a == 1: #No es primo
                return False

def test_Miller_Rabin(p):
    #condiciones de fallo de número
    if p == 2 or p == 3:
        return "probablemente primo"
    if( p<5):
        return "número incorrecto"
    if p%2==0:
        return "p no es primo, es par"
    else: #si no falla se coge p-1
        candidato = p-1;
        des = descomposicion(candidato) #lo descomponemos de la forma (2^u)*s
        j = 0
        s = des[1] #seleccionamos la parte entera del número
        bandera= True
        while j<200 and bandera==True: #comprobamos varias veces el test, para aumentar la probabilidad
            j += 1
            a = randint(2,p-2) #seleccionamos un número aleatorio entre 2 y p-2
            bandera = Miller_Rabin(a,des[0],s,p)
        if bandera == True:
            return "probablemente primo"
        return "no es primo"

#Ejercicio 5. Implementa el algoritmo paso enano-paso gigante para el cálculo de algoritmos discretos en Zp
def isqrt(n): #raiz cuadrada entera
    x = n
    y = (x + 1) // 2
    while y < x:
        x=y
        y = (x + n // x) // 2
    return x

def Paso_enano_gigante(a,b,p):
    s = isqrt(p-1)#calculamos la raiz de p-1 y cogemos la parte entera
    L = [] #creamos una lista L
    exp = s #asignaciones
    producto = b
    variable = potencia_mod(a,exp,p) #asignamos la potencia a una variable
    valor = variable
    for i in range(0,s):
        L = L + [producto % p] #introducimos los elementos del tipo b,b*a,b*a^2...b*a^s en la lista
        producto *= a
    for i in range (1,s+1): #comparamos si un valor generado en "otra lista"
        for j in range (0,s): #que no se crea por eficiencia, coincide con un valor de la lista L
            if(valor == L[j]):
                return s*i-j
        valor = (valor * variable) % p #valores que generamos para comprobar si son iguales de la forma a^s, a^2s...a^ss
    return "no existe solución"

#Ejercicio 6. Sea n = pq, con p y q enteros primos positivos.
#Escribe una función que, dado un entero a y un primo p con (a/p)= 1, devuelve r tal que r^2 ≡ a mod p
#([3, §2.3.4]; primero te hará falta implementar el símbolo de Jacobi [1, 2.149]).

def Jacobi(p,m):
    if m % 2 == 0:
        return "No se puede calcular"
    if p == 0:#casos base
        return 0
    if p == 1:
        return 1
    if p == 2 and (m % 8 == 1 or m % 8 == 7):
        return 1
    if p == 2 and (m % 8 == 3 or m % 8 == 5):
        return -1
    if p % 2 == 0: #si p mod 2 es 0, es que es par y se puede dividir en dos partes el problema
        return Jacobi(2,m) * Jacobi(p//2,m)
    if p % 4 == 3 and m % 4 == 3:
        return (-1) * Jacobi(m%p,p)
    else:
        return Jacobi(m%p,p)

def raices_modulares(a,p):
    t = test_Miller_Rabin(p)
    if t != "probablemente primo":
        return "el segundo valor no es primo"
    des = descomposicion(p-1) #lo descomponemos de la forma (2^u)*s
    if des[0]==1:
        return potencia_mod(a,(des[1]+1)//2,p) #devolvemos a^((s+1)/2)
    sj=0
    m = 1
    while sj!=-1:
        m += 1
        sj = Jacobi(m,p) #seleccionamos un número de Jacobi
    r = potencia_mod(a,(des[1]+1)//2,p) #2^((s+1)/2)
    b = potencia_mod(m,des[1],p)
    inv = inverso_modular(a,p)
    for i in range (0,des[0]-2): #recorremos todos los posibles casos
        if potencia_mod( inv * potencia_mod(r,2,p),2**(des[0]-2-i),p)==p-1: #si se cumple esto es porque vale -1
            r *= b #lo multiplicamos por b
            print("el valor de r es:",r)
        b = potencia_mod(b,2,p) #elevamos al cuadrado
    return r;
    
#Sea a un entero que es residuo cuadrático módulo p y q. Usa el teorema chino de los restos para calcular
#todas las raíces cuadradas de a mod n a partir de las raíces cuadradas de a módulo p y q.

def T_chino_restos(a,b,p,q): #Teorema chino de los restos
    i = inverso_modular(p,q) # hacemos el inverso de p en q ya que se multiplica luego por (b-a)
    k = ((b - a) *i) % q #obtenemos k en módulo q para obtener x
    x = a + p * k #calculamos x
    return x

def levantar_raices(a,p,q):
    b = raices_modulares(a,p)
    c = raices_modulares(a,q)
    e = T_chino_restos(b,c,p,q)
    f = T_chino_restos(b,q-c,p,q)
    g = T_chino_restos(p-b,c,p,q)
    h = T_chino_restos(p-b,q-c,p,q)
    return e,f,g,h
#Ejercicio 7.
#Implementa el Método de Fermat para factorización de enteros.
#Implementa el algoritmo de factorización ρ de Pollard ([1, 3.9])


def cuadrado(n): #Función que devuelve si es cuadrado perfecto
    raiz = isqrt(n)
    if raiz * raiz == n:
        return True
    return False #si no(termina el bucle), no es cuadrado perfecto

def Fermat(p):#función que factoriza un número entero como diferencia de los cuadrados
    if p % 2 == 0:#si el número es par sale
        return "el número es par"
    raiz = isqrt(p) 
    bcuad = ( raiz * raiz ) - p  #raíz al cuadrado menos el número
    escuadrado = False
    while escuadrado == False: #mientras no sea un cuadrado perfecto
        raiz += 1 #aumentamos raíz a 1
        bcuad = ( raiz * raiz ) - p #raíz al cuadrado menos el número
        if cuadrado(bcuad) == True:
            escuadrado = True
    return raiz - isqrt(bcuad)
    
def f(x): #función a utilizar en Pollard
    return x * x + 1

def Pollard(p):
    z=1 #valor para mcd
    iter1 = 1000 #iteraciones del primer bucle
    iter2 = 100 #iteraciones del segundo bucle, elementos que cogemos para mcd
    x = 0 #primer elemento de la función
    x = f(x) % p #calculamos la funcion en x
    y = f(x) % p #calculamos el valor de la función en y
    for i in range (0,iter1):
        for j in range (0,iter2):
            z = (z * (x - y)) % p #calculo del valor para mcd
            x = f(x) % p #funcion en x
            y = f(f(y)) % p #función en y aumentando el 2
        d = Bezout(z,p) #mcd
        if d[2] != 1: #devolvemos si se han encontrado los valores
            return d[2]
    return "no se ha encontrado valor"
            
def main():
    salir = False
    while salir == False:
        print("Seleccione lo que desea ejecutar: \n")
        print("1: Bezout.")
        print("2: Inverso modular. ")
        print("3: Potencia modular. ")
        print("4: Test Miller-Rabin. ")
        print("5: Paso enano-gigante. ")
        print("6: Teorema chino de los restos. ")
        print("7: Jacobi. ")
        print("8: Raices modulares. ")
        print("9: Pollard. ")
        print("10: Fermat. ")
        print("11: Levantar raices. ")
        print("12: salir")
        seleccion = input()
        if seleccion == "1":
            #5,9
            print("##################BEZOUT################## \n")
            print("Dime el valor de a: \n")
            a = int(input())
            print("Dime el valor de b: \n")
            b = int(input())
            start_time = time.time()
            salida = Bezout(a,b)
            elapsed_time = time.time() - start_time
            print("Los valores de Bezout son:","\nValor de u: ",salida[0],"\nValor de v: ",salida[1],"\nValor de mcd: ",salida[2])
            print("Elapsed time: %0.10f seconds." % elapsed_time)
        elif seleccion == "2":
            print("##################INVERSO MODULAR################## \n")
            print("Dime el valor de a: \n")
            a = int(input())
            print("Dime el valor de b: \n")
            b = int(input())
            start_time = time.time()
            salida1 = inverso_modular(a,b)
            elapsed_time = time.time() - start_time
            print("El inverso modular es: " , salida1)
            print("Elapsed time: %0.10f seconds." % elapsed_time)
        elif seleccion == "3":
            print("##################POTENCIA MODULAR################## \n")
            print("Dime el valor de a: \n")
            a = int(input())
            print("Dime el valor de n: \n")
            n = int(input())
            print("Dime el valor de p: \n")
            p = int(input())
            start_time = time.time()
            salida2 = potencia_mod(a,n,p)
            elapsed_time = time.time() - start_time
            print("Potencia Modular: ",salida2)
            print("Elapsed time: %0.10f seconds." % elapsed_time)
        elif seleccion == "4":
            print("##################TEST DE MILLER-RABIN################## \n")
            print("Dime el valor de a: \n")
            a = int(input())
            start_time = time.time()
            salida3 = test_Miller_Rabin(a)
            elapsed_time = time.time() - start_time
            print("Resultado Test Miller-Rabin: ",salida3)
            print("Elapsed time: %0.10f seconds." % elapsed_time)
        elif seleccion == "5":
            print("##################PASO ENANO-GIGANTE################## \n")
            print("Dime el valor de a: \n")
            a = int(input())
            print("Dime el valor de n: \n")
            n = int(input())
            print("Dime el valor de p: \n")
            p = int(input())
            start_time = time.time()
            salida4 = Paso_enano_gigante(a,b,p)
            elapsed_time = time.time() - start_time
            print("La solución Paso-enano-gigante es: ",salida4)
            print("Elapsed time: %0.10f seconds." % elapsed_time)
        elif seleccion == "6":
            print("##################TEOREMA CHINO DE LOS RESTOS################## \n")
            print("Dime el valor de a: \n")
            a = int(input())
            print("Dime el valor de n: \n")
            n = int(input())
            print("Dime el valor de p: \n")
            p = int(input())
            print("Dime el valor de q: \n")
            q = int(input())
            start_time = time.time()
            salida5 = T_chino_restos(a,b,p,q)
            elapsed_time = time.time() - start_time
            print("La salida del Teorema chino de los restos es: ",salida5)
            print("Elapsed time: %0.10f seconds." % elapsed_time)
        elif seleccion == "7":
            print("##################JACOBI################## \n")
            print("Dime el valor de p: \n")
            p = int(input())
            print("Dime el valor de m: \n")
            m = int(input())
            start_time = time.time()
            salida6 = Jacobi(p,m)
            elapsed_time = time.time() - start_time
            print("La salida de Jacobi es: ", salida6)
            print("Elapsed time: %0.10f seconds." % elapsed_time)
        elif seleccion == "8":
            print("##################RAICES MODULARES################## \n")
            print("Dime el valor de a: \n")
            a = int(input())
            print("Dime el valor de p: \n")
            p = int(input())
            start_time = time.time()
            salida7 = raices_modulares(a,p)
            elapsed_time = time.time() - start_time
            print("La raiz modular es: ",salida7)
            print("Elapsed time: %0.10f seconds." % elapsed_time)
        elif seleccion == "9":
            print("##################POLLARD################## \n")
            print("Dime el valor de a: \n")
            a = int(input())
            start_time = time.time()
            salida8 = Pollard(a)
            elapsed_time = time.time() - start_time
            print("Pollard es: ",salida8)
            print("Elapsed time: %0.10f seconds." % elapsed_time)
        elif seleccion == "10":
            print("##################FERMAT################## \n")
            print("Dime el valor de a: \n")
            a = int(input())
            start_time = time.time()
            salida9 = Fermat(91)
            elapsed_time = time.time() - start_time
            print("Fermat es:",salida9)
            print("Elapsed time: %0.10f seconds." % elapsed_time)                
        elif seleccion == "11":
            print("##################LEVANTAR RAICES################## \n")
            print("Dime el valor de a: \n")
            a = int(input())
            print("Dime el valor de p: \n")
            p = int(input())
            print("Dime el valor de q: \n")
            q = int(input())
            start_time = time.time()
            salida10 = levantar_raices(a,p,q)
            elapsed_time = time.time() - start_time
            print("levantar raices: ",salida10)
            print("Elapsed time: %0.10f seconds." % elapsed_time)
        elif seleccion == "12":
            salir = True
        else:
            print("Selección incorrecta \n")
if __name__ == "__main__":
    main()
