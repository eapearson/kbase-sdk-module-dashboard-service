FROM python:2.7.14
MAINTAINER KBase Developer
# -----------------------------------------

# Insert apt-get instructions here to install
# any required dependencies for your module.

# update system and system dependencies
RUN apt-get update \
    && apt-get -y upgrade \
    && apt-get -y dist-upgrade \
    && apt-get -y autoremove \
    && apt-get -y install default-jdk ant vim sqlite3

# install python dependencies
RUN pip install --upgrade pip \
    && pip install coverage \
    && pip install jinja2 \
    && pip install uwsgi \
    && pip install jsonrpcbase \
    && pip install pylru \
    && pip install bsddb3 \
    && pip install nose \
    && pip install 'requests[security]' \
    && pip install 'python-dateutil==2.7.2' \
    && pip install cffi \
    && pip install ndg-httpsclient \
    && pip install pyasn1 

# -----------------------------------------
COPY ./ /kb/module

RUN git clone --depth=1 https://github.com/kbase/kb_sdk /kb/kb_sdk \
    && cd /kb/kb_sdk \
    && make

RUN mkdir -p /kb/module/work/cache \
    && chmod -R a+rw /kb/module

WORKDIR /kb/module
ENV PATH="$PATH:/kb/kb_sdk/bin"

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
