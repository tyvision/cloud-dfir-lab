Automate working with cloud logs:
0) List and identify the interesting logs.
1) Download them.
2) Transform them.
3) Feed them into plaso as event sources.


Getting started with code:

0) Clone the repository
$ git clone https://github.com/tyvision/cloud-dfir-lab
$ cd cloud-dfir-lab/aws

1) Setup credentials by copying and editing aws-config.ini
$ mkdir ~/.aws/
$ cp config/example-aws-config.ini ~/.aws/config.ini
$ vim ~/.aws/config.ini

2) Install requirements and run scripts with python3. Check the script header for example arguments.
$ pip install -r config/requirements.txt
$ python code/cli-choose-logs.py --help


Getting started with Docker:

0) Clone the repository
$ git clone https://github.com/tyvision/cloud-dfir-lab
$ cd cloud-dfir-lab/aws

1) Setup aws-credentials.env file by copying and editing config/example-aws-credentials.env
$ cp config/example-aws-credentials.env aws-credentials.env
$ vim aws-credentials.env

2) Build docker image
$ docker build -t temach/cloud-1 -f docker/Dockerfile .

3) Create directory ./output in current dir
$ mkdir output

4) Run docker
$ docker run -it --env-file=aws-credentials.env --mount type=bind,src=$(pwd)/output,dst=/output temach/cloud-1

5) View log files
$ ls -la output
