# assume running in deployment directory

root=$(git rev-parse --show-toplevel)

rm -rf docker/context/contents
mkdir docker/context/contents 
cd docker/context/contents
cp -pr ${root}/lib .
cp -pr ${root}/scripts .
cp -pr ${root}/test .
cp ${root}/deploy.cfg .
cp ${root}/kbase.yml .
cp ${root}/Makefile .
cp ${root}/*.spec .
