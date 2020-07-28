#!/usr/bin/env python
#
# Test with
# ./download-cloudwatch.py us-east-2 AWS/EC2 NetworkOut -s 2020-06-01T00:00:00 -e 2020-07-20T00:00:00
#
# Test api with
# aws cloudwatch get-metric-statistics \
#    --region us-east-2 \
#    --namespace AWS/EC2 \
#    --metric-name NetworkOut \
#    --period 3600  --statistics "Average" \
#    --start-time 2020-06-01T23:18:00 \
#    --end-time 2020-07-20T23:18:00
#
import boto3
import json

from pprint import pprint

import importlib
lib_utils = importlib.import_module("lib-utils")


def get_parser():
    helptext="Download metrics from Cloud Watch."
    args = [
        "region"
        , "namespace"
        , "metric"
        , "outdir"
        , "timestart"
        , "timeend"
    ]
    return lib_utils.get_parser(helptext, args)


def download_metric(region, namespace, metric, timestart, timeend, aws_id=None, aws_secret=None):
    client = boto3.client('cloudwatch', region_name=region, aws_access_key_id=aws_id, aws_secret_access_key=aws_secret)

    responce = client.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric,
        # Dimensions=[
        #     {
        #         'Name': 'InstanceType',
        #         'Value': 't2.micro'
        #     },
        # ],
        StartTime=timestart,
        EndTime=timeend,
        Period=3600,
        Statistics=[
            'Average'
        ],
        Unit='Bytes'
    )

    return responce


if __name__=='__main__':
    args = get_parser().parse_args()
    res = download_metric(args.region, args.namespace, args.metric, args.timestart, args.timeend)
    pprint(res)
