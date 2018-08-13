#!/bin/bash
echo "Running tests..."
script_dir=$(dirname "$(readlink -f "$0")")
export KB_DEPLOYMENT_CONFIG=$script_dir/../deploy.cfg
export KB_AUTH_TOKEN=`cat /kb/module/work/token`
export PYTHONPATH=$script_dir/../lib:$PATH:$PYTHONPATH
cd $script_dir/../test/active

echo "Starting mock servers in the background"
python -m MockServers.run_server --port 5001 --host "localhost" &

echo "Now running tests..."
python -m nose \
    --with-coverage \
    --cover-package=DashboardService \
    --cover-html \
    --cover-html-dir=/kb/module/work/cover_html \
    --nocapture .
