from database import DataBase
 
class Bed:    

    def get_available_bed():   
        try:      
            query = 'select id from "Bed" where is_available = true limit 1'            
            return DataBase.select(query)
        except Exception as ex:
            error = "Bed - get_available_bed error: {} \n".format(ex)            
            raise Exception(error)            

    def update_status_bed(bed_id):
        try:
            query = 'update "Bed" set is_available = false where id = {}'.format(bed_id)
            DataBase.update(query)
        except Exception as ex:
            error = "Bed - update_status_bed error: {} \n".format(ex)            
            raise Exception(error)