from util import Server
from util import Util, File
from patient import Patient
from treatment import Treatment
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
    patient_arrival_interval, qt_doctors, qt_nurses, simulation_time = Util.get_environment_informations(message)

    File.print(f"\n\n Hospital ira operar em {simulation_time} unidades de tempo, com pacientes chegando em um intervalo de {patient_arrival_interval} unidades de tempo e possuindo {qt_doctors} medicos e {qt_nurses} enfermeiros no dia {day}.\n")

    random.seed(100)       
    env = simpy.Environment()

    #Criando médicos
    doctors = simpy.PreemptiveResource(env, capacity=qt_doctors) 

    #Criando enfermeiros
    nurses = simpy.PreemptiveResource(env, capacity=qt_nurses)    

    env.process(Patient.arrival(env, doctors, nurses, patient_arrival_interval, day))

    env.run(until=simulation_time) 

    avg_state_1 = Treatment.get_treatment_avg_by_state(1, day)
    avg_state_2 = Treatment.get_treatment_avg_by_state(2, day)
    avg_state_3 = Treatment.get_treatment_avg_by_state(3, day)
    avg_state_4 = Treatment.get_treatment_avg_by_state(4, day)

    response = f"""
                Fim do expediente do dia {day}
                Total de pacientes que foram ao hospital:                                    {Patient.get_total_by_day(day)}
                Total de pacientes que foram atendidos (consulta finalizada):                {Patient.get_total_consulted_by_day(day)}

                Total de pacientes LEVES que foram atendidos (consulta finalizada):          {Treatment.get_total_patient_by_state(1, day)}
                Total de pacientes MODERADOS que foram atendidos (consulta finalizada):      {Treatment.get_total_patient_by_state(2, day)}
                Total de pacientes GRAVES que foram atendidos (consulta finalizada):         {Treatment.get_total_patient_by_state(3, day)}
                Total de pacientes GRAVÍSSIMOS que foram atendidos (consulta finalizada):    {Treatment.get_total_patient_by_state(4, day)}                

                Total de pacientes LEVES que não tiveram o seu atendimento concluído:        {Treatment.get_treatment_undone(1, day)}
                Total de pacientes MODERADOS que não tiveram o seu atendimento concluído:    {Treatment.get_treatment_undone(2, day)}
                Total de pacientes GRAVES que não tiveram o seu atendimento concluído:       {Treatment.get_treatment_undone(3, day)}
                Total de pacientes GRAVÍSSIMOS que não tiveram o seu atendimento concluído:  {Treatment.get_treatment_undone(4, day)}

                Total de pacientes LEVES que tiveram o seu atendimento interrompido:         {Treatment.get_total_treatment_canceled(1, day)}
                Total de pacientes MODERADOS que tiveram o seu atendimento interrompido:     {Treatment.get_total_treatment_canceled(2, day)}
                Total de pacientes GRAVES que tiveram o seu atendimento interrompido:        {Treatment.get_total_treatment_canceled(3, day)}
                Total de pacientes GRAVÍSSIMOS que tiveram o seu atendimento interrompido:   {Treatment.get_total_treatment_canceled(4, day)}

                Média do tempo gasto nos atendimentos LEVES:                                 {avg_state_1:.2f} - {"Abaixo da média" if avg_state_1 < Util.TREATMENT_TIME['Leve'] else "Acima da média" }
                Média do tempo gasto nos atendimentos MODERADOS:                             {avg_state_2:.2f} - {"Abaixo da média" if avg_state_2 < Util.TREATMENT_TIME['Moderado'] else "Acima da média" }
                Média do tempo gasto nos atendimentos GRAVES:                                {avg_state_3:.2f} - {"Abaixo da média" if avg_state_3 < Util.TREATMENT_TIME['Grave'] else "Acima da média" }
                Média do tempo gasto nos atendimentos GRAVÍSSIMOS:                           {avg_state_4:.2f} - {"Abaixo da média" if avg_state_4 < Util.TREATMENT_TIME['Gravissimo'] else "Acima da média" }
                """

    #Enviando retorno para o cliente
    Server.send_message(conn, response)    
