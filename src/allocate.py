from util import Util
from patient import Patient
from bed import Bed

class Allocate:

    def insert_patient(name, state_id):
        bed_id = Bed.get_available_bed_id()
        Patient.insert(name, state_id, bed_id)
        Bed.update_status_bed(bed_id)

    def allocate(message):
        try:
            name, state_id = Util.get_patient_information(message)
            Allocate.insert_patient(name, state_id)
            return "Paciente alocado com sucesso"
        except Exception as ex:
            return "Erro ao alocar paciente - {} \n".format(ex)        
