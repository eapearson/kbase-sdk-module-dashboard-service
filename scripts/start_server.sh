#!/bin/bash
script_dir=$(dirname "$(readlink -f "$0")")
export KB_DEPLOYMENT_CONFIG=$script_dir/../deploy.cfg
uwsgi --master --processes 5 --threads 5 --http :5000 --wsgi-file $script_dir/../lib/DashboardService/DashboardServiceServer.py
