#!/bin/bash
# script_dir="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
# $script_dir/run_docker.sh run -i -t -v $script_dir/workdir:/kb/module/work test/narrativeservice:latest bash
root=$(git rev-parse --show-toplevel)
script_dir=${root}/scripts
lib_dir=${root}/lib
  # -v $script_dir/workdir:/kb/module/work \
  # -v $lib_dir:/kb/module/lib \

docker run -i -t \
  --network=kbase-dev \
  --name=dashboard_service2  \
  --dns=8.8.8.8 \
  -e "KBASE_ENDPOINT=https://ci.kbase.us/services" \
  -e "AUTH_SERVICE_URL=https://ci.kbase.us/services/auth/api/legacy/KBase/Sessions/Login" \
  -v $script_dir/workdir:/kb/module/work \
  -v $lib_dir:/kb/module/lib \
  -e "AUTH_SERVICE_URL_ALLOW_INSECURE=true" \
  --rm  test/dashboardservice:latest bash

