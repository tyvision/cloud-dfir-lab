#!/usr/bin/env bash

# get the code working
ssh -i "../config/example_ec2_key" ubuntu@ec2-52-202-17-121.compute-1.amazonaws.com 'bash <<EOF
sudo apt-get update -y && sudo apt-get upgrade -y
sudo apt-get install -y python3-pip
mkdir -p ~/output/
mkdir -p ~/.aws/
EOF'

scp -i "../config/example_ec2_key"    ~/.aws/config ubuntu@ec2-52-202-17-121.compute-1.amazonaws.com:~/.aws/config
scp -i "../config/example_ec2_key" -r ../code       ubuntu@ec2-52-202-17-121.compute-1.amazonaws.com:~/
scp -i "../config/example_ec2_key" -r ../config     ubuntu@ec2-52-202-17-121.compute-1.amazonaws.com:~/

ssh -i "../config/example_ec2_key" ubuntu@ec2-52-202-17-121.compute-1.amazonaws.com 'bash <<EOF
pip3 install -r ~/config/requirements.txt
EOF'

# get docker working
# ssh -i "../config/example_ec2_key" ubuntu@ec2-52-202-17-121.compute-1.amazonaws.com 'bash <<EOF
# sudo apt-get update -y && sudo apt-get upgrade -y
# sudo apt-get install -y docker.io
# EOF'
# 
# scp ../aws-credentials.env  ubuntu@ec2-52-202-17-121.compute-1.amazonaws.com:~/aws-credentials.env
# 
# docker save temach/cloud-1 | ssh -i "../config/example_ec2_key" -C ubuntu@ec2-52-202-17-121.compute-1.amazonaws.com docker load
# 
# ssh -i "../config/example_ec2_key" ubuntu@ec2-52-202-17-121.compute-1.amazonaws.com 'bash <<EOF
# echo docker run -it --env-file=aws-credentials.env --mount type=bind,src=$(pwd)/output,dst=/output temach/cloud-1
# # docker run -d --env-file=aws-credentials.env --mount type=bind,src=$(pwd)/output,dst=/output temach/cloud-1
# EOF'



