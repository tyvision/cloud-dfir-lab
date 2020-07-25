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

1) Verify ansible inventory

```
# cd ansible/
# ansible -i inventory.yml all --list-hosts
```

2) Execute playbook

```
# cd ansible/
# ansible-playbook -i inventory.yml deploy.yml
```



**Developing Ansible scripts**

Its best to test them against a VM. Use vagrant to get Ubuntu 18.04:

```
# mkdir vm1
# cd vm1
# vagrant init hashicorp/bionic64
# vagrant up
```

Edit Vagrant file to allow ports and set memory limits.
Initial connection must be done vagrant ssh, then possible to use plain ssh.
```
# cd vm1
# vagrant ssh
# ssh -i .vagrant/machines/default/virtualbox/private_key vagrant@127.0.0.1 -p 2222
```



## Getting started with Docker:

0) Clone the repository
```
# git clone https://github.com/tyvision/cloud-dfir-lab
# cd cloud-dfir-lab/aws
```
1) Setup credentials file by copying and editing config/example-docker-credentials.env

```
# cp config/example-docker-credentials.env docker-credentials.env
# vim docker-credentials.env
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
# docker run -it --env-file=docker-credentials.env --mount type=bind,src=$(pwd)/output,dst=/output temach/cloud-1
```

5) View log files

```
# ls -la ./output/
```



## Getting started with docker-compose

0) Clone the repository

```
# git clone https://github.com/tyvision/cloud-dfir-lab
# cd cloud-dfir-lab/aws
```

1) Setup environment variables.

You can either directly export them into your shell:

```
export AWS_ACCESS_KEY_ID=XXX
export AWS_SECRET_ACCESS_KEY=XXX
```

Or you can source them from file:

```
# cp config/example-aws-credentials.sh aws-credentials.sh
# vim aws-credentials.sh
# source aws-credentials.sh
```

2) Run docker-compose

```
# cd docker/
# docker-compose up
```

3) Access logcollector to collect logs from cloud.

4) Aceess Timesketch to view events from collected logs on `http://localhost:80`



**Security issue**

The services in docker-compose bind to  0.0.0.0, that is they listen on all interfaces. This is a security problem, because the services (timesketch,  elasticsearch, postgres, etc) are exposed to the internet. And timesketch does not even use HTTPS.

Protect the services by preventing public access to them (to their ports). They should be accessible only via localhost on the laboratory machine. 



**Remote access to secured services**
If the laboratory machine is running in the cloud, it will have SSH access. Therefore two simple ways to access the services:

**HTTP over SSH**
Investigator can use HTTP over SSH to access the services. See: https://ma.ttias.be/socks-proxy-linux-ssh-bypass-content-filters/
The SSH tunnel is created on the investigator's client machine:

```
ssh -i private_key -D 8080 -q -C -N vagrant@127.0.0.1 -p 2222
```

**X over SSH**
Install Xorg-server and a web browser into the laboratory machine. Forward X over SSH:

```
ssh -X -i private_key vagrant@127.0.0.1 -p 2222
```



**Securing services from public access**

Unfortunatelly docker can not be restricted to an interface. The default interface can be set, but it is not restrictive. See: https://docs.docker.com/network/iptables/#setting-the-default-bind-address-for-containers

There are three options, the iptable option is currently implemented.

**Option 1: Using iptables rules**
Use the iptable rules to make the laboratory machine drop new connections if they are not SSH. This rule can be added to INPUT chain or DOCKER-USER chain. Better to add the rule to specific WAN interface e.g. `eth0` so it will not disturb system interfaces e.g. `loopback`, `docker0`. As a result, although the service listens on 0.0.0.0 no new connection can be established with it. 

**Option 2: Using special ports notation**
Special notation for ports: https://docs.docker.com/compose/compose-file/#ports
See also: https://stackoverflow.com/questions/56053824/how-to-restrict-that-a-docker-container-only-listens-connection-from-localhost

```
ports:
  - "127.0.0.1:8001:8001"
```

However this does not work. The outside connections are still accepted: 

```
# sudo netstat -lntp | head
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 127.0.0.1:80            0.0.0.0:*               LISTEN      16505/docker-proxy
tcp        0      0 127.0.0.1:9200          0.0.0.0:*               LISTEN      15271/docker-proxy
tcp        0      0 127.0.0.1:9300          0.0.0.0:*               LISTEN      15259/docker-proxy
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      540/sshd: /usr/bin/
```

**Option 3: Use docker internal network**
Set up an internal network: https://docs.docker.com/compose/compose-file/#internal
The default network is the one that gets created looking like: `[projectname]_default`
See https://docs.docker.com/compose/networking/#configure-the-default-network

