#!/bin/bash

echo "Preparing deploy config..."
python3 ./scripts/prepare_deploy_cfg.py ./deploy.cfg ./work/config.properties
echo "Done"
echo `pwd`
cat ./deploy.cfg

if [ -f ./work/token ] ; then
  export KB_AUTH_TOKEN=$(<./work/token)
fi

if [ $# -eq 0 ] ; then
  sh ./scripts/start_server.sh
elif [ "${1}" = "test" ] ; then
  echo "Run Tests"
  make test
elif [ "${1}" = "async" ] ; then
  sh ./scripts/run_async.sh
elif [ "${1}" = "init" ] ; then
  echo "Initialize module"
elif [ "${1}" = "bash" ] ; then
  bash
elif [ "${1}" = "report" ] ; then
  # export KB_SDK_COMPILE_REPORT_FILE=./work/compile_report.json
  # make compile
  cp ./compile_report.json ./work/compile_report.json
  echo "Compilation Report copied to ./work/compile_report.json"
else
  echo Unknown
fi
