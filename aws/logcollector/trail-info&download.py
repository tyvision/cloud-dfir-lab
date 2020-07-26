import boto3
from datetime import datetime, date, time
import botocore.session
from botocore.config import Config
import json
from pprint import pprint


def getTrailsInfo(key_id,access_key,reg_name):
    
    session = botocore.session.get_session()

    client = session.create_client('cloudtrail', region_name=reg_name,aws_access_key_id=key_id,aws_secret_access_key=access_key)

    response = client.list_trails(
    # NextToken='string'
    )
    for item in response['Trails']:
        response2 = client.get_trail(
            Name=item['TrailARN'],
        )

        result2 = []
        print(item['Name'],response2["Trail"]['S3BucketName'])
        # result2.append(item['Name'],response2["Trail"]['S3BucketName'])

    return result2


print(getTrailsInfo(key_id="AKIASQUHDRT3NPOFP7EO",access_key="dqIG2QGst1lL3z3zrSICilnPXz23v4ydatsz1xum",reg_name='us-east-2'))

# with open('test.txt','w') as out:
#     for key,val in getTrailsInfo(key_id="AKIASQUHDRT3NPOFP7EO",access_key="dqIG2QGst1lL3z3zrSICilnPXz23v4ydatsz1xum",reg_name='us-east-2').items():
#         out.write('{}:{}\n'.format(key,val))

# TESTовый скрипт скачивания - не работает

# import boto3
# import os

# def download_dir(client, resource, dist, local='/tmp', bucket='your_bucket'):
#     paginator = client.get_paginator('list_objects')
#     for result in paginator.paginate(Bucket=bucket, Delimiter='/', Prefix=dist):
#         if result.get('CommonPrefixes') is not None:
#             for subdir in result.get('CommonPrefixes'):
#                 download_dir(client, resource, subdir.get('Prefix'), local, bucket)
#         for file in result.get('Contents', []):
#             dest_pathname = os.path.join(local, file.get('Key'))
#             if not os.path.exists(os.path.dirname(dest_pathname)):
#                 os.makedirs(os.path.dirname(dest_pathname))
#             resource.meta.client.download_file(bucket, file.get('Key'), dest_pathname)

# def downloadS3(key_id,access_key,reg_name):
    
#     session = botocore.session.get_session()

#     s3 = session.create_client('s3', region_name=reg_name,aws_access_key_id=key_id,aws_secret_access_key=access_key)
#     bucket = s3.Bucket('antontrail')

#     response = bucket.get_available_subresources()

#     print(response)
#     # result = {}
#     # for item in response['Trails']:
#     #     response2 = client.get_trail(
#     #         Name=item['TrailARN'],
#     #     )

#     #     # result2 = []
#     #     print(item['Name'],response2["Trail"]['S3BucketName'])
#     #         # result2.append(item2["logStreamName"])
        
#     #     # result[item['logGroupName']] = result2

#     return 0

# print(downloadS3(key_id="AKIASQUHDRT3NPOFP7EO",access_key="dqIG2QGst1lL3z3zrSICilnPXz23v4ydatsz1xum",reg_name='us-east-2'))