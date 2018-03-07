FROM library/ubuntu:16.04

MAINTAINER Haines Zhang <zhmocean@gmail.com>

EXPOSE 8030

ADD ./setup /setup 
RUN chmod a+x /setup -R

ADD ./src/main/python /data/gallery
ADD ./requirement /data/gallery/requirement

RUN apt-get update && apt-get install python python-pip -y && apt-get clean  && pip install --no-cache-dir -r /data/gallery/requirement

ENTRYPOINT /setup/dockerstart.sh && python /data/gallery/server_bottle.py
