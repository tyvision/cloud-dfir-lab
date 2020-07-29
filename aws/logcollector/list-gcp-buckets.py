#!/usr/bin/env python3
#
# Test with
# ./list-gcp-buckets.py
#
from google.oauth2 import service_account
from google.cloud import storage
import os

import importlib
lib_utils = importlib.import_module("lib-utils")

def get_parser():
    helptext="List buckets and their blobs in GCP."
    args = []
    return lib_utils.get_parser(helptext, args)

def build_client(gcp_secret_json=None):
    # there is a bug in credentials helper due to which we need to have our project set explicitly
    if gcp_secret_json:
        project=gcp_secret_json["project_id"]
        credentials = service_account.Credentials.from_service_account_info(gcp_secret_json)
    else:
        project = None
        credentials = None
    return storage.Client(project=project, credentials=credentials)

def list_gcp_buckets(gcp_secret_json=None):
    client = build_client(gcp_secret_json)

    res = {}
    for bucket in client.list_buckets():
        res[bucket.name] = []
        for blob in bucket.list_blobs():
            res[bucket.name].append(blob.name)

    return res

if __name__=='__main__':
    from pprint import pprint
    import json
    args = get_parser().parse_args()
    with open("../../GCP/CloudToken.json", "r") as f:
        creds = json.load(f)
    res = list_gcp_buckets(creds)
    pprint(res)
