#!/usr/bin/env python3
#
# Test with
# ./example-cmdline-params.py gr str -r us-east-1 -o tmp/ -s 2020-07-14T00:30:23 -e 2020-07-01T00:00:00
#
import argparse
from datetime import datetime
import json
import os
import re
from pathlib import Path

def get_parser(helptext, params):
    fulltext = """{}

Configure credentials see https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html
    """.format(helptext)

    parser = argparse.ArgumentParser( description=fulltext , formatter_class=argparse.RawDescriptionHelpFormatter )

    # other
    if "region" in params:
        parser.add_argument('region', type=str,
            help='AWS region e.g. us-east-1. Overwrites the region specified in ~/.aws/config'
        )

    # log steam related (Cloud Watch)
    if "group" in params:
        parser.add_argument('group', type=str,
            help='Name of the log-group in specific region'
        )

    if "stream" in params:
        parser.add_argument('stream', type=str,
            help='Name of the log-stream within the log-group'
        )

    # bucket related (S3)
    if "bucket" in params:
        parser.add_argument('bucket', type=str,
            help='Name of the bucket'
        )

    if "prefix" in params:
        parser.add_argument('-p', '--prefix', type=str, default="",
            help='Optional path prefix used as a filter when including files into download list, by default empty string'
        )

    # metrics related (Cloud Watch)
    if "namespace" in params:
        parser.add_argument('namespace', type=str,
            help='Namespace where metric is hosted e.g. "AWS/EC2" or https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/aws-services-cloudwatch-metrics.html'
        )

    if "metric" in params:
        parser.add_argument('metric', type=str,
            help='Name of the metric e.g. "NetworkOut" or https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/viewing_metrics_with_cloudwatch.html'
        )

    # for JSON clean up scripts
    if "inputfile" in params:
        parser.add_argument('inputfile', type=Path,
            help='Path to input file'
        )

    if "outputfile" in params:
        parser.add_argument('outputfile', type=Path,
            help='Path to output file'
        )

    # other
    if "timestart" in params:
        parser.add_argument('-s', '--timestart', type=datetime.fromisoformat, default=datetime.fromisoformat("2000-01-01T00:00:00"),
            help='Start time (earlier) for events in iso format e.g. 2000-01-01T00:00:00'
        )

    if "timeend" in params:
        parser.add_argument('-e', '--timeend', type=datetime.fromisoformat, default=datetime.fromisoformat("3000-01-01T00:00:00"),
            help='End time (later) for events in iso format e.g. 3000-01-01T00:00:00'
        )

    if "outdir" in params:
        parser.add_argument('-o', '--outdir', type=str, default="./",
            help='Path to output directory, by default current directory'
        )

    return parser


def sanitize_fname(s):
    s = str(s).strip()
    s = s.replace('\\', '-')
    s = s.replace('/', '-')
    s = s.replace(' ', '-')
    s = s.replace('.', '-')
    return re.sub(r'(?u)[^-\w.]', '', s)

def build_sane_basename(fname_components):
    raw_basename = "_".join(fname_components)
    return sanitize_fname(raw_basename)

def build_out_path(outdir, fname_components):
    raw_basename = "_".join(fname_components)
    fname = sanitize_fname(raw_basename) + ".json"
    return os.path.join(outdir, fname)


def write_response(dest_path, response):
    with open(dest_path, 'w') as f:
        f.write(json.dumps(response))


def read_integer(prompt, min_val, max_val):
    while True:
        user_in = input(prompt)

        # check if wants to quit
        if "exit" in user_in or "quit" in user_in or "q" in user_in:
            return None

        # try parsing number
        try:
            i = int(user_in)
            if min_val <= i and i <= max_val:
                return i
            else:
                print("Index must be in range {} to {}".format(min_val, max_val))
        except Exception as e:
            print(e)
            print("Error, please try again")

def read_string(prompt):
    while True:
        user_in = input(prompt)

        # check if wants to quit
        if "exit" in user_in or "quit" in user_in or "q" in user_in:
            return None

        return user_in.strip()

if __name__ == "__main__":
    args = get_parser("Example parser", []).parse_args()

    print(args.log_group)
    print(args.log_stream)
    print(args.region)
    print(args.outdir)
    print(args.timestart.isoformat())
    print(args.timeend.isoformat())
    print(args.inputfile)
    print(args.outputfile)
