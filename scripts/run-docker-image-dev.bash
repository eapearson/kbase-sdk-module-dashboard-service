root=$(git rev-parse --show-toplevel)
source_dir=lib
container_root=/kb/module

#   -e "KBASE_SECURE_CONFIG_PARAM_admin_users=eapearson" \
#   -e "KBASE_SECURE_CONFIG_PARAM_mongo_db=ui_service" \
#   -e "KBASE_SECURE_CONFIG_PARAM_mongo_host=mongo" \
#   -e "KBASE_SECURE_CONFIG_PARAM_mongo_port=27017" \
#   -e "KBASE_SECURE_CONFIG_PARAM_mongo_user=ui_service" \
#   -e "KBASE_SECURE_CONFIG_PARAM_mongo_pwd=ui_service" \


docker run -i -t \
  --network=kbase-dev \
  --name=DashboardService  \
  --dns=8.8.8.8 \
  -p 5000:5000 \
  -e "KBASE_ENDPOINT=https://ci.kbase.us/services" \
  -e "AUTH_SERVICE_URL=https://ci.kbase.us/services/auth/api/legacy/KBase/Sessions/Login" \
  -e "AUTH_SERVICE_URL_ALLOW_INSECURE=true" \
  --mount type=bind,src=${root}/test_local/workdir,dst=${container_root}/work \
  --mount type=bind,src=${root}/${source_dir},dst=${container_root}/${source_dir} \
  --rm  test/dashboard-service:dev 
