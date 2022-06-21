from util import Server
from util import Util
from patient import Patient
import simpy
import random

print('Aguardando conexão')
conn, ender = Server.create_server()

while True:

    #Recebendo mensagem do cliente
    message = Server.get_message(conn)
    if not message:
        error = 'Encerrando conexão'
        print(error)
        Server.send_message(conn, error)
        conn.close()
        break

    #Buscando informações para configurar o ambiente
    patient_arrival_interval, qt_employees, simulation_time = Util.get_environment_informations(message)

    random.seed(100)       
    env = simpy.Environment()

    #Criando médicos em enfermeiros
    employees = simpy.PreemptiveResource(env, capacity=qt_employees)    

    chegadas = env.process(Patient.arrival(env, employees, patient_arrival_interval))

    env.run(until=simulation_time)

    #Enviando retorno para o cliente
    Server.send_message(conn, "Fim do expediente")    
