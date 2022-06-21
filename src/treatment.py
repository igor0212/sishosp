import random
import names
from util import Util, File

class Treatment:
    def execute(env, patient, state_name, priority, is_urgent, doctors, nurses):        
        treatment_time = Util.TREATMENT_TIME[state_name]

        #Verificar qual profissional irá atender o paciente
        if(state_name in ('Leve', 'Moderado')):
            #Aloca um enfermeiro e realiza o atendimento do paciente
            with nurses.request(priority=priority) as request:            
                yield request
                #Gerar nome aleatório para o enfermeiro
                nurse_name = names.get_full_name()
                File.print("\nEnfermeiro %s inicia o atendimento ao paciente %s que esta em estado %s as %4.1f" %(nurse_name, patient, state_name, env.now))
                try:
                    #Configurando o tempo de duração de cada consulta
                    yield env.timeout(random.expovariate(1/treatment_time))
                    File.print("\nEnfermeiro %s finaliza o atendimento ao paciente %s que esta em estado %s as %4.1f" %(nurse_name, patient, state_name, env.now))                
                except:
                    File.print("\nEnfermeiro %s interrompe o atendimento ao paciente %s que esta em estado %s as %4.1f" %(nurse_name, patient, state_name, env.now))         
        else:
            #Aloca um médico e realiza o atendimento do paciente
            with doctors.request(priority=priority, preempt=is_urgent) as request:            
                yield request
                #Gerar nome aleatório para o doutor
                doctor_name = names.get_full_name()
                File.print("\nDoutor %s inicia o atendimento ao paciente %s que esta em estado %s as %4.1f" %(doctor_name, patient, state_name, env.now))

                try:
                    #Configurando o tempo de duração de cada consulta
                    yield env.timeout(random.expovariate(1/treatment_time))
                    File.print("\nDoutor %s finaliza o atendimento ao paciente %s que esta em estado %s as %4.1f" %(doctor_name, patient, state_name, env.now))                                    
                except:
                    File.print("\nDoutor %s interrompe o atendimento ao paciente %s que esta em estado %s as %4.1f" %(doctor_name, patient, state_name, env.now))    

