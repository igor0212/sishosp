import random
from util import Util, File
from database import DataBase

class Treatment:
    def insert(patient_id, flow_id, day, time):   
        try:                        
            query = 'INSERT INTO "Treatment" (patient_id, flow_id, day, time) VALUES ({}, {}, {}, {}) RETURNING id; \n'.format(patient_id, flow_id, day, time)                        
            DataBase.insert(query)
        except Exception as ex:            
            error = "Treatment - insert error: {} \n".format(ex)            
            raise Exception(error)

    def execute(env, patient_id, patient_name, state, priority, is_urgent, doctors, nurses, day):        
        treatment_time = Util.TREATMENT_TIME[state]       

        #Aloca um médico e realiza o atendimento do paciente
        with doctors.request(priority=priority, preempt=is_urgent) as request:            
            yield request                
            File.print(f"\n Paciente {patient_name} que esta em estado {state} tem o seu atendimento iniciado as {env.now:.2f}")
            Treatment.insert(patient_id, 2, day, env.now)

            try:
                #Configurando o tempo de duração de cada consulta
                yield env.timeout(random.expovariate(1/treatment_time))                
                File.print(f"\n Paciente {patient_name} que esta em estado {state} tem o seu atendimento finalizado as {env.now:.2f}")
                Treatment.insert(patient_id, 3, day, env.now)
            except:                
                File.print(f"\n Paciente {patient_name} que esta em estado {state} tem o seu atendimento interrompido as {env.now:.2f}")
                Treatment.insert(patient_id, 4, day, env.now)

