#!/bin/bash
set -veu

ROOT_DIR=$(pwd)

if [[ "$(docker images -q usagi/test:latest 2> /dev/null)" == "" ]]; then
    docker build -f Dockerfile-forTest -t usagi/test .
fi

docker run -it --rm \
    -v ${ROOT_DIR}/test:/usagi/test \
    -v ${ROOT_DIR}/api:/usagi/api \
    -v ${ROOT_DIR}/importer:/usagi/importer \
    -v ${ROOT_DIR}/installer:/usagi/installer \
    -v ${ROOT_DIR}/command:/usagi/command \
    -v ${ROOT_DIR}/config:/usagi/config \
    usagi/test
