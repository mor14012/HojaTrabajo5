'''
Universidad del Valle de Guatemala
Algoritmos y Estructura de Datos
Seccion: 10
Diego Morales. Carne: 14012
Julio Gonzalez. Carne: 14096
21/08/2015
Hoja de Trabajo 5

'''
import simpy #se importa el modulo Simpy y random
import random

def proceso(nombre, tiempo, valor_ram_proceso, valor_instrucciones): #Se define la funcion de proceso y las variables que utiliza
    global tiempo_total        # Se define la variable tiempo_total de manera global 
    #creating process
    yield env.timeout(tiempo) # Analiza el tiempo en crear el proceso 
    inicio_proceso = env.now
    if(gui==1):
        print "\n---------------\n","| Proceso ",nombre,"|\n---------------" #Se imprime le nombre del proceso que se inicia 
        print " Tiempo de creacion",tiempo #Se imprime el tiempo que tardo en crearse el proceso 
    #new
    yield ram.get(valor_ram_proceso) # Se analiza el valor de Ram que va utilizar el proceso y el tiempo de espera
    if(gui==1):
        print " Memoria RAM del proceso: ", valor_ram_proceso,"\n" #Se imprime la cantidad de memoria RAM que solicita el proceso 
    while(True):
        #ready
        with cpu.request() as solicitud: # Se ve lo que el proceso solicita de ram y se espera lo necesario hasta que la capacidad permite que continue
            if(gui==1):
                print nombre, " Solicitando CPU" 
            yield solicitud #Aca se analiza disponibilidad 
            #running
            if(gui==1):
                print nombre, " Procesando instrucciones: ",valor_instrucciones # Se imprime la instruccion actual que se procesa 
            valor_instrucciones-=valor_cpu_instrucciones # Se le resta a valor de instrucciones y actualiza variable 
            yield env.timeout(unidad_tiempo) #Se analiza el tiempo trasncurrido  en porcesar instrucciones
        #terminated
        if(valor_instrucciones<valor_cpu_instrucciones): # Se analiza si el valor de instrucciones es menor al que ejecuta el CPU se termina los procesos
            break # Se sale
        else:
            numero_random = random.randint(1,2) # Se hace un random para determinar si continua o espera
            if(numero_random==1):
                #waiting
                if(gui==1):
                    print nombre, " Espera. Haciendo operaciones de I/O"
                yield env.timeout(random.randint(1,10)) # Se analiza si ya se puede proceder despues de estar esperando para proceder
    ram.put(valor_ram_proceso) #Se  analiza si hay espacio suficiente en memoria para ejecutar
    tiempo_proceso = env.now - inicio_proceso #Se calcula el tiempo que tardo el proceso en ejecutar y correr conn el tiempo actual que llevade ejecucion el programa
    tiempos_procesos.append(tiempo_proceso) #Se agrega al final el tiempo que tado el proceso actual en ejecutarse a la lista de la variabel tiempos_procesos
    tiempo_total += tiempo_proceso # Se suma lo que se tiene en tiempo proceso a tiempo total y se actualiza el valor de la variable 
    if(gui==1):
        print nombre, " Finalizado en ",tiempo_proceso, " segundos" #Se imprime que el proceso fue finalizado

#----- Variables -----
gui = 1                     #Graphical User Interface, seleccionar 1 si se desea imprimir los resultados en tiempo real
valor_ram = 100             #Tamano de Memoria RAM
valor_cpu = 1               #Numero de CPUs
valor_cpu_instrucciones = 3 #Numero de instrucciones que ejecuta el CPU
intervalo = 10              #Intervalo del Random de tiempo inicial de procesos
unidad_tiempo = 1           #Unidad de tiempo del CPU en segundos 
numero_procesos = 25        #Numero de procesos que se generan 
tiempos_procesos=[]         #Array de los tiempos de cada proceso para calcular desviacion estandar
random.seed(5)              #Random seed para que los numeros random generados no varien
tiempo_total = 0.0          #Tiempo total de ejecucion de todas las instrucciones
desviacion = 0.0            #Valor de la desviacion estandar calculada
media = 0.0                 #Valor de la media del tiempo de ejecuacion de instruccion
#----- Simpy -----
env = simpy.Environment()                           #Creacion de ambiente de simulacion
ram = simpy.Container(env, valor_ram, valor_ram)    #Creacion de contenedor para RAM
cpu = simpy.Resource(env, valor_cpu)                #Creacion de resource para CPU

#Creacion de procesos
for i in range(numero_procesos):
    #Creacion de procesos en el ambiente, se envian los parametros requeridos a la funcion proceso
    env.process(proceso(str(i+1), random.expovariate(1.0/intervalo), random.randint(1,10), random.randint(1, 10)))
env.run()                                           #Ejecucion de simulacions
#Calculo de resultados
media = tiempo_total/numero_procesos                #Calculo de la media
for i in tiempos_procesos:                          #Calculo de la desviacion Estandar
    desviacion+=((i-media)**2)                      #Se resta la media al tiempo del proceso y se eleva al cuadrado
desviacion/=numero_procesos                         #Division entre numero de elementos
desviacion=desviacion**(0.5)                        #Raiz de resultado 
print "\nTiempo Promedio Proceso: ", media          #Se imprime el tiempo promedio
print "Desviacion Estandar: ",desviacion            #Se imprime la desviacion Estandar
