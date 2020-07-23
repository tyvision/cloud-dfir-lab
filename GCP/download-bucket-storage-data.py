import os
from os import makedirs
from os.path import join, isdir, isfile, basename
from google.cloud import storage

current_directory = os.path.abspath(os.getcwd())

storage_client = storage.Client()

def down(bucket_name):

    prefix = '' #nado dopilit...
    
    bucket = storage_client.bucket(bucket_name=bucket_name)
    blobs = bucket.list_blobs(prefix=prefix)

    for blob in blobs:
        blob_fs_name = basename(blob.name)
        print("Download: `" + basename(blob_fs_name) + "`")
        blob.download_to_filename(blob_fs_name)

    print("All done")

def listBucket():
    for bucket in storage_client.list_buckets():
        print(bucket)

print("If u wont to see the list of Buckets press `1` or press `2` to download Bucket")

value = input()

if value == "1":
    listBucket()
elif value == "2":
    print("Put 'Name of bucket'.")
    valya1 = input()
    down(valya1)
else:
    print("vasya pidr")
