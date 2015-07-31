#-*- encoding: utf-8 -*-
#Práctica III Criptografía
#Funciones de un solo sentido
#Autor: Pedro Luis Trigueros Mondéjar
#DNI: 53593707-G
from random import randint
import práctica1.py

import uuid
import hashlib

#Ejercicio 1. Sea (a1, . . . ,ak ) una secuencia super-creciente de números positivos (la suma de los términos que preceden a ai es menor que ai
#, para todo i). Elige n > sum(ai) y u un entero positivo tal que gcd(n,u)=1.
#Define a* = uai mod n. La función mochila (knapsack) asociada a (a1* , . . . ,ak*) es
#f : Zk2 -> N, f (x1, . . . ,xk )=sum(xi ai*). Implementa esta función y su inversa, tal y como se explica en [2, §4.5]. La llave pública es (a*
#1 , . . . ,ak* ), mientras que la privada (y puerta de atrás) es ((a1, . . . ,ak ),n,u).


def super_creciente(li):
    #clave privada
    u,n,k = 41651,2097152,20
    sucesion = []
    for i in range(0,k):
        sucesion.append(2**i)
    #clave pública
    publica = []
    for i in range(0,k):
        publica.append((sucesion[i]*u)% n)
    #calculamos el valor
    coste = 0
    for i,j in zip(publica,li):
        coste = (coste + i*j) % n 
    return coste 

def super_creciente_inv(coste):
    #clave privada
    u,n,k = 41651,2097152,20
    sucesion = []
    for i in range(0,k):
        sucesion.append((2**i) % n)
    #inverso de 3, llave privada
    inverso = práctica1.inverso_modular(u,2097152)
    s = (coste * inverso) %  n
    #lista de salida
    salida = []
    i = k
    while s !=0:
        if s >= sucesion[i-1]:
            s -= sucesion[i-1]
            salida.append(1)
        else:
            salida.append(0)
        i -= 1
    if len(salida) != k:
        for i in range(len(salida),k):
            salida.append(0)
    salida.reverse()
    return salida

###Ejercicio 2. Sea p un (pseudo-)primo mayor o igual que vuestro número de identidad. Encuentra un
###elemento primitivo, alfa, de Z*p (se puede usar [3, 2.132 (iv)]; para facilitar el criterio, es bueno escoger p de
###forma que (p - 1)/2 sea también primo, y para ello usamos (Miller-Rabin). Definimos
###f : Zp -> Zp, x -> alfa^x .
###Calcula el inverso de tu fecha de nacimiento con el formato AAAAMMDD.
###En lo que sigue, p y q son enteros primos, y n = pq.

def primitivo(n):
    n += (3 - n)% 4 #con esto evitamos que si entra un numero par, se quede de manera par 
    q = int((n-1)/2) #lo dividimos entre 2 para calcular primero el primo pequeño
    primo = False
    while primo == False:
        pprimo = práctica1.test_Miller_Rabin(q) #comprobamos si q es primo
        if pprimo == "probablemente primo":
            pprimo1 = práctica1.test_Miller_Rabin(2*q+1)#comprobamos si 2*q+1 es primo
            if pprimo1 == "probablemente primo":
                n = 2*q+1 # si los dos son primos, tenemos primo
                primo = True
            else:
                q += 2 #si no, aumentamos el bucle de dos en dos
        else:
            q += 2
    i,p = 2,0
    primitivo = False
    while primitivo == False and i < n-2:
        p = i
        prim = práctica1.Jacobi(i,n)
        if prim == -1:
            primitivo = True
    return práctica1.Paso_enano_gigante(p,19921030,n),p,n
    

        
###Ejercicio 3. Sea f : Zn → Zn la función de Rabin: f (x) = x^2. Sea n = 48478872564493742276963. Sabemos
###que f (12) = 144 = f (37659670402359614687722). Usando esta información, calcula p y q (mira la
###demostración de [1, Lemma 2.43]).

def descodificar_Rabin():
    p = práctica1.Bezout(48478872564493742276963,37659670402359614687722+12)
    q = práctica1.Bezout(48478872564493742276963,37659670402359614687722-12)
    return p[2],q[2]

###Ejercicio 4. Elige a0 y a1 dos cuadrados arbitrarios módulo n (n como en el Ejercicio 3). Sea
###h : Z2x(Zn)* -> (Zn)*, h(b,x) = x^2 a0^b  a1^(1-b).
###Usa la construcción de Merkle-Damgard para implementar una función resumen tomando h como función
###de compresión (esta h fue definida por Goldwasser, Micali y Rivest). Los parámetros a0, a1 y n se
###hacen públicos (la función debería admitir un parámetro en el que venga especificado el vector inicial).
##
def h(b,x,a0,a1,n):
    return ((x**2)  * (a0**b) * (a1 **(1-b))) % n

