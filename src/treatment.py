import random
import names
from util import Util, File

class Treatment:
    def execute(env, patient, state, priority, is_urgent, employees):        
        treatment_time = Util.TREATMENT_TIME[state]

        occupation = 'Enfermeiro' if state in ('Leve', 'Moderado') else 'Doutor'

        #Aloca um médico e realiza o atendimento do paciente
        with employees.request(priority=priority, preempt=is_urgent) as request:            
            yield request                
            File.print(f"\n {occupation} inicia o atendimento ao paciente %s que esta em estado %s as %4.1f" %(patient, state_name, env.now))

            try:
                #Configurando o tempo de duração de cada consulta
                yield env.timeout(random.expovariate(1/treatment_time))
                File.print(f"\n {occupation} finaliza o atendimento ao paciente %s que esta em estado %s as %4.1f" %(patient, state_name, env.now))                                    
            except:
                File.print(f"\n{occupation} interrompe o atendimento ao paciente %s que esta em estado %s as %4.1f" %(patient, state_name, env.now))    

