#!/usr/bin/env python3
#
# Test with
# ./download-log-stream.py us-east-2 RDSOSMetrics db-KQFXALKUCZHCARNXDMBWEKSUSY -o tmp -s 2020-01-01T00:00:01 -e 2020-10-01T00:00:01
#
import boto3

from pprint import pprint

import importlib
import os
lib_utils = importlib.import_module("lib-utils")


def get_parser():
    helptext="Download Log Stream"
    args = [
        "region"
        , "group"
        , "stream"
        , "outdir"
        , "timestart"
        , "timeend"
    ]
    return lib_utils.get_parser(helptext, args)


def time2boto(t):
    return int(t.timestamp()) * 1000

def download_log_stream_to_path(region_name, log_group, log_stream, tstart, tend, fpath, aws_id=None, aws_secret=None):
    client = boto3.client('logs', region_name=region_name, aws_access_key_id=aws_id, aws_secret_access_key=aws_secret)

    response = client.get_log_events(
        logGroupName=log_group,
        logStreamName=log_stream,
        startTime=time2boto(tstart),
        endTime=time2boto(tend)
    )

    lib_utils.write_response(fpath, response)


if __name__=="__main__":
    args = get_parser().parse_args()
    outpath = os.path.join(args.outdir, "test-log-stream.json")
    download_log_stream_to_path(args.region, args.group, args.stream, args.timestart, args.timeend, outpath )
