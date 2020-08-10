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
        "bucket"
        , "prefix"
        , "outdir"
    ]
    return lib_utils.get_parser(helptext, args)

def download_object_from_s3(bucket_name, key, outpath, aws_id=None, aws_secret=None):
    # region does not matter for buckets
    resource = boto3.resource('s3', region_name='us-east-1', aws_access_key_id=aws_id, aws_secret_access_key=aws_secret)
    resource.Object(bucket_name, key).download_file(outpath)

def download_dir_from_s3(bucket_name, prefix, outdir, aws_id=None, aws_secret=None):
    # region does not matter for buckets
    resource = boto3.resource('s3', region_name='us-east-1', aws_access_key_id=aws_id, aws_secret_access_key=aws_secret)
    bucket = resource.Bucket(bucket_name)

    for obj in bucket.objects.filter(Prefix = prefix):
        dest_path = os.path.join(outdir, obj.key)

        # its a folder key, aws path sep is '/'
        if (obj.key[-1] == '/'):
            continue

        # its a file
        sane_path = lib_utils.build_out_path(outdir, dest_path.split('/'))
        bucket.download_file(obj.key, sane_path)

if __name__=='__main__':
    args = get_parser().parse_args()
    download_dir_from_s3(args.bucket, args.prefix, args.outdir)
