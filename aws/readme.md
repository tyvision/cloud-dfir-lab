# AWS Cloud DFIR

0) List and identify the interesting logs.

1) Download them.

2) Feed into Timesketch as events.

3)  Analyse in Timesketch.



## Getting started with code

Every python script has example command line of how to run it in the file header.

Every python script has a  `--help` argument.



0) Clone the repository

```
# git clone https://github.com/tyvision/cloud-dfir-lab
# cd cloud-dfir-lab/aws
```

1) Setup credentials by copying and editing aws-config.ini (for windows the path is: `%UserProfile%\.aws\config`)

```
# mkdir ~/.aws/
# cp config/example-aws-config.ini ~/.aws/config
# vim ~/.aws/config
```

2) Install requirements and run scripts with python3.

```
# pip install -r config/requirements.txt
# python code/cli-choose-logs.py --help
```



## Getting started with Terraform

Useful link:  https://learn.hashicorp.com/terraform/getting-started/install.html

Terraform state is stored remotely in S3 bucket, see `terraform` directive in .tf files.

0) Clone the repository
```
# git clone https://github.com/tyvision/cloud-dfir-lab
# cd cloud-dfir-lab/aws
```

1) Setup credentials by copying and editing aws-config.ini (for windows the path is: `%UserProfile%\.aws\config`)

```
# mkdir ~/.aws/
# cp config/example-aws-config.ini ~/.aws/config
# vim ~/.aws/config
```

3) Install terraform

4) Install aws command line utility (to use the aws terraform provider).

5) Copy security config so terraform will read AWS security tokens ( `~/.aws/config` is not read)

```
# cp ~/.aws/config ~/.aws/credentials
```

6) Review terraform recipe and create you own SSH key file for the deployed instances.

7) Create infrastructure 

```
# cd terraform/
# terraform init
# terraform show
```



## Getting started with Ansible

Playbook is made to run against infrastructure created by terraform. 

0) Check inventory.yml to make sure the correct SSH key and user are set for the instances.

1) Check that ansible inventory

```
# cd ansible/
# ansible -i inventory.yml all --list-hosts
```

2) Execute playbook

```
# cd ansible/
# ansible-playbook -i inventory.yml deploy.yml
```



## Getting started with Docker:

0) Clone the repository
```
# git clone https://github.com/tyvision/cloud-dfir-lab
# cd cloud-dfir-lab/aws
```
1) Setup aws-credentials.env file by copying and editing config/example-aws-credentials.env

```
# cp config/example-aws-credentials.env aws-credentials.env
# vim aws-credentials.env
```
2) Build docker image

```
# docker build -t temach/cloud-1 -f docker/Dockerfile .
```

3) Create directory ./output in current dir

```
# mkdir output
```

4) Run docker

```
# docker run -it --env-file=aws-credentials.env --mount type=bind,src=$(pwd)/output,dst=/output temach/cloud-1
```

5) View log files

```
# ls -la ./output/
```



## Getting started with Timesketch:

Clone, use the e2e directory. Its for end-to-end testing and does not have debug flags. Add kibana crate:


  kibana:
    image: kibana:7.6.2
    ports:
      - "5601:5601"
    environment:
      ELASTICSEARCH_URL: http://elasticsearch:9200
      ELASTICSEARCH_HOST: http://elasticsearch:9200

Set timesketch USER and PASSWORD to admin:admin.

Run compose. 


For kibana: localhost:5601
For timesketch: localhost:80

For postgres docker attach to container. Then "psql --username=timesketch --password=password".
See databases: \list
See tables: \dt

Try importing test events: aws/config/example-events.jsonl
For some readon web interface does not work.

Using command line works:

Docker cp example-events.jsonl into `e2e_timesketch_1` container.

```
# docker cp example-events.jsonl e2e_timesketch_1:/
# docker exec -it e2e_timesketch_1 /bin/bash
```

Attach to docker container.
Use tsctl to import.
```
# tsctl list_sketches
# tsctl import --sketch_id 1 --file example-events.jsonl --timeline_name test1 --user admin

```


To view data in Kibana create index pattern and get all messages.
Also can go to dev tools and execute queries directly agains elastic database.


To View all documents for all indices (note parameter size=200, because by default size is 10):

```
GET /_all/_search?size=200
{
  "query": {
    "match_all": {}
  }
}
```

Also list all indices:
```
GET _cat/indices?v
```

To get data about the contents of DB use GET index:
```
Get 6ae91f0374634aa9a06186e9110d6989
```


How example data is stored in Elastic:

```
   {
        "_index": "6ae91f0374634aa9a06186e9110d6989",
        "_type": "_doc",
        "_id": "K0WOfHMB12F-ZfcnOtiQ",
        "_version": 1,
        "_score": 0,
        "_source": {
          "message": "A message",
          "timestamp": 123456789,
          "datetime": "2015-07-24T19:01:01",
          "timestamp_desc": "Write time",
          "extra_field_1": "foo"
        },
        "fields": {
          "datetime": [
            "2015-07-24T19:01:01.000Z"
          ]
        }
      },
      {
        "_index": "6ae91f0374634aa9a06186e9110d6989",
        "_type": "_doc",
        "_id": "LEWOfHMB12F-ZfcnOtiQ",
        "_version": 1,
        "_score": 0,
        "_source": {
          "message": "Another message",
          "timestamp": 123456790,
          "datetime": "2015-07-24T19:01:02",
          "timestamp_desc": "Write time",
          "extra_field_1": "bar"
        },
        "fields": {
          "datetime": [
            "2015-07-24T19:01:02.000Z"
          ]
        }
      },
      {
        "_index": "6ae91f0374634aa9a06186e9110d6989",
        "_type": "_doc",
        "_id": "LUWOfHMB12F-ZfcnOtiQ",
        "_version": 1,
        "_score": 0,
        "_source": {
          "message": "Yet more messages",
          "timestamp": 123456791,
          "datetime": "2015-07-24T19:01:03",
          "timestamp_desc": "Write time",
          "extra_field_1": "baz"
        },
        "fields": {
          "datetime": [
            "2015-07-24T19:01:03.000Z"
          ]
        }
      }

```


## Getting started with Logstsah

After timesketch stack is up and running the next step is to load data.

Get logstash docker container that is the same version as elxasticsearch used in timesketch - 7.6.2

```
# docker pull logstash:7.6.2
# cd aws
# mkdir output
# docker run -it --mount type=bind,src=$(pwd)/config/,dst=/conf --mount type=bind,src=$(pwd)/output,dst=/input logstash:7.6.2 /bin/bash
```

For debug run bash and start logstash manually, you should see it parse the logs.
```
# logstash --verbose -f /conf/logstash-simple.conf
```

After every run logstash saves data bout progress wih respect to file into a sincedb file.
This causes problems during development, because it does not re-read old logs. See https://stackoverflow.com/questions/32742379/logstash-file-input-glob-not-working

Best solution is to remove old sincedb files and set [input][file] option [start_position] = beginning to
tell logstash that is must re-parse log files fully each time. Optionally set [input][file][sincedb_path] => "/dev/null"
this will stop writing new sincedb files, but you still need to delete old ones, because they are still read on startup.

To delete old sincedb files use the below to find them:
```
cd /
find . | grep sincedb
```

They are actually part of the file plugin.


To add new events and see how they work use:
```
# cd aws
# cat config/example-events-logstash-1.jsonl >> output/file_2.jsonl
```

Outout should be on stdout.
Note json_lines plugin for file does NOT work, but json plugin works.
