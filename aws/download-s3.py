import boto3
import os

# supply configuration
# see https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html
# best way is to rely on aws config file set by AWS_CONFIG_FILE environment variable

def download_dir_from_s3(local_dir, bucket_name, dir_prefix):
    s3_resource = boto3.resource('s3')
    bucket = s3_resource.Bucket(bucket_name)
    for obj in bucket.objects.filter(Prefix = dir_prefix):
        dest_path = os.path.join(local_dir, obj.key)
        if not os.path.exists(os.path.dirname(dest_path)):
            os.makedirs(os.path.dirname(dest_path))
        bucket.download_file(obj.key, dest_path)


download_dir_from_s3("tmp", "artembucket2.testdom1.co.uk", "test")
