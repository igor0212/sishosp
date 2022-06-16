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