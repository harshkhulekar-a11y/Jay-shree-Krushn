import json
import boto3

client=boto3.client('ses')

def send_email(bucket,files):
    response = client.send_email(
    Destination={
        'ToAddresses': [
            'harshkhulekar@gmail.com',
        ],
    },
    Message={
        'Body': {
            'Html': {
                'Charset': 'UTF-8',
                'Data': '{} file upload on this bucket : {}'.format(files,bucket),
            },
            'Text': {
                'Charset': 'UTF-8',
                'Data': 'This is the message body in text format.',
            },
        },
        'Subject': {
            'Charset': 'UTF-8',
            'Data': 'File upload in s3 notification',
        },
    },
    Source='harshkhulekar@gmail.com',
)


def lambda_handler(event, context):
    
    message = json.loads(json.loads(event['Records'][0]['body'])['Message'])

    files = []

    for record in message['Records']:
        bucket = record['s3']['bucket']['name']
        files.append(record['s3']['object']['key'])

    send_email(bucket, files)

    return files
 
