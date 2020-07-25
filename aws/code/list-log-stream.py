#!/usr/bin/env python3
#
# Test with
# ./list-log-stream.py
#
import boto3
from pprint import pprint

import importlib
lib_utils = importlib.import_module("lib-utils")

def get_parser():
    helptext="""
Show the hierarchy Regions -> LogGroups -> LogStreams
This script does not need any arguments.
"""
    args = []
    return lib_utils.get_parser(helptext, args)

def list_regions():
    # this must be 'ec2'
    # region can be any valid region
    client = boto3.client( 'ec2', region_name='us-east-1' )
    responce = client.describe_regions()
    names = [region['RegionName'] for region in responce['Regions']]
    return names

def list_region_log_groups(client):
    responce = client.describe_log_groups(
            limit=50
    )
    names = [group['logGroupName'] for group in responce['logGroups']]
    return names

def list_region_log_group_log_streams(client, log_group):
    responce = client.describe_log_streams(
        logGroupName=log_group,
        orderBy='LogStreamName',
        descending=True,
        limit=50
    )
    names = [stream['logStreamName'] for stream in responce['logStreams']]
    return names

def list_hierarchy():
    res = {}
    for reg in list_regions():
        res[reg] = {}
        client = boto3.client('logs', region_name=reg)
        for group in list_region_log_groups(client):
            res[reg][group] = []
            for stream in list_region_log_group_log_streams(client, group):
                res[reg][group].append(stream)
    return res

if __name__=="__main__":
    args = get_parser().parse_args()
    res = list_hierarchy()
    pprint(res)

