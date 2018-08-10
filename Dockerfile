FROM alpine:3.8 as builder
MAINTAINER KBase Developer

# update system and system dependencies
RUN apk upgrade --update-cache --available \
    && apk add --update --no-cache \
        linux-headers=4.4.6-r2 \
        sqlite=3.24.0-r0 \
        git=2.18.0-r0 \
        make=4.2.1-r2 \
        bash=4.4.19-r1 \
        libffi-dev=3.2.1-r4 \
        openssl-dev=1.0.2o-r2 \
        python2=2.7.15-r0 \
        python2-dev=2.7.15-r0 \
        py2-pip=10.0.1-r0 \
        g++=6.4.0-r8 \
        openjdk8=8.171.11-r0 \
        apache-ant=1.10.4-r0

# install python dependencies
RUN pip install --upgrade pip \
    && pip install 'coverage==4.5.1' \
    && pip install 'jinja2==2.10' \
    && pip install 'uwsgi==2.0.17.1' \
    && pip install 'jsonrpcbase==0.2.0' \
    && pip install 'nose==1.3.7' \
    && pip install 'requests==2.19.1' \
    && pip install 'python-dateutil==2.7.2' \
    && pip install 'cffi==1.11.5' \
    && pip install 'ndg-httpsclient==0.5.1' \
    && pip install 'pyasn1==0.4.4'

# apsw is a much better sqlite3 library than provided with Pyhton.
# also beware: the apsw distributed through pip is NOT the official version
# and is hopelessly out of date.
RUN pip install https://github.com/rogerbinns/apsw/releases/download/3.24.0-r1/apsw-3.24.0-r1.zip \
    --global-option=fetch --global-option=--version --global-option=3.24.0 --global-option=--all \
    --global-option=build --global-option=--enable-all-extensions

RUN mkdir -p /kb \
    && git clone --depth=1 https://github.com/kbase/kb_sdk /kb/kb_sdk \
    && cd /kb/kb_sdk \
    && make

COPY ./ /kb/module

RUN mkdir -p /kb/module/work/cache \
    && chmod -R a+rw /kb/module \
    && cd /kb/module \
    && PATH=$PATH:/kb/kb_sdk/bin make install

FROM alpine:3.8
MAINTAINER KBase Developer

# update system and system dependencies
RUN apk upgrade --update-cache --available \
    && apk add --update --no-cache \
        linux-headers=4.4.6-r2 \
        sqlite=3.24.0-r0 \
        git=2.18.0-r0 \
        make=4.2.1-r2 \
        bash=4.4.19-r1 \
        libffi-dev=3.2.1-r4 \
        openssl-dev=1.0.2o-r2 \
        python2=2.7.15-r0 \
        python2-dev=2.7.15-r0 \
        py2-pip=10.0.1-r0 \
        g++=6.4.0-r8

# install python dependencies
RUN pip install --upgrade pip \
    && pip install 'jinja2==2.10' \
    && pip install 'uwsgi==2.0.17.1' \
    && pip install 'jsonrpcbase==0.2.0' \
    && pip install 'requests==2.19.1' \
    && pip install 'python-dateutil==2.7.2' \
    && pip install 'cffi==1.11.5' \
    && pip install 'ndg-httpsclient==0.5.1' \
    && pip install 'pyasn1==0.4.4'

RUN pip install https://github.com/rogerbinns/apsw/releases/download/3.24.0-r1/apsw-3.24.0-r1.zip \
--global-option=fetch --global-option=--version --global-option=3.24.0 --global-option=--all \
--global-option=build --global-option=--enable-all-extensions

COPY --from=builder /kb/module /kb/module

WORKDIR /kb/module

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
