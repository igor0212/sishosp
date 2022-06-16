from util import Util
from patient import Patient
from bed import Bed

class Allocate:

    def allocate_patient(message):
        try:            
            name, state_id = Util.get_patient_information(message)
            bed = Bed.get_available_bed()
            is_waiting = True
            bed_id = None

            if(bed):
                is_waiting = False
                bed_id = bed[0]['id']

            Patient.insert(name, state_id, bed_id, is_waiting)

            if(bed_id):
                Bed.update_status_bed(bed_id)
                return "Paciente alocado com sucesso"

            return "Paciente à espera de um leito"
        except:
            return "Erro ao inserir paciente - {} \n".format(ex)        


    def allocate(message):
        try:            
            allocate_patient = Allocate.allocate_patient(message)            
            print(allocate_patient)

            return "Fim da operação"
        except Exception as ex:
            return "Erro ao alocar paciente - {} \n".format(ex)        