```
networks:
  default:
    internal: true
```

However this does not work as default network is not accessiable even to localhost.



## Getting started with Timesketch:

Clone, use the e2e directory. Its for end-to-end testing and does not have debug flags. Add kibana crate:

```
kibana:
    image: kibana:7.6.2
    ports:
	  - "5601:5601"
  	environment:
      ELASTICSEARCH_URL: http://elasticsearch:9200
      ELASTICSEARCH_HOST: http://elasticsearch:9200
```

Set timesketch USER and PASSWORD to admin:admin.

Run compose. 

For kibana: localhost:5601
For timesketch: localhost:80

For postgres: docker attach to container. Then "psql --username=timesketch --password=password".
See databases: \list
See tables: \dt

Try importing test events: aws/config/example-events.jsonl
For some readon web interface does not work.

Using command line works:

Docker cp example-events.jsonl into `e2e_timesketch_1` container. Then attach to that container.

```
# docker cp example-events.jsonl e2e_timesketch_1:/
# docker exec -it e2e_timesketch_1 /bin/bash
```

Use tsctl to import.

```
# tsctl list_sketches
# tsctl import --sketch_id 1 --file example-events.jsonl --timeline_name test1 --user admin

```

To view data in Kibana create index pattern and get all messages.
Also can go to dev tools and execute queries directly against elastic database.


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

To get all documents from particular index "myindexname":
```
GET /myindexname/_search?size=200
{
    "query" : {
        "match_all" : {}
    }
}
```


Below is how data gets stored when imported with "tsctl import" cli tool from index 6ae91f0374634aa9a06186e9110d6989:

```
      {
        "_index" : "6ae91f0374634aa9a06186e9110d6989",
        "_type" : "_doc",
        "_id" : "K0WOfHMB12F-ZfcnOtiQ",
        "_score" : 1.0,
        "_source" : {
          "message" : "A message",
          "timestamp" : 123456789,
          "datetime" : "2015-07-24T19:01:01",
          "timestamp_desc" : "Write time",
          "extra_field_1" : "foo"
        }
      },
      {
        "_index" : "6ae91f0374634aa9a06186e9110d6989",
        "_type" : "_doc",
        "_id" : "LEWOfHMB12F-ZfcnOtiQ",
        "_score" : 1.0,
        "_source" : {
          "message" : "Another message",
          "timestamp" : 123456790,
          "datetime" : "2015-07-24T19:01:02",
          "timestamp_desc" : "Write time",
          "extra_field_1" : "bar"
        }
      },
      {
        "_index" : "6ae91f0374634aa9a06186e9110d6989",
        "_type" : "_doc",
        "_id" : "LUWOfHMB12F-ZfcnOtiQ",
        "_score" : 1.0,
        "_source" : {
          "message" : "Yet more messages",
          "timestamp" : 123456791,
          "datetime" : "2015-07-24T19:01:03",
          "timestamp_desc" : "Write time",
          "extra_field_1" : "baz"
        }
      }
```



## Getting started with Logstsah

After timesketch stack is up and running the next step is to load data.

Get logstash docker container that is the same version as elxasticsearch used in timesketch - 7.6.2
Also attach to the same docker network where timesketch is running.

```
# docker pull logstash:7.6.2
# cd aws
# mkdir output
# docker run -it --network e2e_default --mount type=bind,src=$(pwd)/config/,dst=/conf --mount type=bind,src=$(pwd)/output,dst=/input logstash:7.6.2 /bin/bash
```

For debug run bash and start logstash manually, you should see it parse the logs.
```
# logstash --verbose -f /conf/logstash-simple.conf
```

After every run logstash saves data bout progress wih respect to file into a sincedb file.
This causes problems during development, because it does not re-read old logs. See https://stackoverflow.com/questions/32742379/logstash-file-input-glob-not-working

Best solution is to remove old sincedb files and set `[input][file][start_position] = beginning` to
tell logstash that is must re-parse log files fully each time. Optionally set `[input][file][sincedb_path] => "/dev/null"` this will stop writing new sincedb files, but you still need to delete old ones, because they are still read on startup.

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

Output will be on stdout.
Note json_lines plugin for file does NOT work, but json plugin works.

Here is how data imported with logstash looks (compare with that imported by tsctl) from index `logstash-2020.07.24-000001`:

