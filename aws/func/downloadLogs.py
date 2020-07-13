import boto3
from datetime import datetime, date, time
import botocore.session
from botocore.config import Config
import json
import time

def downloadLogs(key_id,access_key,reg_name,log_Name,stime,etime,blimit):
    session = botocore.session.get_session()

    client = session.create_client('logs', region_name=reg_name,aws_access_key_id=key_id,aws_secret_access_key=access_key)

    response = client.start_query(
        logGroupName=log_Name,
        startTime=stime,
        endTime=etime,
        queryString='fields @timestamp, @message | sort @timestamp desc',
        limit=blimit
    )

    print("queryID: " + response["queryId"])
    print()
    time.sleep(1)

    response2 = client.get_query_results(
        queryId = response["queryId"] # ID получаем после выполнения запроса start_query
    )
    time.sleep(0.5)

    response3 = client.stop_query(
        queryId=response["queryId"]
    )

    if response3["success"] == True:
        print("Query stop success")
        print()
    else:
        print("Query stop error")
        print()

    print(response2)
    return response2

# print(downloadLogs(key_id="AKIASQUHDRT3NPOFP7EO",access_key="dqIG2QGst1lL3z3zrSICilnPXz23v4ydatsz1xum",reg_name='us-east-2',log_Name="RDSOSMetrics",stime=1593982800,etime=1594054800,blimit=10))

with open('logs.txt','w') as out:
    for key,val in downloadLogs(key_id="AKIASQUHDRT3NPOFP7EO",access_key="dqIG2QGst1lL3z3zrSICilnPXz23v4ydatsz1xum",reg_name='us-east-2',log_Name="RDSOSMetrics",stime=1593982800,etime=1594054800,blimit=10).items():
        out.write('{}:{}\n'.format(key,val))