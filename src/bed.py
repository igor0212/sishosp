from database import DataBase
 
class Bed:    

    def get_available(state_id):   
        try:      
            query = """
                        SELECT b.id as bed_id, b."name" as bed_name, b2.id as block_id, b2."name" block_name
                        FROM "Bed" b
                        INNER JOIN "Block" b2 ON b.block_id = b2.id 
                        WHERE b.is_available = true AND b2.state_id = {}
                        LIMIT 1
                    """.format(state_id)
            return DataBase.select(query)
        except Exception as ex:
            error = "Bed - get_available error: {} \n".format(ex)            
            raise Exception(error)            

    def get_available_other_block():   
        try:                      
            query = """
                        SELECT b.id as bed_id, b."name" as bed_name, b2.id as block_id, b2."name" block_name
                        FROM "Bed" b
                        INNER JOIN "Block" b2 ON b.block_id = b2.id 
                        WHERE b.is_available = true AND b2.state_id in (1, 2, 3)
                        ORDER BY b2.state_id desc
                        LIMIT 1
                    """
            return DataBase.select(query)
        except Exception as ex:
            error = "Bed - get_available_other_block error: {} \n".format(ex)            
            raise Exception(error)            

    def update_status(id, is_available=False):
        try:
            query = 'UPDATE "Bed" SET is_available = {} WHERE id = {}'.format(is_available, id)
            DataBase.update(query)
        except Exception as ex:
            error = "Bed - update_status error: {} \n".format(ex)            
            raise Exception(error)