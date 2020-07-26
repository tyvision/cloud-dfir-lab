# Test with
# docker build -t name/tag -f docker/Dockerfile .
#
# Test with
# docker run -it --env-file docker-credentials.env name/tag
#
FROM debian:latest

RUN apt-get update
RUN apt-get install -y python3 python3-pip

WORKDIR /root/cloud-dfir

COPY ./config/requirements.txt ./
RUN pip3 install -r requirements.txt

COPY ./logcollector/*.py ./

# the code expects environment variables, here they are left empty
ENV AWS_ACCESS_KEY_ID=
ENV AWS_SECRET_ACCESS_KEY=

CMD ["sleep", "infinity"]
# CMD ["./frontend-cli.py"]
# CMD ["/bin/sh"]
