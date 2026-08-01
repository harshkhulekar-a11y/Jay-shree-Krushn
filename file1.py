import json
import boto3

client=boto3.client('s3')
ScourceBucket='offline-13-bucket'
DestinationBucket='offline-13-bucket-desti'

def file_read():
    files=[]
    response = client.list_objects( Bucket='{}'.format(ScourceBucket))
    for file in response['Contents']:
        files.append(file['Key'])
    return files

def move_to_destination(file):
    response = client.copy_object(
    Bucket='{}'.format(DestinationBucket),
    CopySource='/{}/{}'.format(ScourceBucket,file),
    Key='{}'.format(file),
)

def delete_object_from_scource(file):
    response = client.delete_object(
    Bucket='{}'.format(ScourceBucket),
    Key='{}'.format(file),
)


def lambda_handler(event, context):
    file_list=file_read()
    for file in file_list:
        move_to_destination(file)
        delete_object_from_scource(file)

