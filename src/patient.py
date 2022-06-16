from database import DataBase
 
class Patient:

    def insert(name, state_id, bed_id):   
        try:                        
            query = 'INSERT INTO "Patient" (name, state_id, bed_id) VALUES (\'{}\', {}, {}); \n'.format(name, state_id, bed_id)                        
            DataBase.insert(query)
        except Exception as ex:            
            error = "Patient - insert error: {} \n".format(ex)            
            raise Exception(error)