#!/usr/bin/env python
#
# Test with
# ./download-cloudwatch.py -r us-east-1 -s 2020-06-25 -e 2020-06-26 AWS/EC2 NetworkOut
#
import boto3
from botocore.config import Config

import argparse
from datetime import datetime

def arguments():
    parser = argparse.ArgumentParser(description='''
    Download logs from AWS.
    Credentials are read from ~/.aws/config or
    see https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html
    ''')

    parser.add_argument('namespace', type=str,
        help='Namespace where metric is hosted e.g. "AWS/EC2" or https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/aws-services-cloudwatch-metrics.html'
    )
    parser.add_argument('metric', type=str,
        help='Name of the metric e.g. "NetworkOut" or https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/viewing_metrics_with_cloudwatch.html'
    )
    parser.add_argument('-r', '--awsregion', type=str,
        help='AWS region e.g. us-east-1. Overwrites the region specified in ~/.aws/config'
    )
    parser.add_argument('-o', '--outdir', type=str, default="./",
        help='Path to output directory'
    )
    parser.add_argument('-s', '--timestart', type=datetime.fromisoformat,
        help='Start time for events in iso format e.g. 2020-07-14T00:33:24'
    )
    parser.add_argument('-e', '--timeend', type=datetime.fromisoformat,
        help='End time for events in iso format e.g. 2020-07-14T00:33:24'
    )

    return parser.parse_args()

def open_aws_entity(args):
    custom_config = Config(
        region_name=args.awsregion
    )

    # boto3 will automatically use parameters from custom Config if they are not None
    client = boto3.client('cloudwatch', config=custom_config)
    return client

def list_metrics(args, client):
    response = client.list_metrics(
        Namespace=args.namespace,
        MetricName=args.metric
    )

    print("Listing: ", response)

def get_statistics(args, client):
    response = client.get_metric_statistics(
        Namespace=args.namespace,
        MetricName=args.metric,
        Dimensions=[
            {
                'Name': 'InstanceType',
                'Value': 't2.micro'
            },
        ],
        StartTime=args.timestart,
        EndTime=args.timeend,
        Period=120,
        Statistics=[
            'Average'
        ],
        Unit='Kilobytes'
    )

    print('Result:', response)

if __name__=='__main__':
    args = arguments()
    client = open_aws_entity(args)
    list_metrics(args, client)
    get_statistics(args, client)
