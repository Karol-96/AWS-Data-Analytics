import boto3
import json

def get_data():
    #S3 Bucket we will be interacting with
    s3_bucket = 'random-users-data-807211637290'
    #Because we need to combine data from multiple s3 objects, initialize a list to hold this data before returning it.
    data = []
    #Initialize an boto3 S3 client, and list the objects in our bucket. the data about the contents of our bucket will be stored in a list called data
    s3 = boto3.client('s3')
    objects = s3.list_objects_v2(Bucket = s3_bucket)['Contents']
    
    s3_keys = []
    for object in objects:
        if object['Key'].startswith('users_'):
            s3_keys.append(object['Key'])
            
            
    #After collecting the appropriate keys that begin with "users_" gather each object, and combine the returned data with the existing 'data'
    for key in s3_keys:
        object = s3.get_object(
            Bucket = s3_bucket,
            Key = key)
        object_data = json.loads(object['Body'].read())
        data += object_data
    return data

def handler(event, context):
    # Call the "get_data" function and return appropriately formatted results.
    return {'isBase64Encoded': False,'statusCode': 200,'body': json.dumps(get_data()), 'headers': {"Access-Control-Allow-Origin": "*"}}