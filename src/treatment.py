import random
from util import Util, File
from database import DataBase

class Treatment:
    def get_last_time(patient_id):   
        try:      
            query = """
                        select time 
                        from "Treatment" t 
                        where patient_id = {}
                        order by id
                    """.format(patient_id)            
            times = DataBase.select(query)                
            return times[len(times)-1]['time']
        except Exception as ex:
            return 0

    def get_time_spent(patient_id, flow_id, time):
        time_spent = 0        
        if(flow_id != 1):
            last_time = Treatment.get_last_time(patient_id)            
            if(last_time > 0):
                time_spent = round(time, 2) - round(last_time, 2)
        return time_spent    

    def insert(patient_id, flow_id, day, time):   
        try:
            time_spent = Treatment.get_time_spent(patient_id, flow_id, time)            
            query = 'INSERT INTO "Treatment" (patient_id, flow_id, day, time, time_spent) VALUES ({}, {}, {}, {}, {}) RETURNING id; \n'.format(patient_id, flow_id, day, time, time_spent)                        
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

    def get_total_time_spent_by_state(state_id):   
        try:      
            query = """
                        select sum(t."time_spent") as "time_spent" 
                        from "Treatment" t 
                        inner join "Patient" p ON t.patient_id = p.id 
                        inner join "State" s on p.state_id = s.id 
                        inner join "Flow" f on t.flow_id = f.id
                        where s.id = {}
                    """.format(state_id)            
            return DataBase.select(query)[0]['time_spent']
        except Exception as ex:
            error = "Patient - get_total_time_spent_by_state error: {} \n".format(ex)            
            raise Exception(error)

    def get_total_treatment_by_state(state_id):   
        try:      
            query = """
                        select COUNT (DISTINCT p."name")  
                        from "Treatment" t 
                        inner join "Patient" p ON t.patient_id = p.id 
                        inner join "State" s on p.state_id = s.id 
                        inner join "Flow" f on t.flow_id = f.id
                        where s.id = {}
                    """.format(state_id)            
            return DataBase.select(query)[0]['count']
        except Exception as ex:
            error = "Patient - get_total_treatment_by_state error: {} \n".format(ex)            
            raise Exception(error)  
        
    def get_treatment_avg_by_state(state_id):
        avg = 0
        total_time_spent = Treatment.get_total_time_spent_by_state(state_id)
        total_treatment = Treatment.get_total_treatment_by_state(state_id)
        if(total_treatment > 0):
            avg = total_time_spent/total_treatment
        return avg

