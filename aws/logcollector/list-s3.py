#!/usr/bin/env python3
#
# Test with
# ./list-s3.py
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

def list_buckets(aws_id, aws_secret):
    # region can be any valid region
    client = boto3.client( 's3', region_name='us-east-1', aws_access_key_id=aws_id, aws_secret_access_key=aws_secret)
    response = client.list_buckets()
    names = [bucket['Name'] for bucket in response['Buckets']]
    return names

def list_bucket_keys(client, bucket):
    paginator = client.get_paginator('list_objects')
    page_iterator = paginator.paginate(Bucket=bucket)
    keys = []
    for page in page_iterator:
        for key in page['Contents']:
            # dont mention the file if its a directory
            # aws path sep is '/'
            if key['Key'][-1] == '/':
                continue

            keys.append( key['Key'] )

    pprint(keys)
    return keys

def list_hierarchy(aws_id=None, aws_secret=None):
    res = {}
    client = boto3.client('s3', region_name='us-east-1', aws_access_key_id=aws_id, aws_secret_access_key=aws_secret)
    for bucket in list_buckets(aws_id, aws_secret):
        res[bucket] = []
        for key in list_bucket_keys(client, bucket):
            res[bucket].append(key)
    return res


def list_hierarchy_jsonl(aws_id=None, aws_secret=None):
    res = ""
    for bucket in list_buckets(aws_id, aws_secret):
        client = boto3.client('s3', region_name='us-east-1', aws_access_key_id=aws_id, aws_secret_access_key=aws_secret)
        for key in list_bucket_keys(client, bucket):
            item = {
                "cloud" : "aws",
                "storage" : "s3",
                "cleanup" : "default",
                "bucket" : bucket,
                "key" : key,
            }
            res += json.dumps(item, indent=4, sort_keys=True) + "\n"
    return res

if __name__=="__main__":
    args = get_parser().parse_args()
    # res = list_hierarchy()
    # pprint(res)
    res = list_hierarchy_jsonl()
    print(res)

