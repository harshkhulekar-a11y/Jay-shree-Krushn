import json
import boto3
import csv
import pymysql 
import os 

client=boto3.client('s3')
host='database-1.czewk2q0eqo4.ap-south-1.rds.amazonaws.com'
port=3306
username='admin'
password='Admin#2110'
dbname='offline13'

def database_connection():
    try:

        conn=pymysql.connect(host=host,port=port,user=username,password=password,db=dbname)
        cur=conn.cursor()
        return conn,cur

    except Exception as e:
        print(e)

def download_files(Bucket_name,Input_files):
    try:

        client.download_file('{}'.format(Bucket_name), '{}'.format(Input_files), '/tmp/{}'.format(Input_files))

    except Exception as e:
        print(e)

def read_csv_file(Input_files):
    try:

        with open('/tmp/{}'.format(Input_files),'r')as fp:
            r=csv.DictReader(fp)
            data=list(r)
            return data

    except Exception as e:
        print(e)

def get_table_name(Input_files):
    try:
        base_name = os.path.basename(Input_files) # filename alg krke dega
        table_name = os.path.splitext(base_name)[0] # isme se .csv nikal dega
        table_name = ''.join(ch if ch.isalnum() or ch == '_' else '_' for ch in table_name)
        if table_name and table_name[0].isdigit():
            table_name = '_' + table_name
        return table_name
    
    except Exception as e:
        print(e)

def insert_file_into_db(conn,cur,table_name,data):
    try:

        columns = list(data[0].keys()) # column name dega 
        columns_def = ', '.join(['`{}` TEXT'.format(col) for col in columns]) # column ke aage text lgayega
        create_query = "CREATE TABLE IF NOT EXISTS `{}` ({})".format(table_name, columns_def)
        cur.execute(create_query)
        conn.commit()

        for i in data:

            column=','.join(i.keys()) # keys seprate krega 
            values=','.join(['%s'] * len(i))

            query1="insert into `{}` ({}) values ({})".format(table_name,column,values)
            cur.execute(query1, list(i.values()))
            conn.commit()

    except Exception as e:
        print(e)

def lambda_handler(event, context):
    try:
        
        Bucket_name=event["Records"][0]["s3"]["bucket"]["name"]
        Input_files=event["Records"][0]["s3"]["object"]["key"]
        conn,cur=database_connection()
        download_files(Bucket_name,Input_files)
        data=read_csv_file(Input_files)
        table_name=get_table_name(Input_files)
        insert_file_into_db(conn,cur,table_name,data)
        cur.close()
        conn.close()

    except Exception as e:
        print(e)
 
