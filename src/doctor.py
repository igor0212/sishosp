from database import DataBase
 
class Doctor:
    def get_name(patient_id):   
        try:      
            query = """
                        select name 
                        from "Doctor" t 
                        where patient_id = {}                        
                    """.format(patient_id)            
            doctors = DataBase.select(query)                
            return doctors[len(doctors)-1]['name']
        except Exception as ex:
            return ""

    def insert(patient_id, name, time):   
        try:
            query = 'INSERT INTO "Doctor" (patient_id, name, time) VALUES ({}, \'{}\', {}) RETURNING id; \n'.format(patient_id, name, time)                        
            DataBase.insert(query)
        except Exception as ex:            
            error = "Treatment - insert error: {} \n".format(ex)            
            raise Exception(error)