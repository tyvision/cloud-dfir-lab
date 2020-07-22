#!/usr/bin/env python3
#
# Test with
# ./download-s3.py us-east-1 artembucket2.testdom1.co.uk -p test -o tmp
#
import boto3
import os

import importlib
lib_utils = importlib.import_module("lib-utils")

def get_parser():
    helptext="Download S3 buckets from AWS."
    args = [
        "region"
        , "bucket"
        , "prefix"
        , "outdir"
    ]
    return lib_utils.get_parser(helptext, args)

def download_dir_from_s3(bucket_name, prefix, region, outdir):
    resource = boto3.resource('s3', region_name=region)
    bucket = resource.Bucket(bucket_name)

    for obj in bucket.objects.filter(Prefix = prefix):
        dest_path = os.path.join(outdir, obj.key)

        # its a folder
        if (obj.key[-1] == os.path.sep):
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)

        # its a file
        else:
            bucket.download_file(obj.key, dest_path)

if __name__=='__main__':
    args = get_parser().parse_args()
    download_dir_from_s3(args.bucket, args.prefix, args.region, args.outdir)