def Merkle_Damgard(li,x):
    n = 48478872564493742276963
    a0, a1 = (596822145236698**2) % n,(3514861561631611**2) % n
    coste = 0
    for i in range(0,len(li)):
        coste = h(li[i],x,a0,a1,n)    
        x = coste
    return coste

###Ejercicio 5. Sea p el menor primo entero mayor o igual que tu número de identidad, y sea q el primer
###primo mayor o igual que tu fecha de nacimiento (AAAAMMDD). Selecciona e tal que gcd(e, (p-1)(q-1))=1. Define la función RSA
###f : Zn -> Zn, x -> x^e .
###Calcula el inverso de 1234567890.

def Calculoe():
    esprimo = False
    i,j =53593707,19921031
    priDNI,priFN,e = 0,0,0 
    while(esprimo ==False):
        if (práctica1.test_Miller_Rabin(i) == "probablemente primo"): #buscamos número primo cercano al DNI
            priDNI = i
            esprimo = True
        else:
            i += 2
    esprimo = False
    while(esprimo ==False):
        if (práctica1.test_Miller_Rabin(j) == "probablemente primo"): #buscamos número primo cercano a la fecha de nacimiento
            priFN = j
            esprimo = True
        else:
            j += 2
    noencontrado = False
    k = 16341684165161
    while(noencontrado == False):
        mcd = práctica1.Bezout(k,(priDNI-1)*(priFN))
        if(mcd[2] == 1):
            e = k
            noencontrado = True
        else:
            k += 1
    return e,priDNI,priFN

def Calculod():
    valores = Calculoe()
    d = práctica1.inverso_modular(valores[0],(valores[1]-1)*(valores[2]-1))#inverso de e mod p-1*q-1
    return d,valores[0],valores[1],valores[2]
    
def RSA(n):
    valores = Calculod()
    return práctica1.potencia_mod(n,valores[0],valores[2]*valores[3])

###Ejercicio 6. Sea n = 50000000385000000551, y que sabemos que una inversa de Zn -> Zn, x -> x^5 es x ->
###x^10000000074000000101 (esto es, conoces tanto la llave pública como la privada de la función RSA). Encuentra
###p y q usando el método explicado en [2, Page 92].Compara este procedimiento con el algoritmo deMiller-
###Rabin y el Ejercicio 3.

def Factorizacion(b,n):
    noencontrado = False
    primerbucle = False
    aux = práctica1.descomposicion(5*b-1)
    a = randint(2,n-1)
    while(primerbucle == False):
        a = práctica1.potencia_mod(a,aux[1],n)
        if a == 1 or a == n-1:
            a = randint(2,n-1)
        else:
            primerbucle= True
    while(noencontrado == False):
        z = (a**2) % n
        if z == 1:
            mcd1 = práctica1.Bezout(n,a+1)
            mcd2 = práctica1.Bezout(n,a-1)
            return mcd1[2],mcd2[2]
        if z == n-1:
            primerbucle = False
            a = randint(2,n-1)
            while(primerbucle == False):
                a = práctica1.potencia_mod(a,aux[1],n)
                if a == 1 or a == n-1:
                    a = randint(2,n-1)
                else:
                    primerbucle= True
        else:
            a = z
        
    

###Ejercicio 7. En este ejercicio se pide implementar un sistema de firma digital y verificación de la firma. Se
###puede elegir entre firma RSA o DSS.
###Al igual que antes, debe realizar tres tareas: generación de claves (ejercicios anteriores), generación de
###firma y verificación de firma.
###Para la generación de la firma, se le introducirá un mensaje a cifrar (fichero) y el fichero con la clave
###(privada), y deberá generar una firma, que se guardará en un fichero de texto.
###Puesto que lo que realmente se firma no es el mensaje, sino un resumen del mensaje, hay que generar
###un resumen de dicho mensaje. Para esto emplearemos la función SHA1 (se pueden añadir otras funciones
###resumen). Cualquiera de las implementaciones de esta función que hay en la red puede ser usada.
###Para la verificación de la firma, se introduce el mensaje (fichero) que se ha firmado, un fichero con la
###firma (con el mismo formato que el generado en el apartado anterior) y un fichero con la clave (pública).
###Deberá responder si la firma es o no válida.


