from database import DataBase
 
class Employee:    

    def get_available(occupation_id=None):   
        try:      
            query = """
                        SELECT e.id AS employee_id, e."name" AS employee_name, o."name" AS occupation_name 
                        FROM "Employee" e
                        INNER JOIN "Occupation" o ON e.occupation_id = o.id 
                        WHERE e.block_id IS NULL                        
                    """
            if(occupation_id):
                query += " AND e.occupation_id = {}".format(occupation_id)

            query += " LIMIT 1"
            return DataBase.select(query)
        except Exception as ex:
            error = "Employee - get_available error: {} \n".format(ex)            
            raise Exception(error)            

    def update_block(id, block_id):
        try:
            query = 'UPDATE "Employee" SET block_id = {} WHERE id = {}'.format(block_id, id)
            DataBase.update(query)
        except Exception as ex:
            error = "Employee - update_block error: {} \n".format(ex)            
            raise Exception(error)

    def get_count_by_block(block_id):   
        try:      
            query = """
                        SELECT COUNT(*) 
                        FROM "Employee" e 
                        WHERE e.block_id = {}
                    """.format(block_id)            
            return DataBase.select(query)[0]['count']
        except Exception as ex:
            error = "Employee - get_count_by_block error: {} \n".format(ex)            
            raise Exception(error)    

    def get_by_block_id(block_id):   
        try:
            query = """
                        SELECT name AS employee_name, id AS employee_id
                        FROM "Employee" e                        
                        WHERE e.block_id = {}
                        LIMIT 1
                    """.format(block_id)

            return DataBase.select(query)           
            
        except Exception as ex:
            error = "Employee - get_by_block_id error: {} \n".format(ex)            
            raise Exception(error)    

    def remove(id):   
        try:
            query = 'UPDATE "Employee" SET block_id = NULL WHERE id = {}'.format(id)
            DataBase.update(query)            
        except Exception as ex:
            error = "Employee - remove error: {} \n".format(ex)            
            raise Exception(error)    