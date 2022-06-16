from util import Util
from patient import Patient
from bed import Bed
from employee import Employee

class Allocate:

    def allocate_patient(message):
        try:
            print("\nAlocando paciente ao leito...")

            #Buscar informações do paciente
            patient_name, state_id = Util.get_patient_information(message)

            #Buscar leito disponível
            bed = Bed.get_available(state_id)
            
            #Não possui leito disponível
            if(not bed):
                print("Paciente {} à espera de um leito.".format(patient_name))

                #Verificar se paciente pode aguardar leito
                if(Util.PATIENT_STATE[state_id] in ('Ligh', 'Moderate')):
                    print("Paciente {} pode aguardar pois o seu estado permite.".format(patient_name))
                    return

                #Buscar outro leito para paciente
                bed = Allocate.get_another_bed(patient_name)

            bed_id = bed[0]['bed_id']
            bed_name = bed[0]['bed_name']
            block_id = bed[0]['block_id']
            block_name = bed[0]['block_name']
            
            #Cadastrar paciente
            Patient.insert(patient_name, state_id, bed_id)

            #Tornar leito indisponível            
            Bed.update_status(bed_id)
            print("Paciente {} alocado(a) com sucesso ao leito {} do bloco {}.\n".format(patient_name, bed_name, block_name))
            return block_id, block_name
            
        except Exception as ex:
            error = "Erro ao alocar paciente - {} \n".format(ex)
            raise Exception(error)
    
    def get_another_bed(patient_name):
        
        #Buscar leito de outro bloco
        bed = Bed.get_available_other_block()
        if(not bed):
            #Remover do leito um paciente que está em estado leve            
            print("Hospital com capacidade máxima. Removendo um paciente em estado leve")            
            
            patient = Patient.get_by_state_id(1)            
            removed_patient_id =  patient[0]['patient_id']
            removed_bed_id =  patient[0]['bed_id']
            removed_patient_name =  patient[0]['patient_name']

            print("Paciente {} será removido de seu leito.".format(removed_patient_name))

            Patient.remove_bed(removed_patient_id)
            Bed.update_status(removed_bed_id, True)
            
            #Buscar leito que fora esvaziado
            bed = Bed.get_available_other_block()

            if(not bed):
                raise Exception("Erro ao buscar leito depois de removido") 

        print("Paciente {} precisará ocupar um leito de outro bloco.".format(patient_name))
        
        return bed

    def get_another_employee():

        #Buscar profissional independente do cargo
        employee = Employee.get_available()
        
        if(not employee):
            #Transferir um profissional do bloco A para o bloco necessitado
            print("Todos os profissionais estão alocados. Transferindo um profissional do bloco A")            
            
            removed_employee = Employee.get_by_block_id(1)            
            removed_employee_id =  removed_employee[0]['employee_id']            
            removed_employee_name =  removed_employee[0]['employee_name']

            print("Profissional {} será removido do bloco A.".format(removed_employee_name))

            Employee.remove(removed_employee_id)            
            
            #Buscar profissional que fora desalocado
            employee = Employee.get_available()

            if(not employee):
                raise Exception("Erro ao buscar profissional depois de removido")         
        
        return employee


    def allocate_employee(block_id, block_name):
        try:
            #Verificar se alocação de profissional é necessária
            if(not Allocate.check_allocate_is_necessary(block_id, block_name)):
                print("Alocação de profissional não é necessária pois já existem funcionários suficientes no bloco {}".format(block_name))
                return

            print("\nAlocando profissional ao bloco...")
            #Verificar em qual bloco o paciente foi alocado para enviar médico ou enfermeiro
            occupation_id = 1
            if(block_name in ('A', 'B')):
                occupation_id = 2

            #Buscar profissional
            employee = Employee.get_available(occupation_id)

            if(not employee):

                #Verificar se bloco pode aguardar até a chegada de outro profissional
                if(block_name in ('A', 'B')):
                    print("Bloco {} pode aguardar pois o seu estado permite.".format(block_name))
                    return

                #Buscar profissional de outro bloco
                employee = Allocate.get_another_employee()

            #Alocar profissional ao bloco
            employee_id = employee[0]['employee_id']
            employee_name = employee[0]['employee_name']
            occupation_name = employee[0]['occupation_name']
            Employee.update_status(employee_id, block_id)
            print("{} {} alocado(a) com sucesso no bloco {}.\n".format(occupation_name, employee_name, block_name))
        except Exception as ex:
            error = "Erro ao alocar profissional - {} \n".format(ex)
            raise Exception(error)            

    def check_allocate_is_necessary(block_id, block_name):
        count_patient = Patient.get_count_by_block(block_id)
        count_employee = Employee.get_count_by_block(block_id)
        qt_max_allowed = Util.QT_EMPLOYEES_BY_BLOCK[block_name]

        if(count_employee == 0):
            return True
        
        result = count_patient/count_employee
        if(result > qt_max_allowed):
            return True

        return False

    def allocate(message):
        try:            
            #Alocar paciente ao leito
            block_id, block_name = Allocate.allocate_patient(message)            
            
            if(not block_id or not block_name):
                raise Exception("Bloco não encontrado.")             

            #Alocar profissional ao bloco
            Allocate.allocate_employee(block_id, block_name)

            return "Fim da operação"
        except Exception as ex:
            return "Erro ao fazer alocações - {} \n".format(ex)        
