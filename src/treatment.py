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

    def execute(env, patient_id, patient_name, status, priority, is_urgent, doctors, nurses, day, treatment_time=None):        
        treatment_time_status = Util.TREATMENT_TIME[status]

        #Médico só atenderá paciente nos estados Grave e Gravíssimo
        if(status in ('Grave', 'Gravissimo', 'Moderado')):                
            #Aloca um médico e realiza o atendimento do paciente
            with doctors.request(priority=priority, preempt=is_urgent) as request:                
                yield request
                treatment_start = env.now
                File.print(f"\n Paciente {patient_name} que esta em estado {status} tem o seu atendimento iniciado pelo medico as {env.now:.2f}")
                Treatment.insert(patient_id, 2, day, env.now)

                try:
                    #Configurando o tempo de duração de cada consulta
                    if not treatment_time:
                        treatment_time = treatment_time_status                    
                    yield env.timeout(treatment_time)
                    File.print(f"\n Paciente {patient_name} que esta em estado {status} tem o seu atendimento finalizado pelo medico as {env.now:.2f}")
                    Treatment.insert(patient_id, 3, day, env.now)
                except:
                    treatment_time -= env.now-treatment_start 
                    File.print(f"\n Paciente {patient_name} que esta em estado {status} tem o seu atendimento interrompido pelo medico as {env.now:.2f}")
                    File.print(f"\n Paciente {patient_name} que esta em estado {status} ainda precisa de {treatment_time:.2f} de atendimento")
                    Treatment.insert(patient_id, 4, day, env.now)

                    #Aumenta a prioridade de quem teve o seu atendimento interrompido para um que acabou de chegar (com o mesmo grau)
                    priority -= 0.01
                    env.process(Treatment.execute(env, patient_id, patient_name, status, priority, is_urgent, doctors, nurses, day, treatment_time)) 
        else:        
            #Aloca um enfermeiro e realiza o atendimento do paciente
            with nurses.request(priority=priority) as request:
                yield request
                treatment_start = env.now
                File.print(f"\n Paciente {patient_name} que esta em estado {status} tem o seu atendimento iniciado pelo enfermeiro as {env.now:.2f}")
                Treatment.insert(patient_id, 2, day, env.now)

                try:
                    #Configurando o tempo de duração de cada consulta                    
                    if not treatment_time:
                        treatment_time = random.expovariate(1/treatment_time_status)
                    yield env.timeout(treatment_time)
                    File.print(f"\n Paciente {patient_name} que esta em estado {status} tem o seu atendimento finalizado pelo enfermeiro as {env.now:.2f}")                    
                    Treatment.insert(patient_id, 3, day, env.now)
                except:
                    treatment_time -= env.now-treatment_start 
                    File.print(f"\n Paciente {patient_name} que esta em estado {status} tem o seu atendimento interrompido pelo enfermeiro as {env.now:.2f}")
                    File.print(f"\n Paciente {patient_name} que esta em estado {status} ainda precisa de {treatment_time:.2f} de atendimento")
                    Treatment.insert(patient_id, 4, day, env.now)  

                    #Aumenta a prioridade de quem teve o seu atendimento interrompido para um que acabou de chegar (com o mesmo grau)
                    priority -= 0.01
                    env.process(Treatment.execute(env, patient_id, patient_name, status, priority, is_urgent, doctors, nurses, day, treatment_time)) 

    def get_total_time_spent_by_status(status_id, day):   
        try:      
            query = """
                        select sum(t."time_spent") as "time_spent" 
                        from "Treatment" t 
                        inner join "Patient" p ON t.patient_id = p.id 
                        inner join "Status" s on p.status_id = s.id 
                        inner join "Flow" f on t.flow_id = f.id
                        where s.id = {} and t.day = {}
                    """.format(status_id, day)            
            return DataBase.select(query)[0]['time_spent']
        except Exception as ex:
            error = "Patient - get_total_time_spent_by_status error: {} \n".format(ex)            
            raise Exception(error)

    def get_total_treatment_by_status(status_id, day):   
        try:      
            query = """
                        select COUNT (DISTINCT p."name")  
                        from "Treatment" t 
                        inner join "Patient" p ON t.patient_id = p.id 
                        inner join "Status" s on p.status_id = s.id 
                        inner join "Flow" f on t.flow_id = f.id
                        where s.id = {} and t.day = {}
                    """.format(status_id, day)            
            return DataBase.select(query)[0]['count']
        except Exception as ex:
            error = "Patient - get_total_treatment_by_status error: {} \n".format(ex)            
            raise Exception(error)  
        
    def get_treatment_avg_by_status(status_id, day):
        avg = 0
        total_time_spent = Treatment.get_total_time_spent_by_status(status_id, day)
        total_treatment = Treatment.get_total_treatment_by_status(status_id, day)
        if(total_treatment > 0):
            avg = total_time_spent/total_treatment
        return avg

    def get_total_treatment_canceled(status_id, day):   
        try:      
            query = """
                        select count(distinct(patient_id))
                        from "Treatment" t 
                        inner join "Patient" p ON t.patient_id = p.id 
                        inner join "Status" s on p.status_id = s.id
                        where s.id = {} and t.flow_id = 4 and t.day = {}
                    """.format(status_id, day)            
            return DataBase.select(query)[0]['count']
        except Exception as ex:
            error = "Patient - get_total_treatment_canceled error: {} \n".format(ex)            
            raise Exception(error)  

    def get_total_patient_by_status(status_id, day):   
        try:      
            query = """
                        select count(*)                         
                        from "Treatment" t 
                        inner join "Patient" p ON t.patient_id = p.id 
                        inner join "Status" s on p.status_id = s.id
                        inner join "Flow" f on t.flow_id = f.id 
                        where s.id = {} and t.flow_id = 3 and t.day = {}
                    """.format(status_id, day)            
            return DataBase.select(query)[0]['count']
        except Exception as ex:
            error = "Patient - get_total_patient_by_status error: {} \n".format(ex)            
            raise Exception(error)  

    def get_patient_id_by_day(status_id, day):   
        try:      
            query = """
                        select distinct (p."id") as patient_id
                        from "Treatment" t 
                        inner join "Patient" p ON t.patient_id = p.id 
                        inner join "Status" s on p.status_id = s.id
                        where s.id = {} and t.day = {}
                    """.format(status_id, day)            
            return DataBase.select(query)
        except Exception as ex:
            error = "Patient - get_patient_id_by_day error: {} \n".format(ex)            
            raise Exception(error)  

    def get_treatment_undone_by_id(patient_id):   
        try:      
            query = """
                        select t.flow_id 
                        from "Treatment" t 
                        inner join "Patient" p ON t.patient_id = p.id
                        where p.id = {}
                    """.format(patient_id)            
            return DataBase.select(query)
        except Exception as ex:
            error = "Patient - get_treatment_undone_by_id error: {} \n".format(ex)            
            raise Exception(error)  

    def get_treatment_undone(status_id, day):
        patients = Treatment.get_patient_id_by_day(status_id, day)        
        total = 0
        for patient in patients:
            patient_id = patient['patient_id']
            flows = Treatment.get_treatment_undone_by_id(patient_id)            
            if({'flow_id': 3} not in flows):
                total += 1

        return total   




