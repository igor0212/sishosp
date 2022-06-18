from database import DataBase
 
class Patient:

    def insert(name, state_id, bed_id):   
        try:                        
            query = 'INSERT INTO "Patient" (name, state_id, bed_id) VALUES (\'{}\', {}, {}); \n'.format(name, state_id, bed_id)                        
            DataBase.insert(query)
        except Exception as ex:            
            error = "Patient - insert error: {} \n".format(ex)            
            raise Exception(error)

    def get_count_by_block(block_id):   
        try:      
            query = """
                        SELECT COUNT(*) 
                        FROM "Patient" p
                        INNER JOIN "Bed" b ON p.bed_id = b.id 
                        WHERE b.block_id = {}
                    """.format(block_id)            
            return DataBase.select(query)[0]['count']
        except Exception as ex:
            error = "Patient - get_count_by_block error: {} \n".format(ex)            
            raise Exception(error)    

    def get_by_state_id(state_id):   
        try:
            query = """
                        SELECT name AS patient_name, bed_id, id AS patient_id
                        FROM "Patient" p                        
                        WHERE p.state_id = {} AND bed_id IS NOT NULL
                        LIMIT 1
                    """.format(state_id)

            return DataBase.select(query)           
            
        except Exception as ex:
            error = "Patient - get_by_state_id error: {} \n".format(ex)            
            raise Exception(error)    

    def remove_bed(id):   
        try:
            query = 'UPDATE "Patient" SET bed_id = NULL, is_waiting = true WHERE id = {}'.format(id)
            DataBase.update(query)            
        except Exception as ex:
            error = "Patient - remove_bed error: {} \n".format(ex)            
            raise Exception(error)    

    def update_state(id, state_id, bed_id):   
        try:
            query = 'UPDATE "Patient" SET bed_id = {}, state_id = {} WHERE id = {}'.format(bed_id, state_id, id)
            DataBase.update(query)            
        except Exception as ex:
            error = "Patient - update_state error: {} \n".format(ex)            
            raise Exception(error)    