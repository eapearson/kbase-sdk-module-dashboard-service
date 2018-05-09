#!/bin/bash
# script_dir="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
# $script_dir/run_docker.sh run -i -t -v $script_dir/workdir:/kb/module/work test/narrativeservice:latest bash
script_dir=`pwd`/scripts
lib_dir=`pwd`/lib
urlBase="https://ci.kbase.us"
# -p 5000:5000 \
docker run -i -t \
  --network=kbase-dev \
  --name=dashboard_service  \
  --dns=8.8.8.8 \
  -e "KBASE_ENDPOINT=${urlBase}/services" \
  -e "AUTH_SERVICE_URL=${urlBase}/services/auth/api/legacy/KBase/Sessions/Login" \
  -e "AUTH_SERVICE_URL_ALLOW_INSECURE=true" \
  -v $script_dir/workdir:/kb/module/work \
  -v $lib_dir:/kb/module/lib \
  --rm  kbase/dashboard_service:dev bash

