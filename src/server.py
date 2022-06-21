from util import Server
from util import Util, File
from patient import Patient
import simpy
import random

print('Aguardando conexão')
conn, ender = Server.create_server()
day = 0

while True:

    #Setando o primeiro dia de expediente    
    day += 1

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

    File.print(f"\n\n Hospital ira operar em {simulation_time} unidades de medida, com pacientes chegando em um intervalo de {patient_arrival_interval} unidades de medida e possuindo {qt_employees} funcionarios no dia {day}.\n")

    random.seed(100)       
    env = simpy.Environment()

    #Criando médicos em enfermeiros
    employees = simpy.PreemptiveResource(env, capacity=qt_employees)    

    env.process(Patient.arrival(env, employees, patient_arrival_interval, day))

    env.run(until=simulation_time) 

    response = f"""
                Fim do expediente
                Total de pacientes que adentraram o hospital no dia {day}: {Patient.get_total_by_day(day)}
                Total de pacientes que foram atendidos (consulta finalizada) no dia {day}: {Patient.get_total_consulted_by_day(day)}                
                """

    #Enviando retorno para o cliente
    Server.send_message(conn, response)    
