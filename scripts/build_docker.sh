#!/bin/bash -x

# Gets the root of the repo, cross platform
root=$(git rev-parse --show-toplevel)

export BRANCH=${TRAVIS_BRANCH:-`git symbolic-ref --short HEAD`}
export DATE=`date -u +"%Y-%m-%dT%H:%M:%SZ"`
export COMMIT=${TRAVIS_COMMIT:-`git rev-parse --short HEAD`}
docker build --build-arg BUILD_DATE=$DATE \
     		 --build-arg VCS_REF=$COMMIT \
			 --build-arg BRANCH=$BRANCH \
             -t test/dashboardservice:latest  ${root} \
			 