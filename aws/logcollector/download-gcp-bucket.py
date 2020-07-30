#!/usr/bin/env python3
#
# Test with
# ./download-gcp-bucket.py 'save-logs' -o tmp
#
from google.oauth2 import service_account
from google.cloud import storage
import os

import importlib
lib_utils = importlib.import_module("lib-utils")

def get_parser():
    helptext="Download buckets from GCP."
    args = [
        "bucket"
        , "prefix"
        , "outdir"
    ]
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

def download_blob_to_path(bucket_name, prefix, dest_path, gcp_secret_json=None):
    client = build_client(gcp_secret_json)
    bucket = client.bucket(bucket_name=bucket_name)
    blob = storage.blob.Blob(prefix, bucket)
    blob.download_to_filename(dest_path)

def download_dir_from_gcp(bucket_name, prefix, outdir, gcp_secret_json=None):
    client = build_client(gcp_secret_json)
    bucket = client.bucket(bucket_name=bucket_name)

    for blob in bucket.list_blobs(prefix=prefix):
        dest_path = os.path.join(outdir, blob.name)

        # make folder paths
        if not os.path.exists(os.path.dirname(dest_path)):
            try:
                os.makedirs(os.path.dirname(dest_path))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        # download the file
        blob.download_to_filename(dest_path)

if __name__=='__main__':
    args = get_parser().parse_args()
    import json
    with open("../../GCP/CloudToken.json", "r") as f:
        creds = json.load(f)
    download_dir_from_gcp(args.bucket, args.prefix, args.outdir, gcp_secret_json=creds)
