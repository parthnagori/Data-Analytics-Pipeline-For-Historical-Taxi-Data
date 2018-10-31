import boto3
import json
import csv
import datetime
import os
from collections import defaultdict

SOURCE_BUCKET = os.environ.get("SOURCE_BUCKET", "nyc-tlc")
DESTINATION_BUCKET = os.environ.get("DESTINATION_BUCKET", "nyc-tlc-processed")

# main function of lambda
def lambda_handler(event, context):    
    files = list_s3_files(SOURCE_BUCKET)
    for f in files:
        read_file(SOURCE_BUCKET, f)

# List the keys in the bucket
def list_s3_files(bucket):
    '''
    input- string: bucket name - nyc-tlc
    output- list: file names
    '''

    # Create the path to list
    path = bucket + "/trip data"
    my_bucket = s3.Bucket(path)

    # Connect to S3
    try:
        conn = client('s3')
    except Exception:
        print("Could not connect to S3")
        exit(1)

    # List files in the bucket
    files = []
    try:
        for key in conn.list_objects(Bucket=path)['Contents']:
            filename = key['Key']
            filename = filename.strip("{}./".format(bucket))
            files.append(filename)
    except Exception:
        print("Could not list key in {}".format())
        pass

    return files


# Read the files in the bucket and process
def read_file(bucket, key):
    '''
    input-  string: bucket 
            key: file name
    output- None   
    '''
    print("read file {}".format(key))

    # Connect to S3
    try:
        s3 = boto3.resource('s3')
    except Exception:
        print("Could not connect to S3")
        exit(1)
    
    # read the content
    try:        
        obj = s3.Object(bucket, key)
        input = obj.get()['Body'].read().decode('utf-8')
        process_file(content, key)
    except Exception:
        print("Could not connect to S3")
        exit(1)
        
# Process the file by calling the appropriate lambda 
def process_file(content, key):
    '''
    input-  bytes: content 
            key: key path to object inside bucket
    output- None   
    '''

    print("Processing file {}".format(content))

    # Get lamda client
    try:
        client = boto3.client('lambda')
    except Exception:
        print("Could not connect to S3")
        exit(1)
    
    # Construct the payload for next lambda call
    input = {
        "content": content,
        "destination": DESTINATION_BUCKET,
        "key": key,
    }

    # Asynchronous call to processing 
    response = client.invoke(
            FunctionName=processor,
            InvocationType="Event",
            Payload=bytes(JSON.dumps(input), 'utf-8')
        )
    ## processor lambda to be implemented