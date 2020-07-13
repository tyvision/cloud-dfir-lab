import boto3
from datetime import datetime, date, time
import botocore.session
from botocore.config import Config
import json


def getLogGroups(key_id,access_key,reg_name):
    
    session = botocore.session.get_session()

    client = session.create_client('logs', region_name=reg_name,aws_access_key_id=key_id,aws_secret_access_key=access_key)

    response = client.describe_log_groups(
        limit=50
    )

    result = {}
    for item in response['logGroups']:
        response2 = client.describe_log_streams(
            logGroupName=item['logGroupName'],
            orderBy= 'LastEventTime',
            descending=True,
            limit=50
        )
        result2 = []
        for item2 in response2["logStreams"]:
            result2.append(item2["logStreamName"])
        
        result[item['logGroupName']] = result2

    return result




print(getLogGroups(key_id="AKIASQUHDRT3NPOFP7EO",access_key="dqIG2QGst1lL3z3zrSICilnPXz23v4ydatsz1xum",reg_name='us-east-2'))

with open('data.txt','w') as out:
    for key,val in getLogGroups(key_id="AKIASQUHDRT3NPOFP7EO",access_key="dqIG2QGst1lL3z3zrSICilnPXz23v4ydatsz1xum",reg_name='us-east-2').items():
        out.write('{}:{}\n'.format(key,val))
