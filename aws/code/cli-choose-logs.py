#!/usr/bin/env python3
import importlib

list_log_streams = importlib.import_module("list-log-groups-streams")
download_log_stream = importlib.import_module("download-log-stream")

# list_s3_buckets
# download-s3.py

# list_cloudwatch_metrics
# download-cloudwatch.py

from pprint import pprint
from botocore.config import Config
import argparse
from datetime import datetime
import boto3


def arguments():
    parser = argparse.ArgumentParser(description='''
    Download selected Log Streams with correct time range.
    Credentials are read from ~/.aws/config or
    see https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html
    ''')

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


def read_index(min_val, max_val):
    while True:
        try:
            i = int(input("Enter index of stream to download or Ctrl-C to quit:"))
            if min_val <= i and i <= max_val:
                return i
            else:
                print("Index must be in range {} to {}".format(min_val, max_val))
        except Exception as e:
            print(e)
            print("Error, please try again")


def get_possible_download_items():
    res = list_log_streams.list_hierarchy()
    count = 0
    valid = []
    for reg, group_dict in res.items():
        for group, stream_list in group_dict.items():
            for stream in stream_list:
                valid.append([" ", count, reg, group, stream])
                count += 1
    return valid


def interactively_download(args, items):
    for item in items:
        print("{:2} {:3} {:20} {:60} {}".format(*item))

    i = read_index(0, len(items)-1)

    _, _, cur_reg, cur_group, cur_stream = items[i]

    # perform the download
    download_client = boto3.client('logs', region_name=cur_reg)
    download_log_stream.download_log_stream(args.outdir, download_client, cur_group, cur_stream, args.timestart, args.timeend)

    # change status
    items[i][0] = "+"
    print("Download done.")


def test_interactive_download():
    args = arguments()

    items = [
        [' ', 0, 'us-east-2', '/aws/rds/instance/artem1/postgresql', 'artem1.0'],
        [' ', 1, 'us-east-2', '/aws/rds/instance/artem1/postgresql', 'artem1.0'],
        [' ', 2, 'us-east-2', '/aws/rds/instance/artem1/postgresql', 'artem1.0']
    ]

    while True:
        interactively_download(args, items)


if __name__ == "__main__":
    # test_interactive_download()
    args = arguments()

    items = get_possible_download_items()

    while True:
        interactively_download(args, items)
