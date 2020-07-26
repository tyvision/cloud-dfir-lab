#!/usr/bin/env python3
#
# Test with
# ./download-log-stream.py us-east-2 RDSOSMetrics db-KQFXALKUCZHCARNXDMBWEKSUSY -o tmp -s 2020-01-01T00:00:01 -e 2020-10-01T00:00:01
#
import boto3

from pprint import pprint

import importlib
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

def get_log_stream(region_name, log_group, log_stream, tstart, tend, outdir):
    client = boto3.client('logs', region_name=region_name)

    responce = client.get_log_events(
        logGroupName=log_group,
        logStreamName=log_stream,
        startTime=time2boto(tstart),
        endTime=time2boto(tend)
    )

    return responce

def download_log_stream_to_path(region_name, log_group, log_stream, tstart, tend, fpath):
    client = boto3.client('logs', region_name=region_name)

    responce = client.get_log_events(
        logGroupName=log_group,
        logStreamName=log_stream,
        startTime=time2boto(tstart),
        endTime=time2boto(tend)
    )

    lib_utils.write_responce(fpath, responce)

def download_log_stream_to_file(region_name, log_group, log_stream, tstart, tend, outdir):
    client = boto3.client('logs', region_name=region_name)

    responce = client.get_log_events(
        logGroupName=log_group,
        logStreamName=log_stream,
        startTime=time2boto(tstart),
        endTime=time2boto(tend)
    )

    fpath = lib_utils.build_out_path(outdir, [region_name, log_group, log_stream])
    lib_utils.write_responce(fpath, responce)


if __name__=="__main__":
    args = get_parser().parse_args()
    res = get_log_stream(args.region, args.group, args.stream, args.timestart, args.timeend, args.outdir)
    pprint(res)
