import json
import boto3
import pymysql
import csv 

client=boto3.client('s3')
host='off-database-13.czewk2q0eqo4.ap-south-1.rds.amazonaws.com'
port=3306
username='admin'
password='Admin#2110'
dbname='offline13'
Bucket_name='off-database-files'
filename='company_employees.csv'

def database_connection():
    try:

        conn=pymysql.connect(host=host,port=port,user=username,password=password,db=dbname)
        cur=conn.cursor()

        return conn,cur

    except Exception as e:
        print(e)

def download_file_from_s3():
    try:
    
        client.download_file('{}'.format(Bucket_name),'{}'.format(filename), '/tmp/{}'.format(filename))
    
    except Exception as e:
        print(e)

def read_csv_file():
    try:

        with open ('/tmp/{}'.format(filename)) as fp:
            r=csv.DictReader(fp)
            data=list(r)
            return data

    except Exception as e:
        print(e)

def insert_data_into_db(conn,cur,data):
    try:
        for i in data:
            query="insert into emp values('{}','{}',{},'{}','{}','{}',{},{},'{}','{}',{},'{}')".format(
                                            (i['EmployeeID']),(i['Name']),(i['Age']),
                                            (i['Gender']),(i['Department']),(i['Designation']),
                                            (i['Salary']),(i['Experience']),(i['City']),
                                            (i['JoinDate']),(i['ManagerID']),(i['Status']))
            cur.execute(query)
            conn.commit()
    
    except Exception as e:
        print(e)

def lambda_handler(event, context):
    try:

        conn,cur=database_connection()
        download_file_from_s3()
        data=read_csv_file()
        insert_data_into_db(conn,cur,data)
        cur.close()
        conn.close()

    except Exception as e:
        print(e)
  
  