from google.auth.transport.urllib3 import AuthorizedHttp
from google.auth import compute_engine
from google.oauth2 import service_account
import json


def export_image_to_cloud(project_id, timeout, source_image, image_format, destination_uri):
  '''
  project-id: The project ID for the project that contains the image that you want to export.
  timeout: The maximum time a build should last before it fails with a TIMEOUT message. In the API, the time must be specified in seconds. A timeout value of 7200s should work for most scenarios.
  source-image: Name of the image to be exported.
  image-format: Format of the exported image. Valid formats include vmdk, vhdx, vpc, vdi, and qcow2.
  destination-uri: The Cloud Storage URI location that you want to export the virtual disk file to. For example, gs://my-bucket/my-exported-image.vmdk.
  '''
  json_data = {
    "timeout": f"{timeout}",
    "steps":[
      {
        "args":[
          f"-timeout={timeout}",
          f"-source_image={source_image}",
          "-client_id=api",
          f"-format={image_format}",
          f"-destination_uri={destination_uri}"
        ],
        "name":"gcr.io/compute-image-tools/gce_vm_image_export:release",
        "env":[
          "BUILD_ID=$BUILD_ID"
        ]
      }
    ],
    "tags":[
      "gce-daisy",
      "gce-daisy-image-export"
    ]
  }

  return json.dumps(json_data)

def gen_body(image_name, zone, source_disk, location=None):
  '''
  project-id: The project to which the image belongs.
  image-name: A name for the new image that you want to create.
  zone: The zone where the source disk is located.
  source-disk: The disk from which you want to create the image.
  location: An optional parameter that lets you select the storage location of your image. For example, specify us to store the image in the us multi-region, or us-central1 to store it in the us-central1 region. If you don't make a selection, Compute Engine stores the image in the multi-region closest to your image's source location.
  [FORCE_CREATE]: An optional parameter that lets you create the image from a running instance. Specify TRUE only if you are sure that you want to create the image from a running instance. The default value if you do not specify this parameter is FALSE.
  '''
  json_body = {
    "name": f"{image_name}",
    "sourceDisk": f"/zones/{zone}/disks/{source_disk}",
    "forceCreate": "TRUE"  
  }

  return json.dumps(json_body)

def move():
  project_id = "gentle-pier-284510"
  credentials = service_account.Credentials.from_service_account_file('config.json')
  scoped_credentials = credentials.with_scopes(['https://www.googleapis.com/auth/cloud-platform'])
  authed_http = AuthorizedHttp(credentials=scoped_credentials)

  # Docs: https://cloud.google.com/compute/docs/images/create-delete-deprecate-private-images#api
  body_data = gen_body("newimage", "europe-west1-b", "instance-1-test")
  response = authed_http.request('POST', f"https://compute.googleapis.com/compute/v1/projects/{project_id}/global/images", body=body_data)
  print(json.loads(response.data))
  print("===== End First Stage =====")
  
  # Docs: https://cloud.google.com/compute/docs/images/export-image#api
  json_data = export_image_to_cloud("gentle-pier-284510", "7200s", "instance-1-test", "vmdk", "gs://test-example-com-marat-taram/image.tar.gz")
  response = authed_http.request('POST', f"https://cloudbuild.googleapis.com/v1/projects/{project_id}/builds", body=json_data)
  print(json.loads(response.data))
  print("===== End Second Stage =====")

if __name__ == '__main__':
  move()