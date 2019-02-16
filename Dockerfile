FROM alpine:3.9 as builder
MAINTAINER KBase Developer

# update system and system dependencies
RUN apk upgrade --update-cache --available \
    && apk add --update --no-cache \
    apache-ant=1.10.5-r0 \
    bash=4.4.19-r1 \
    git=2.20.1-r0 \
    linux-headers=4.18.13-r1 \
    make=4.2.1-r2 \
    openjdk8=8.191.12-r0


RUN apk add --no-cache python3=3.6.8-r1 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache

RUN mkdir -p /kb \
    && git clone --depth=1 https://github.com/kbase/kb_sdk /kb/kb_sdk \
    && cd /kb/kb_sdk \
    && make

COPY ./ /kb/module

RUN mkdir -p /kb/module/work/cache \
    && chmod -R a+rw /kb/module \
    && cd /kb/module \
    && PATH=$PATH:/kb/kb_sdk/bin make install

FROM alpine:3.9
MAINTAINER KBase Developer

# update system and system dependencies
#  python2=2.7.15-r3 \
# python2-dev=2.7.15-r3 \
RUN apk upgrade --update-cache --available \
    && apk add --update --no-cache \
    bash=4.4.19-r1 \
    g++=8.2.0-r2 \
    git=2.20.1-r0 \
    libffi-dev=3.2.1-r6 \
    linux-headers=4.18.13-r1 \
    make=4.2.1-r2 \
    openssl-dev=1.1.1a-r1 \
    sqlite=3.26.0-r3 \
    pcre=8.42-r1 \
    pcre-dev=8.42-r1

RUN apk add --no-cache \
    python3=3.6.8-r1 \
    python3-dev=3.6.8-r1 \
    py3-setuptools=40.6.3-r0 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache

# install python dependencies
RUN pip install --upgrade pip \
    && pip install 'jinja2==2.10' \
    && pip install 'uwsgi==2.0.18' \
    && pip install 'jsonrpcbase==0.2.0' \
    && pip install 'requests==2.21.0' \
    && pip install 'python-dateutil==2.8.0' \
    && pip install 'cffi==1.12.0' \
    && pip install 'ndg-httpsclient==0.5.1' \
    && pip install 'pyasn1==0.4.5'

# apsw is a much better sqlite3 library than provided with Pyhton.
# also beware: the apsw distributed through pip repos is NOT the official version
# and is hopelessly out of date.
RUN pip install https://github.com/rogerbinns/apsw/releases/download/3.24.0-r1/apsw-3.24.0-r1.zip \
    --global-option=fetch \
    --global-option=--version \
    --global-option=3.24.0 \
    --global-option=--all \
    --global-option=build \
    --global-option=--enable-all-extensions 

COPY --from=builder /kb/module /kb/module

RUN addgroup --system kbmodule && \
    adduser --system --ingroup kbmodule kbmodule

WORKDIR /kb/module

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
