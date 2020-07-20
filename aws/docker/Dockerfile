# Test with
# docker build -t name/tag -f docker/Dockerfile .
#
# Test with
# docker run -it --env-file docker-credentials.env --mount type=bind,src=$(pwd)/output,dst=/output name/tag /bin/sh
#
FROM alpine:latest

# the code expects environment variables via --env-file
ENV AWS_ACCESS_KEY_ID=XXX
ENV AWS_SECRET_ACCESS_KEY=XXX

RUN apk add --no-cache python3

WORKDIR /root/cloud-dfir

COPY ./config/requirements.txt ./
RUN pip3 install -r requirements.txt

COPY ./code/*.py ./

# to extract downloaded log files mount to local ./output directory via --mount
CMD ["./cli-choose-logs.py", "-o", "/output"]
# CMD ["/bin/sh"]
