import json
import boto3
import pymysql
import csv

client=boto3.client('s3')
host='database-1.czewk2q0eqo4.ap-south-1.rds.amazonaws.com'
port=3306
username='admin'
password='Admin#2110'
database='offline13'
outputfile='bank_info.csv'
bucketname='offline-email-ses'

def database_connection():
    try:
        conn=pymysql.connect(host=host,user=username,password=password,port=port,db=database)
        cur=conn.cursor()
        return conn,cur

    except Exception as e:
        print(e)

def fetch_data_from_db(conn,cur):
    try:
        query="select AccountNumber,CustomerName,Balance from bank_info"
        cur.execute(query)
        data=cur.fetchall()
        return data

    except Exception as e:
        print(e)

def write_file(data):
    try:
        with open('/tmp/{}'.format(outputfile),'w') as fp:
            w=csv.writer(fp)
            w.writerow(['AccountNumber','CustomerName','Balance'])
            w.writerows(data)

    except Exception as e:
        print(e)

def upload_into_s3():
    try:

        client.upload_file('/tmp/{}'.format(outputfile), '{}'.format(bucketname), '{}'.format(outputfile))
    
    except Exception as e:
        print(e)
 

def lambda_handler(event, context):
    conn,cur=database_connection()
    data=fetch_data_from_db(conn,cur)
    write_file(data)
    upload_into_s3()
    cur.close()
    conn.close()

