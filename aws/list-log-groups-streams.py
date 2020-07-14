#!/usr/bin/env python3
import boto3
from datetime import datetime, date, time
import botocore.session
from botocore.config import Config
import json

from pprint import pprint
import argparse
from datetime import datetime

parser = argparse.ArgumentParser(description='''
Show the hierarchy Regions -> LogGroups -> LogStreams
Credentials are read from ~/.aws/config or
see https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html
''')

parser.add_argument('--prefixregion', type=str, default=None,
    help='Prefix to filter regions e.g. us-east'
)
parser.add_argument('--prefixgroup', type=str, default=None,
    help='Prefix to filter log-groups'
)
parser.add_argument('--prefixstream', type=str, default=None,
    help='Prefix to filter log-streams'
)
parser.add_argument('-o', '--outdir', type=str, default="./",
    help='Path to output directory, by default current directory'
)
parser.add_argument('-s', '--timestart', type=datetime.fromisoformat,
    help='Start time for events in iso format e.g. 2020-07-14T00:33:24'
)
parser.add_argument('-e', '--timeend', type=datetime.fromisoformat,
    help='End time for events in iso format e.g. 2020-07-14T00:33:24'
)

args = parser.parse_args()

def list_regions():
    # this can be any service, lets just use ec2
    client = boto3.client('ec2')
    responce = client.describe_regions()
    # get only the names
    # names = [region['RegionName'] if region['RegionName'].startswith(args.prefixregion) for region in responce['Regions']]
    names = [region['RegionName'] for region in responce['Regions']]
    return names

def list_region_log_groups(client):
    responce = client.describe_log_groups(
        # logGroupNamePrefix=args.prefixgroup,
        limit=50
    )
    # get only the names
    names = [group['logGroupName'] for group in responce['logGroups']]
    return names

def list_region_log_group_log_streams(client, log_group):
    responce = client.describe_log_streams(
        logGroupName=log_group,
        # logStreamNamePrefix=args.prefixstream,
        orderBy='LogStreamName',
        descending=True,
        limit=50
    )
    # get only the names
    names = [stream['logStreamName'] for stream in responce['logStreams']]
    return names

def list_hierarchy():
    for reg in list_regions():
        # print(reg)
        client = boto3.client('logs', region_name=reg)
        for group in list_region_log_groups(client):
            # print("{}-{}".format(reg, group))
            for stream in list_region_log_group_log_streams(client, group):
                # print("{}-{}-{}".format(reg, group, stream))
                yield (reg, group, stream)

if __name__=="__main__":
    res = list_hierarchy()
    for item in res:
        print("{} - {:50} - {}".format(*item))

# def get_log_stream(client, log_group, log_stream)
#     responce = client.get_log_events(
#         logGroupName=log_group,
#         logStreamName=log_stream,
#         startTime=args.timestart,
#         endTime=args.timeend
#     )
#     # write to file
#     return responce
# 
