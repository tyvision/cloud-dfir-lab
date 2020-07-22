#!/usr/bin/env python3
#
# Test with
# ./list-log-stream.py
#
import boto3
from botocore.config import Config
import argparse
from datetime import datetime
from pprint import pprint

def arguments():
    parser = argparse.ArgumentParser(description='''
    Show the hierarchy Regions -> LogGroups -> LogStreams
    This script does not take any arguments.
    Credentials are read from ~/.aws/config or
    see https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html
    ''')

    return None

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
    args = arguments()
    res = list_hierarchy()
    pprint(res)