def GenerarClaves():
    p,q = 0,0
    l = pow(2,511) #l-1
    s = pow(2,159)+1
    t = pow(2,1024)
    u = pow(2,160)
    alfa = 0
    escongruente = False
    esprimo = False
    while esprimo ==False and s<=u:
        if (práctica1.test_Miller_Rabin(s) == "probablemente primo"): #buscamos número primo entre 2^159 y 2^160
            q = s
            esprimo = True
        else:
            s += 2
    esprimo = False
    while esprimo ==False and l<=t:
        p = l*q + 1
        if (práctica1.test_Miller_Rabin(p) == "probablemente primo"): #buscamos número primo entre 2^511 y 2^1024
            esprimo = True
        else:
            l += 2
    while escongruente == False:
        g = randint(2,p-2) #número entre 2 y p-2
        alfa = práctica1.potencia_mod(g,(p-1)//q,p) #cáculo de alfa
        if alfa !=1:
            escongruente = True
        else:
            g += 1
    x = randint(2,q-2) #número entre 2 y q-2
    y =  práctica1.potencia_mod(alfa,x,p)
    outfile = open('público.txt', 'w') # Indicamos el valor 'w'.
    #escribimos en el fichero público los valores
    outfile.write(str(p))
    outfile.write('\n')
    outfile.write(str(q))
    outfile.write('\n')
    outfile.write(str(alfa))
    outfile.write('\n')
    outfile.write(str(y))
    # Cerramos el fichero.
    outfile.close()
    outfile = open('privado.txt', 'w') # Indicamos el valor 'w'.
    #escribimos en el fichero privado los valores
    outfile.write(str(p))
    outfile.write('\n')
    outfile.write(str(q))
    outfile.write('\n')
    outfile.write(str(alfa))
    outfile.write('\n')
    outfile.write(str(x))
    outfile.write('\n')
    outfile.write(str(y))
    # Cerramos el fichero.
    outfile.close()
    print("Claves generadas correctamente")

def DSS(ficherofirmar,firmaprivada):
    #abrimos ficheros de firma publica
    fich = open(firmaprivada)
    fichero = fich.readlines()
    #recuperamos valores de p,q,alfa,x,y
    p = int(fichero[0])
    q = int(fichero[1])
    alfa = int(fichero[2])
    x = int(fichero[3])
    y = int(fichero[4])
    #abrimos el fichero a firmar.
    infile = open(ficherofirmar, 'r')
    cifrar = infile.read()
    resumen = hashlib.md5()
    resumen.update(cifrar.encode('utf-8'))
    resumen = resumen.hexdigest()
    resumen = int(resumen,16)
    k = randint(2,q-2)
    r = (práctica1.potencia_mod(alfa,k,p)) % q
    s = ((resumen+x*r) * práctica1.inverso_modular(k,q)) % q
    outfile = open("firma.txt", 'w') # Indicamos el valor 'a'.
    outfile.write('\n')
    outfile.write(str(r))
    outfile.write('\n')
    outfile.write(str(s))
    outfile.close()
    print("Fichero firmado")

def ComprobarDSS(ficherofirmado,firmapublica,firma):
    #abrimos ficheros de firma publica
    fich = open(firmapublica)
    fichero = fich.readlines()
    #cerramos fichero de firma publica
    fich.close()
    #abrios fichero firmado
    fich1 = open(ficherofirmado)
    fichero1 = fich1.readlines()
    #cerramos el fichero firmado
    fich1.close()
    #abrios fichero firmado
    fich2 = open(firma)
    fichero2 = fich2.readlines()
    #cerramos el fichero firmado
    fich2.close()
    #recuperamos valores de p,q,alfa,r,s
    p = int(fichero[0])
    q = int(fichero[1])
    alfa = int(fichero[2])
    y = int(fichero[3])
    s = int(fichero2[-1])
    r = int(fichero2[-2])
    aux = ""
    for i in fichero1:
        aux += i
    resumen = hashlib.md5()
    resumen.update(aux.encode('utf-8'))
    resumen = resumen.hexdigest()
    resumen = int(resumen,16)
    inv_s = práctica1.inverso_modular(s,q)
    u = (resumen * inv_s) % q 
    v = (r * inv_s) % q
    alfau = práctica1.potencia_mod(alfa,u,p)
    yv = práctica1.potencia_mod(y,v,p)
    auyv = (alfau * yv) % p
    rpri = auyv % q
    if(r == rpri):
        print("La firma es valida")
        return True
    else:
        print("Firma incorrecta")
        return False


    
def main():
    salir = False
    while salir == False:
        print("Seleccione lo que desea ejecutar: \n")
        print("1: Mochila.")
        print("2: Inverso Mochila. ")
        print("3: Primitivo. ")
        print("4: Descodificar Rabin. ")
        print("5: MerkleDamgard. ")
        print("6: RSA. ")
        print("7: Factorizacion. ")
        print("8: Generar claves DSS. ")
        print("9: DSS. ")
        print("10: Comprobar DSS. ")
        print("11: salir")
        seleccion = input()
        if seleccion == "1":
            print("##################MOCHILA################## \n")
            print("Dime el valor de a: (usado [1,1,0,0,1,1,0,1,1,1,1,1,0,1,1,1,0,1,1,1])\n")
            a = input()
            li = []
            for i in a:
                li.append(int(i))
            start_time = time.time()
            salida = super_creciente(li)
            elapsed_time = time.time() - start_time
            print("Mochila es: ", salida)
            print("Elapsed time: %0.10f seconds." % elapsed_time)
        elif seleccion == "2":
            print("##################INVERSO MOCHILA################## \n")
            print("Dime el valor de a: \n")
            a = int(input())
            start_time = time.time()
            salida1 = super_creciente_inv(a)
            elapsed_time = time.time() - start_time
            print("El inverso mochila es: " , salida1)
            print("Elapsed time: %0.10f seconds." % elapsed_time)
        elif seleccion == "3":
            print("##################PRIMITIVO################## \n")
            print("Dime el valor de a: (prueba 53593707)\n")
            a = int(input())
            start_time = time.time()
            salida2 = primitivo(a)
            elapsed_time = time.time() - start_time
            print("Primivivo: ",salida2[0],salida2[1],salida2[2])
            print("Elapsed time: %0.10f seconds." % elapsed_time)
        elif seleccion == "4":
            print("##################DESCODIFICAR RABIN################## \n")
            start_time = time.time()
            salida3 = descodificar_Rabin()
            elapsed_time = time.time() - start_time
            print("Resultado Descodificar Rabin: ",salida3[0], salida3[1])
            print("Elapsed time: %0.10f seconds." % elapsed_time)
        elif seleccion == "5":
            print("##################MERKLE DAMGARD################## \n")
            print("Dime el valor de a: (prueba [0,1,1,0],4235793452357)\n")
            a = input()
            li = []
            for i in a:
                li.append(int(i))
            print("Dime el valor de x: \n")
            x = int(input())
            start_time = time.time()
            salida4 = Merkle_Damgard(li,x)
            elapsed_time = time.time() - start_time
            print("La solución Merkle Damgard es: ",salida4)
            print("Elapsed time: %0.10f seconds." % elapsed_time)
        elif seleccion == "6":
            print("##################RSA################## \n")
            print("Dime el valor de a: (rpueba 1234567890)\n")
            a = int(input())
            start_time = time.time()
            salida5 = RSA(a)
            elapsed_time = time.time() - start_time
            print("La salida del RSA es: ",salida5)
            print("Elapsed time: %0.10f seconds." % elapsed_time)
        elif seleccion == "7":
            print("##################FACTORIZACION################## \n")
            print("Dime el valor de b: (prueba 10000000074000000101 y 50000000385000000551)\n")
            b = int(input())
            print("Dime el valor de n: \n")
            n = int(input())
            start_time = time.time()
            salida6 = Factorizacion(b,n)
            elapsed_time = time.time() - start_time
            print("La salida de Factorizacion es: ", salida6[0], salida6[1])
            print("Elapsed time: %0.10f seconds." % elapsed_time)
        elif seleccion == "8":
            print("##################GENERAR CLAVES DSS################## \n")
            start_time = time.time()
            GenerarClaves()
            elapsed_time = time.time() - start_time
            print("Elapsed time: %0.10f seconds." % elapsed_time)
        elif seleccion == "9":
            print("##################DSS################## \n")
            print("Fichero a firmar: \n")
            ficherofirmar = input()
            print("Introduce el fichero con firma privada: \n")
            firmaprivada = input()
            start_time = time.time()
            DSS(ficherofirmar,firmaprivada)
            elapsed_time = time.time() - start_time
            print("Elapsed time: %0.10f seconds." % elapsed_time)
        elif seleccion == "10":
            print("##################COMPROBAR DSS################## \n")
            print("Fichero a comprobar: \n")
            ficherocomprobar = input()
            print("Fichero firma publica: \n")
            firmapublica = input()
            print("Fichero con firma: \n")
            firma = input()
            start_time = time.time()
            ComprobarDSS(ficherocomprobar,firmapublica,firma)
            elapsed_time = time.time() - start_time
            print("Elapsed time: %0.10f seconds." % elapsed_time)                
        elif seleccion == "11":
            salir = True
        else:
            print("Selección incorrecta \n")
if __name__ == "__main__":
    main()
    
    
