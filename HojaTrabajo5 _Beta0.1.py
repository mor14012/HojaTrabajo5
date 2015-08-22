import simpy
import random

def proceso(nombre, tiempo, valor_ram_proceso, valor_instrucciones):
    global tiempo_total
    #creating process
    yield env.timeout(tiempo)
    inicio_proceso = env.now
    if(gui==1):
        print "\n---------------\n","| Proceso ",nombre,"|\n---------------"
        print " Tiempo de creacion",tiempo
    #new
    yield ram.get(valor_ram_proceso)
    if(gui==1):
        print " Memoria RAM del proceso: ", valor_ram_proceso,"\n"
    while(True):
        #ready
        with cpu.request() as solicitud:
            if(gui==1):
                print nombre, " Solicitando CPU"
            yield solicitud
            #running
            if(gui==1):
                print nombre, " Procesando instrucciones: ",valor_instrucciones
            valor_instrucciones-=valor_cpu_instrucciones
            yield env.timeout(unidad_tiempo)
        #terminated
        if(valor_instrucciones<valor_cpu_instrucciones):
            break
        else:
            numero_random = random.randint(1,2)
            if(numero_random==1):
                #waiting
                if(gui==1):
                    print nombre, " Espera. Haciendo operaciones de I/O"
                yield env.timeout(random.randint(1,10))
    ram.put(valor_ram_proceso)
    tiempo_proceso = env.now - inicio_proceso
    tiempo_total += tiempo_proceso
    if(gui==1):
        print nombre, " Finalizado en ",tiempo_proceso, " segundos"

#----- Variables -----
gui = 1                      
valor_ram = 100            
valor_cpu = 1               
valor_cpu_instrucciones = 3 
intervalo = 10              
unidad_tiempo = 1           
numero_procesos = 25        
random.seed(5)        
tiempo_total = 0.0   
#----- Simpy -----
env = simpy.Environment()                           #Creacion de ambiente de simulacion
ram = simpy.Container(env, valor_ram, valor_ram)    #Creacion de contenedor para RAM
cpu = simpy.Resource(env, valor_cpu)                #Creacion de resource para CPU

#Creacion de procesos
for i in range(numero_procesos):
    #Creacion de procesos en el ambiente, se envian los parametros requeridos a la funcion proceso
    env.process(proceso(str(i+1), random.expovariate(1.0/intervalo), random.randint(1,10), random.randint(1, 10)))
env.run()                                           #Ejecucion de simulacions
