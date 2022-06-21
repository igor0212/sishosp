import psycopg2

class DataBase:
    def get_connection():
        host = 'localhost'
        database = 'sishosp'
        user = 'postgres'
        password = '@Eliane9455'    
        return psycopg2.connect(host=host, database=database, user=user, password=password)   

    def insert(query):
        try:
            conn = DataBase.get_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            new_id = cursor.fetchone()[0]            
            conn.commit()
            cursor.close()            
            return new_id
        except Exception as ex:
            error = "DataBase Error: Query insert error - {} \n".format(ex)
            raise Exception(error)
        finally:
            if conn is not None:
                conn.close()
