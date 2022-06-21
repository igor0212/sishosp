import random
from util import Util, File

class Treatment:
    def execute(env, patient, state, priority, is_urgent, employees):        
        treatment_time = Util.TREATMENT_TIME[state]       

        #Aloca um médico e realiza o atendimento do paciente
        with employees.request(priority=priority, preempt=is_urgent) as request:            
            yield request                
            File.print(f"\n Paciente {patient} que esta em estado {state} tem o seu atendimento iniciado as {env.now:.2f}")

            try:
                #Configurando o tempo de duração de cada consulta
                yield env.timeout(random.expovariate(1/treatment_time))                
                File.print(f"\n Paciente {patient} que esta em estado {state} tem o seu atendimento finalizado as {env.now:.2f}")
            except:                
                File.print(f"\n Paciente {patient} que esta em estado {state} tem o seu atendimento interrompido as {env.now:.2f}")

