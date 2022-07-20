from database import DataBase
 
class Doctor:

  def insert(patient_id, name, time):   
        try:
            query = 'INSERT INTO "Doctor" (patient_id, name, time) VALUES ({}, \'{}\', {}) RETURNING id; \n'.format(patient_id, name, time)                        
            DataBase.insert(query)
        except Exception as ex:            
            error = "Treatment - insert error: {} \n".format(ex)            
            raise Exception(error)