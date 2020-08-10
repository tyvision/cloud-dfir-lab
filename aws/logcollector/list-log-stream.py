#!/usr/bin/env python3
#
# Test with
# ./list-log-stream.py
#
import boto3
from pprint import pprint
import json

import importlib
lib_utils = importlib.import_module("lib-utils")

def get_parser():
    helptext="""
Show the hierarchy Regions -> LogGroups -> LogStreams
This script does not need any arguments.
"""
    args = []
    return lib_utils.get_parser(helptext, args)

def list_regions(aws_id, aws_secret):
    # this must be 'ec2'
    # region can be any valid region
    client = boto3.client( 'ec2', region_name='us-east-1', aws_access_key_id=aws_id, aws_secret_access_key=aws_secret)
    response = client.describe_regions()
    names = [region['RegionName'] for region in response['Regions']]
    return names

def list_region_log_groups(client):
    response = client.describe_log_groups(
            limit=50
    )
    names = [group['logGroupName'] for group in response['logGroups']]
    return names

def list_region_log_group_log_streams(client, log_group):
    response = client.describe_log_streams(
        logGroupName=log_group,
        orderBy='LogStreamName',
        descending=True,
        limit=50
    )
    names = [stream['logStreamName'] for stream in response['logStreams']]
    return names

def list_hierarchy(aws_id=None, aws_secret=None):
    res = {}
    for reg in list_regions(aws_id, aws_secret):
        res[reg] = {}
        client = boto3.client('logs', region_name=reg, aws_access_key_id=aws_id, aws_secret_access_key=aws_secret)
        for group in list_region_log_groups(client):
            res[reg][group] = []
            for stream in list_region_log_group_log_streams(client, group):
                res[reg][group].append(stream)
    return res


def list_hierarchy_jsonl(aws_id=None, aws_secret=None):
    res = ""
    for reg in list_regions(aws_id, aws_secret):
        client = boto3.client('logs', region_name=reg, aws_access_key_id=aws_id, aws_secret_access_key=aws_secret)
        for group in list_region_log_groups(client):
            for stream in list_region_log_group_log_streams(client, group):
                item = {
                    "cloud" : "aws",
                    "storage" : "logstream",
                    "cleanup" : "default",
                    "region" : reg,
                    "group" : group,
                    "stream" : stream,
                }
                res += json.dumps(item, indent=4, sort_keys=True) + "\n"
    return res


if __name__=="__main__":
    args = get_parser().parse_args()
    res = list_hierarchy()
    pprint(res)

