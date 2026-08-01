import json
import boto3
import pymysql 
import csv

secred_client=boto3.client('secretsmanager')
s3_client=boto3.client('s3')


def get_credentials():

    response =secred_client.get_secret_value(SecretId='prod/s3/cread')
    secret=json.loads(response['SecretString'])
    return secret

def database_connection(secret):
    try:
        conn=pymysql.connect(host=secret['host'],user=secret['username'],password=secret['password'],db=secret['dbname'],port=int(secret['port']))
        cur=conn.cursor()
        return conn,cur

    except Exception as e:
        print(e)

def download_file_from_s3(Bucket_name,Filename):
    try:

        s3_client.download_file('{}'.format(Bucket_name), '{}'.format(Filename), '/tmp/{}'.format(Filename))

    except Exception as e:
        print(e)

def read_file_from_tmp(Filename):
    try:
        with open('/tmp/{}'.format(Filename,))as fp:
            r=csv.DictReader(fp)
            data=list(r)
            return data
    except Exception as e:
        print(e)

def insert_into_database(conn,cur,data):
    try:
        query="CREATE TABLE IF NOT EXISTS emp_data(OrderID int,ProductID int,Quantity int)"
        cur.execute(query)

        for i in data:  
            query1="insert into emp_data values({},{},{})".format(i['OrderID'], i['ProductID'], i['Quantity'])
            cur.execute(query1)
        conn.commit()

    except Exception as e:
        print(e)

def lambda_handler(event, context):
    Bucket_name=event['Records'][0]['s3']['bucket']['name']
    Filename=event['Records'][0]['s3']['object']['key']
    secret=get_credentials()
    conn,cur=database_connection(secret)
    download_file_from_s3(Bucket_name, Filename)
    data=read_file_from_tmp(Filename)
    insert_into_database(conn,cur,data)

   


