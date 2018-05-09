FROM python:2.7.14
MAINTAINER KBase Developer
# -----------------------------------------

# Insert apt-get instructions here to install
# any required dependencies for your module.

RUN apt-get update \
    && apt-get -y upgrade \
    && apt-get -y dist-upgrade \
    && apt-get -y autoremove \
    && apt-get -y install default-jdk ant vim sqlite3

RUN pip install --upgrade pip \
    && pip install coverage \
    && pip install jinja2 \
    && pip install uwsgi \
    && pip install jsonrpcbase \
    && pip install pylru \
    && pip install bsddb3 \
    && pip install nose \
    && pip install 'python-dateutil==2.7.2'

# update security libraries in the base image
# in this modified dockerfile, we are installing or upgrading 
# depends what is in the core python image.
# TODO: document that here
RUN pip install cffi --upgrade \
    && pip install pyopenssl --upgrade \
    && pip install ndg-httpsclient --upgrade \
    && pip install pyasn1 --upgrade \
    && pip install requests --upgrade \
    && pip install 'requests[security]' --upgrade

# -----------------------------------------
RUN git clone --depth=1 https://github.com/kbase/kb_sdk /kb/kb_sdk \
    && cd /kb/kb_sdk   \
    && make


COPY ./deployment/docker/context/contents /kb/module
RUN chmod -R a+rw /kb/module
RUN mkdir -p /kb/module/work/cache

WORKDIR /kb/module

RUN PATH=$PATH:/kb/kb_sdk/bin make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
