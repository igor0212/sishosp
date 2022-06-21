from state import State
from util import File
from treatment import Treatment
import random
import names
 
class Patient:

    def arrival(env, employees, arrival_interval):        
        while True:

            #Configurando o intervalo em que os pacientes chegarão
            yield env.timeout(random.expovariate(1/arrival_interval))             

            #Gerar nome aleatório para paciente
            patient = names.get_full_name()            

            #Buscar, randomicamente, qual é o estado do paciente (1: LEVE, 2: MODERADO, 3: GRAVE, 4: GRAVÍSSIMO), qual sua prioridade e se o paciente precisa de atendimento imediato
            state, priority, is_urgent = State.get()                        

            File.print(f"\n Paciente {patient} que esta em estado {state} chega ao hospital as {env.now:.2f}")

            #Inicia o processo do atendimento
            env.process(Treatment.execute(env, patient, state, priority, is_urgent, employees))        
