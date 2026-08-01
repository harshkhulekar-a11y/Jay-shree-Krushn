import json
import boto3

client=boto3.client('s3')
Bucket='folder-assigenment'
Source_data='scource/'
Destination_data='destination/'

def list_object_from_s3():
    file=[]
    response = client.list_objects_v2(Bucket='{}'.format(Bucket),Prefix='{}'.format(Source_data))
    for files in response["Contents"]:
        file.append(files['Key'])
    return file

def copy_object_to_desti(file_list):
    response = client.copy_object(
    Bucket='{}'.format(Bucket),
    CopySource='/{}/{}'.format(Bucket,file_list),
    Key=file_list.replace(Source_data, Destination_data, 1)
)

def delete_file_from_s3(file_list):
    response = client.delete_object(
        Bucket='{}'.format(Bucket),
        Key='{}'.format(file_list)
    )

def lambda_handler(event, context):
    file_list=list_object_from_s3()
    for files in file_list:
        copy_object_to_desti(files)
        delete_file_from_s3(files)
        
    


