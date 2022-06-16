from database import DataBase
 
class Employee:    

    def get_available(occupation_id):   
        try:      
            query = """
                        SELECT e.id AS employee_id, e."name" AS employee_name, o."name" AS occupation_name 
                        FROM "Employee" e
                        INNER JOIN "Occupation" o ON e.occupation_id = o.id 
                        WHERE e.block_id IS NULL AND e.occupation_id = {}
                        LIMIT 1
                    """.format(occupation_id)            
            return DataBase.select(query)
        except Exception as ex:
            error = "Employee - get_available error: {} \n".format(ex)            
            raise Exception(error)            

    def update_status(id, block_id):
        try:
            query = 'UPDATE "Employee" SET block_id = {} WHERE id = {}'.format(block_id, id)
            DataBase.update(query)
        except Exception as ex:
            error = "Employee - update_status error: {} \n".format(ex)            
            raise Exception(error)