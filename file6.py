import json
import pyodbc



server = 'database-1.czewk2q0eqo4.ap-south-1.rds.amazonaws.com'
database = 'offline13'
username = 'admin'
password = 'Admin#2110'

def database_connection():
    try:

        conn = pyodbc.connect(
            f'DRIVER={{ODBC Driver 18 for SQL Server}};'
            f'SERVER={server},1433;'
            f'DATABASE={database};'
            f'UID={username};'
            f'PWD={password};'
            'TrustServerCertificate=yes;')
        
        cur=conn.cursor()

        return conn,cur
    
    except Exception as e:
        print(e)

def insert_data_into_mssql(conn,cur):
    try:
        query="insert into emp (id,name,city) values(101,'harsh','akola')"
        cur.execute(query)
        conn.commit()
    except Exception as e:
        print(e)


def lambda_handler(event, context):
    try:

        conn,cur=database_connection()
        insert_data_into_mssql(conn, cur)
        cur.close()
        conn.close()
    
    except Exception as e:
        print(e)

