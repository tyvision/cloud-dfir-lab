#!/usr/bin/env python3
#
# Test with
# ./transfer-events.py ../config/example-transfer-spec.json
#
#
import os
import shutil
from pprint import pprint
import json
from pathlib import Path

import importlib
lib_utils = importlib.import_module("lib-utils")

download_log_stream = importlib.import_module("download-log-stream")
download_s3 = importlib.import_module("download-s3")

cleanup_vpc_logs = importlib.import_module("cleanup-vpc-logs")
cleanup_cloudtrail_logs = importlib.import_module("cleanup-cloudtrail-logs")
cleanup_s3access_logs = importlib.import_module("cleanup-s3access-logs")

download_gcp_bucket = importlib.import_module("download-gcp-bucket")
cleanup_gcp_cloudaudit_logs = importlib.import_module("cleanup-gcp-cloudaudit-logs")

rawdir = './rawlogs/'
cleandir = "./cleanlogs/"


def get_parser():
    helptext="""
Consumes JSON specification of events to transfer from AWS logs into Timesketch.
See example spec in config/example-transfer-spec.json
"""
    args = [
        "inputfile"
        , "timestart"
        , "timeend"
    ]
    return lib_utils.get_parser(helptext, args)

def find_cleanup(target, raw_path):
    cleanup_functions = {
        "vpc" : cleanup_vpc_logs.cleanup_file2file,
        "cloudaudit" : cleanup_gcp_cloudaudit_logs.cleanup_file2file,
        "cloudtrail" : cleanup_cloudtrail_logs.cleanup_file2file,
        "s3access" : cleanup_s3access_logs.cleanup_file2file,
    }

    return cleanup_functions[ target["cleanup"] ]

def find_download(target):
    download_functions = {
        "aws" : {
            "logstream" : download_aws_logstream_target,
            "s3" : download_aws_s3_target,
            "cloudwatch" : None,
        },
        "gcp" : {
            "bucket" : download_gcp_bucket_target,
        }
    }

    return download_functions[ target["cloud"] ][ target["storage"] ]

def download_aws_logstream_target(target, timestart, timeend, aws_id=None, aws_secret=None, gcp_secret_json=None):
    region_name = target["region"]
    log_group = target["group"]
    log_stream = target["stream"]
    stream_sane_name = lib_utils.build_sane_basename([region_name, log_group, log_stream])
    raw_path = os.path.join(rawdir, stream_sane_name) + ".json"
    download_log_stream.download_log_stream_to_path(region_name, log_group, log_stream, timestart, timeend, raw_path, aws_id, aws_secret)
    return raw_path

def download_aws_s3_target(target, timestart, timeend, aws_id=None, aws_secret=None, gcp_secret_json=None):
    bucket = target["bucket"]
    key = target["key"]
    sane_path = lib_utils.build_sane_basename(key.split('/'))
    raw_path = os.path.join(rawdir, sane_path) + ".json"
    download_s3.download_object_from_s3(bucket, key, raw_path, aws_id, aws_secret)
    return raw_path

def download_gcp_bucket_target(target, timestart, timeend, aws_id=None, aws_secret=None, gcp_secret_json=None):
    bucket_name = target["bucket"]
    prefix = target["prefix"]
    stream_sane_name = lib_utils.build_sane_basename([bucket_name, prefix])
    raw_path = os.path.join(rawdir, stream_sane_name) + ".json"
    download_gcp_bucket.download_blob_to_path(bucket_name, prefix, raw_path, gcp_secret_json)
    return raw_path

def recreate_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

def transfer_events(timesketch_url, targets, timestart, timeend, aws_id=None, aws_secret=None, gcp_secret_json=None):
    rawdir = './rawlogs/'
    cleandir = "./cleanlogs/"

    recreate_dir(rawdir)
    recreate_dir(cleandir)

    for target in targets:
        # download raw log
        download = find_download(target)
        if download is None:
            print("Download function for {} can not be found, can not upload to timesketch. Skipping this entry.".format(target))
            continue
        raw_path = download(target, timestart, timeend, aws_id, aws_secret, gcp_secret_json)

        # cleanup log
        clean_path = os.path.join(cleandir, Path(raw_path).stem) + ".jsonl"
        cleanup = find_cleanup(target, raw_path)
        if cleanup is None:
            print("Cleanup function for {} can not be found, can not upload to timesketch. Skipping this entry.".format(target))
            continue
        cleanup(raw_path, clean_path)

        # upload into timesketch, must limit timeline name
        timeline_name = Path(raw_path).stem[:100]
        command = """timesketch_importer --host '{}' \
                --timeline_name '{}' \
                --sketch_id 1 \
                --username admin \
                --password admin \
                {}
        """.format(timesketch_url, timeline_name, clean_path)
        print("Running:{}".format(command))
        os.system(command)
        print("Done")


if __name__ == "__main__":
    args = get_parser().parse_args()

    targets = []
    import ijson.backends.python as ijson
    with open(args.inputfile, "rb") as f:
        targets = list( ijson.items(f, '', multiple_values=True) )

    gcp_credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', "../../GCP/CloudToken.json")
    import json
    with open(gcp_credentials_path, "rb") as f:
        gcp_credentials = json.load(f)

    aws_id = os.getenv('AWS_ACCESS_KEY_ID', None)
    aws_secret = os.getenv('AWS_SECRET_ACCESS_KEY', None)

    transfer_events("http://localhost:80", targets, args.timestart, args.timeend, aws_id=aws_id, aws_secret=aws_secret, gcp_secret_json=gcp_credentials)
