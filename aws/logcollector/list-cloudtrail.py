#!/usr/bin/env python3
#
# Test with
# ./list-cloudtrail.py
#
import boto3
from pprint import pprint
import json
import os

import importlib
lib_utils = importlib.import_module("lib-utils")

def get_parser():
    helptext="""
Show the hierarchy Bucket -> Objects
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

def list_region_trails(client):
    response = client.list_trails()
    names = [trail['TrailARN'] for trail in response['Trails']]
    return names

def list_hierarchy(aws_id=None, aws_secret=None):
    res = {}
    for reg in list_regions(aws_id, aws_secret):
        res[reg] = []
        client = boto3.client('cloudtrail', region_name=reg, aws_access_key_id=aws_id, aws_secret_access_key=aws_secret)
        for trail in list_region_trails(client):
            res[reg].append(trail)
    return res


def list_hierarchy_jsonl(aws_id=None, aws_secret=None):
    res = ""
    for reg in list_regions(aws_id, aws_secret):
        client = boto3.client('cloudtrail', region_name=reg, aws_access_key_id=aws_id, aws_secret_access_key=aws_secret)
        for trail in list_region_trails(client):
            item = {
                "cloud" : "aws",
                "storage" : "logstream",
                "cleanup" : "default",
                "region" : reg,
                "trail" : trail,
            }
            res += json.dumps(item, indent=4, sort_keys=True) + "\n"
    return res


if __name__=="__main__":
    args = get_parser().parse_args()
    res = list_hierarchy_jsonl()
    print(res)
