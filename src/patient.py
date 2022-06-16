from database import DataBase
 
class Patient:

    def insert(name, state_id, bed_id, is_waiting):   
        try:            
            if(bed_id):
                query = 'INSERT INTO public."Patient"(name, state_id, bed_id, is_waiting) VALUES (\'{}\', {}, {}, {}); \n'.format(name, state_id, bed_id, is_waiting)            
            else:
                query = 'INSERT INTO public."Patient"(name, state_id, is_waiting) VALUES (\'{}\', {}, {}); \n'.format(name, state_id, is_waiting)            
            DataBase.insert(query)
        except Exception as ex:            
            error = "Patient - insert error: {} \n".format(ex)            
            raise Exception(error)