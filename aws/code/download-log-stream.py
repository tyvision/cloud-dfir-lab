#!/usr/bin/env python3
#
# Test with
# ./download-log-stream.py 'us-east-2' 'RDSOSMetrics' 'db-KQFXALKUCZHCARNXDMBWEKSUSY' -o tmp -s 2020-01-01T00:00:01 -e 2020-10-01T00:00:01
#
import boto3
from botocore.config import Config
import argparse
from datetime import datetime
import os
import json
import re

def arguments():
    parser = argparse.ArgumentParser(description='''
    Download Log Stream
    Credentials are read from ~/.aws/config or
    see https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html
    ''')

    parser.add_argument('awsregion', type=str,
        help='AWS region e.g. us-east-1. Overwrites the region specified in ~/.aws/config'
    )
    parser.add_argument('log_group', type=str,
        help='Name of the log-group'
    )
    parser.add_argument('log_stream', type=str,
        help='Name of the log-stream within the log-group'
    )
    parser.add_argument('-o', '--outdir', type=str, default="./",
        help='Path to output directory, by default current directory'
    )
    parser.add_argument('-s', '--timestart', type=datetime.fromisoformat, default=datetime.fromisoformat("3000-01-01T00:00:00"),
        help='Start time for events in iso format e.g. 2020-07-14T00:33:24'
    )
    parser.add_argument('-e', '--timeend', type=datetime.fromisoformat, default=datetime.fromisoformat("2000-01-01T00:00:00"),
        help='End time for events in iso format e.g. 2020-07-14T00:33:24'
    )

    return parser.parse_args()


def open_aws_entity(args):
    custom_config = Config(
        region_name=args.awsregion
    )

    # boto3 will automatically use parameters from custom Config if they are not None
    client = boto3.client('logs', config=custom_config)
    return client

def get_valid_fname(s):
    s = str(s).strip()
    s = s.replace('\\', '-')
    s = s.replace('/', '-')
    s = s.replace(' ', '-')
    s = s.replace('.', '-')
    return re.sub(r'(?u)[^-\w.]', '', s)

def download_log_stream(local_dir, client, log_group, log_stream, tstart, tend):
    responce = client.get_log_events(
        logGroupName=log_group,
        logStreamName=log_stream,
        startTime=int(tstart.timestamp()),
        endTime=int(tend.timestamp())
    )
    stream_fs_name = "{}_{}_{}".format(client._client_config.region_name, log_group, log_stream)
    sanitised_stream_fs_name = get_valid_fname(stream_fs_name) + ".json"
    dest_path = os.path.join(local_dir, sanitised_stream_fs_name)
    with open(dest_path, 'w') as stream_file:
        stream_file.write(json.dumps(responce))


if __name__=="__main__":
    args = arguments()
    client = open_aws_entity(args)
    download_log_stream(args.outdir, client, args.log_group, args.log_stream, args.timestart, args.timeend)
