# Main doc: https://www.terraform.io/docs/providers/aws/index.html
# for each stanza see the appropriate docs
# e.g. for data "aws_ami" see https://www.terraform.io/docs/providers/aws/d/ami.html
# e.g. for resource "aws_instance" see https://www.terraform.io/docs/providers/aws/r/instance.html
# to find possible AWS AMI see https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/finding-an-ami.html
# to connect is something like: ssh -i "example_ec2_key.pem" ubuntu@ec2-52-202-17-121.compute-1.amazonaws.com
# terraform state is stored in s3 backend. See: https://www.terraform.io/docs/backends/types/s3.html

terraform {
  backend "s3" {
    bucket = "terraform.testdom1.co.uk"
    key    = "cloud-dfir-lab/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  profile = "default"
  region  = "us-east-1"
}

data "aws_ami" "latest_bionic_ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-bionic-18.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

resource "aws_key_pair" "example_ec2" {
  key_name   = "example_ec2_key"
  # to create key file automatically look into terraform provisioner "local-exec"
  public_key = file("../config/example_ec2_key.pub")

  tags = { CreatedBy = "terraform" }
}


resource "aws_instance" "logcollector" {
  key_name      = aws_key_pair.example_ec2.key_name
  ami           = data.aws_ami.latest_bionic_ubuntu.id
  instance_type = "t2.medium"
  security_groups = ["allowall"]

  tags = { CreatedBy = "terraform" }
}

resource "aws_eip" "logcollector_eip" {
  vpc      = true
  instance = aws_instance.logcollector.id

  tags = { CreatedBy = "terraform" }
}
