import psycopg2

class DataBase:
    def get_connection():
        host = 'localhost'
        database = 'sishosp'
        user = 'postgres'
        password = '@Eliane9455'    
        return psycopg2.connect(host=host, database=database, user=user, password=password)   

    def select(query, args=(), one=False):
        try:    
            conn = DataBase.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, args)
            r = [dict((cursor.description[i][0], value) \
                    for i, value in enumerate(row)) for row in cursor.fetchall()]
            cursor.connection.close()
            return (r[0] if r else None) if one else r
        except Exception as ex:
            error = "DataBase Error: Query select error - {} \n".format(ex)            
            raise Exception(error)            

    def insert(query):
        try:
            conn = DataBase.get_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()                        
            cursor.close()            
        except Exception as ex:
            error = "DataBase Error: Query insert error - {} \n".format(ex)
            raise Exception(error)
        finally:
            if conn is not None:
                conn.close()

    def update(query):
        try:
            conn = DataBase.get_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()                        
            cursor.close()            
        except Exception as ex:
            error = "DataBase Error: Query update error - {} \n".format(ex)            
            raise Exception(error)
        finally:
            if conn is not None:
                conn.close()       
