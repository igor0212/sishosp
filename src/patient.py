import random
import names
from status import Status
from util import Util, File
from treatment import Treatment
from database import DataBase
 
class Patient:

    def insert(name, status_id):   
        try:                        
            query = 'INSERT INTO "Patient" (name, status_id) VALUES (\'{}\', {}) RETURNING id;'.format(name, status_id)                        
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

    def validate_treatment_time(env, status, simulation_time, now):
        treatment_time = Util.TREATMENT_TIME[status]
        time = simulation_time - now        
        if(treatment_time > time):
            return False
        return True

    def arrival(env, doctors, nurses, arrival_interval, day, simulation_time):        
        while True:

            #Configurando o intervalo em que os pacientes chegarão
            yield env.timeout(random.expovariate(1/arrival_interval))             

            #Gerar nome aleatório para paciente
            patient_name = names.get_full_name()            

            #Buscar, randomicamente, qual é o estado do paciente (1: LEVE, 2: MODERADO, 3: GRAVE, 4: GRAVÍSSIMO), qual sua prioridade e se o paciente precisa de atendimento imediato
            status_id, priority, is_urgent = Status.get()           

            now = env.now

            status = Util.PATIENT_STATUS_PT_BR[status_id]

            File.print(f"\n Paciente {patient_name} que esta em estado {status} chega ao hospital as {now:.2f}")

            if(not Patient.validate_treatment_time(env, status, simulation_time, now)):
                File.print(f"\n Paciente {patient_name} que esta em estado {status} nao podera ser atendido pois o tempo do expediente está acabando")
                continue

            patient_id = Patient.insert(patient_name, status_id)
            Treatment.insert(patient_id, 1, day, env.now)

            #Inicia o processo do atendimento
            env.process(Treatment.execute(env, patient_id, patient_name, status, priority, is_urgent, doctors, nurses, day))        
