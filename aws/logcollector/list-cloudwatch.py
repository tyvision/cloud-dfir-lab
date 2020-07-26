#!/usr/bin/env python
#
# Test with
# ./list-cloudwatch.py us-east-2 AWS/EC2 NetworkOut
#
import boto3
import json

from pprint import pprint

import importlib
lib_utils = importlib.import_module("lib-utils")


def get_parser():
    helptext="List metrics available in Cloud Watch."
    args = [
        "region"
        , "namespace"
        , "metric"
        , "outdir"
    ]
    return lib_utils.get_parser(helptext, args)


def list_metric(region_name, namespace, metric, outdir):
    client = boto3.client('cloudwatch', region_name=region_name)

    responce = client.list_metrics(
        Namespace=namespace,
        MetricName=metric
    )

    return responce


if __name__=='__main__':
    args = get_parser().parse_args()

    res = list_metric(args.region, args.namespace, args.metric, args.outdir)
    pprint(res)
