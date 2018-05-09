#!/bin/bash
script_dir=$(dirname "$(readlink -f "$0")")
python -u $script_dir/../lib/DashboardService/DashboardServiceServer.py $1 $2 $3
