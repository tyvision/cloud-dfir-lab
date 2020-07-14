#!/usr/bin/env python3
#
# Test with
# ./download-s3.py artembucket2.testdom1.co.uk -p test -o tmp
#
import boto3
import os
from botocore.config import Config

import argparse
from datetime import datetime

def arguments():
    parser = argparse.ArgumentParser(description='''
    Download S3 buckets from AWS.
    Credentials are read from ~/.aws/config or
    see https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html
    ''')

    parser.add_argument('bucket', type=str,
        help='Name of the bucket'
    )
    parser.add_argument('-p', '--prefix', type=str, default="",
        help='Optional path prefix used as a filter when including files into download list, by default empty string'
    )
    parser.add_argument('-r', '--awsregion', type=str,
        help='AWS region e.g. us-east-1. Overwrites the region specified in ~/.aws/config'
    )
    parser.add_argument('-o', '--outdir', type=str, default="./",
        help='Path to output directory, by default current directory'
    )

    return parser.parse_args()

def open_aws_entity(args):
    custom_config = Config(
        region_name=args.awsregion
    )

    # boto3 will automatically use parameters from custom Config if they are not None
    resource = boto3.resource('s3', config=custom_config)
    bucket = resource.Bucket(args.bucket)
    return bucket

def download_dir_from_s3(local_dir, bucket, dir_prefix):
    for obj in bucket.objects.filter(Prefix = dir_prefix):
        dest_path = os.path.join(local_dir, obj.key)

        # its a folder
        if (obj.key[-1] == os.path.sep):
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)

        # its a file
        else:
            bucket.download_file(obj.key, dest_path)


if __name__=='__main__':
    args = arguments()
    bucket = open_aws_entity(args)
    download_dir_from_s3(args.outdir, bucket, args.prefix)
