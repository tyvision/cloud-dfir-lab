#!/usr/bin/env python3
#
# Test with
# ./example-cmdline-params.py gr str -r us-east-1 -o tmp/ -s 2020-07-14T00:30:23 -e 2020-07-01T00:00:00
#
import argparse
from datetime import datetime

parser = argparse.ArgumentParser(description='''
Download logs from AWS.
Credentials are read from ~/.aws/config or
see https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html
''')

parser.add_argument('log_group', type=str,
    help='Name of the log-group'
)
parser.add_argument('log_stream', type=str,
    help='Name of the log-stream within the log-group'
)
parser.add_argument('-r', '--awsregion', type=str,
    help='AWS region e.g. us-east-1. Overwrites the region specified in ~/.aws/config'
)
parser.add_argument('-o', '--outdir', type=str, default="./"
    help='Path to output directory'
)
parser.add_argument('-s', '--timestart', type=datetime.fromisoformat,
    help='Start time for events in iso format e.g. 2020-07-14T00:33:24'
)
parser.add_argument('-e', '--timeend', type=datetime.fromisoformat,
    help='End time for events in iso format e.g. 2020-07-14T00:33:24'
)

args = parser.parse_args()

print(args.log_group)
print(args.log_stream)
print(args.awsregion)
print(args.outdir)
print(args.timestart.isoformat())
print(args.timeend.isoformat())
