import boto3
from datetime import datetime, date, time
import botocore.session
from botocore.config import Config

my_config = Config(
    region_name = 'us-east-2',
    signature_version = 'v4',
)

aws_access_key_id = ""
aws_secret_access_key = ""

session = botocore.session.get_session()
client = session.create_client('cloudwatch', region_name='us-east-2',aws_access_key_id="access_KEY_ID",
         aws_secret_access_key= "SECRET")
response = client.get_metric_statistics(
    Namespace='AWS/EC2',
    MetricName='NetworkOut',
    Dimensions=[
        {
            'Name': 'InstanceType',
            'Value': 't2.micro'
        },
    ],
    StartTime=datetime(2020, 6, 25),
    EndTime=datetime(2020, 6, 26),
    Period=120,
    Statistics=[
        'Average',
    ],
    Unit='Kilobytes'
)

print('Result:', response)


# # Create CloudWatch client
# cloudwatch = boto3.client('cloudwatch', config=my_config)

# # List metrics through the pagination interface
# paginator = cloudwatch.get_paginator('list_metrics')
# for response in paginator.paginate(Dimensions=[{'Name': 'LogGroupName'}],
#                                    MetricName='NetworkOut',
#                                    Namespace='AWS/EC2'):
#     print(response['Metrics'])