```
      {
        "_index" : "logstash-2020.07.24-000001",
        "_type" : "_doc",
        "_id" : "Q7RHgXMBzy7j0CFDpY-O",
        "_score" : 1.0,
        "_source" : {
          "@timestamp" : "2020-07-24T14:43:42.789Z",
          "extra_field_1" : "bar",
          "host" : "9f4af4e57c19",
          "message" : "Another message Logstash try1",
          "datetime" : "2015-07-24T19:01:02",
          "timestamp" : 123456790,
          "timestamp_desc" : "Write time",
          "@version" : "1",
          "path" : "/input/file_1.jsonl"
        }
      },
      {
        "_index" : "logstash-2020.07.24-000001",
        "_type" : "_doc",
        "_id" : "QrRHgXMBzy7j0CFDpY-N",
        "_score" : 1.0,
        "_source" : {
          "@timestamp" : "2020-07-24T14:43:42.757Z",
          "extra_field_1" : "foo",
          "host" : "9f4af4e57c19",
          "message" : "A message Logstash try1",
          "datetime" : "2015-07-24T19:01:01",
          "timestamp" : 123456789,
          "timestamp_desc" : "Write time",
          "@version" : "1",
          "path" : "/input/file_1.jsonl"
        }
      },
      {
        "_index" : "logstash-2020.07.24-000001",
        "_type" : "_doc",
        "_id" : "QbRHgXMBzy7j0CFDpY-N",
        "_score" : 1.0,
        "_source" : {
          "@timestamp" : "2020-07-24T14:43:42.790Z",
          "extra_field_1" : "baz",
          "host" : "9f4af4e57c19",
          "message" : "Yet more messages Logstash try1",
          "datetime" : "2015-07-24T19:01:03",
          "timestamp" : 123456791,
          "timestamp_desc" : "Write time",
          "@version" : "1",
          "path" : "/input/file_1.jsonl"
        }
      }
```



## Problem with Logstash + Timesketch

In Timesketch a sketch is made up of timelines. Each timeline is stored in a separate index in the Elasticsearch database. The events of the timeline each become a document in the index. So a timeline with 3 events results in a new index with 3 documents.

Below I imported two timelines into timesketch, one uses index 6ae91f0374634aa9a06186e9110d6989 in elasticsearch database and another uses index 86ed7402923a428eb415649222e69694.

When importing a timeline in timesketch, we can see the index name created in postgres in table searchindex.

```
timesketch=# select * from searchindex;
 id |         created_at         |         updated_at         |       name       |   description    |            index_name            | user_id
----+----------------------------+----------------------------+------------------+------------------+----------------------------------+---------
  1 | 2020-07-23 16:42:41.040877 | 2020-07-23 16:42:41.040877 | test1            | test1            | 6ae91f0374634aa9a06186e9110d6989 |       1
  2 | 2020-07-24 14:56:20.811376 | 2020-07-24 14:56:20.811376 | example-events-2 | example-events-2 | 86ed7402923a428eb415649222e69694 |       1
(2 rows)

```

The extract from elastic database showing all the indices:
```
health status index                            uuid                   pri rep docs.count docs.deleted store.size pri.store.size
yellow open   6ae91f0374634aa9a06186e9110d6989 nvET5RTcT_S9wNPVAv8oUw   1   1          3            0      5.6kb          5.6kb
green  open   .kibana_task_manager_1           BibfRLY2QomU4bqy_7O74g   1   0          2            2     20.4kb         20.4kb
yellow open   86ed7402923a428eb415649222e69694 YvXcYeuoRiChCGU1Q-jV1Q   1   1          3            0      5.6kb          5.6kb
green  open   ilm-history-1-000001             po6qdqTiQbCblI85NZTbzA   1   0         18            0     25.6kb         25.6kb
green  open   .apm-agent-configuration         J3IqgvGsSSiQK53jiXxHjg   1   0          0            0       283b           283b
yellow open   logstash-2020.07.24-000001       PF8Iwb_pS9iwA3DvF5Ze4Q   1   1          3            0     13.4kb         13.4kb
green  open   .kibana_1                        axp3KbomQCSZtNl-0d2QVw   1   0         11            0     86.2kb         86.2kb
```

The same index names 86ed7402923a428eb415649222e69694 and 6ae91f0374634aa9a06186e9110d6989 are found here.
Also note the index name logstash-2020.07.24-000001 which was created automatically by logstash, when importing.

So while its possible to insert data into db with logstash, to make it work with Timeksketch we need to also insert meta-data into the Postgres DB. Otherwise timesketch will not know how to use the data. On the other hand we can modify Logstash config to specify explicitly the index where data should be placed, however for that we still need to get access to postgres DB because the index names are randomly generated and not visible in Timesketch interface.

Both of the above are poor solutions to implement.



