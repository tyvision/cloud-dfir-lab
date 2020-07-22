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
