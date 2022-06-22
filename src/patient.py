import random
import names
from state import State
from util import Util, File
from treatment import Treatment
from database import DataBase
 
class Patient:

    def insert(name, state_id):   
        try:                        
            query = 'INSERT INTO "Patient" (name, state_id) VALUES (\'{}\', {}) RETURNING id;'.format(name, state_id)                        
            return DataBase.insert(query)
        except Exception as ex:            
            error = "Patient - insert error: {} \n".format(ex)            
            raise Exception(error)

    def get_total_by_day(day):   
        try:      
            query = """
                        select count(distinct(patient_id))
                        from "Treatment" t
                        WHERE t.day = {}
                    """.format(day)            
            return DataBase.select(query)[0]['count']
        except Exception as ex:
            error = "Patient - get_total_by_day error: {} \n".format(ex)            
            raise Exception(error)   

    
    def get_total_consulted_by_day(day):   
        try:      
            query = """
                        select count(distinct(patient_id))
                        from "Treatment" t
                        WHERE t.day = {} and t.flow_id = 3
                    """.format(day)            
            return DataBase.select(query)[0]['count']
        except Exception as ex:
            error = "Patient - get_total_consulted_by_day error: {} \n".format(ex)            
            raise Exception(error)   

    def arrival(env, doctors, nurses, arrival_interval, day):        
        while True:

            #Configurando o intervalo em que os pacientes chegarão
            yield env.timeout(random.expovariate(1/arrival_interval))             

            #Gerar nome aleatório para paciente
            patient_name = names.get_full_name()            

            #Buscar, randomicamente, qual é o estado do paciente (1: LEVE, 2: MODERADO, 3: GRAVE, 4: GRAVÍSSIMO), qual sua prioridade e se o paciente precisa de atendimento imediato
            state_id, priority, is_urgent = State.get()                        

            state = Util.PATIENT_STATE_PT_BR[state_id]

            File.print(f"\n Paciente {patient_name} que esta em estado {state} chega ao hospital as {env.now:.2f}")
            patient_id = Patient.insert(patient_name, state_id)
            Treatment.insert(patient_id, 1, day, env.now)

            #Inicia o processo do atendimento
            env.process(Treatment.execute(env, patient_id, patient_name, state, priority, is_urgent, doctors, nurses, day))        
