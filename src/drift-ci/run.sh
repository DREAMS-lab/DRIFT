#!/bin/bash

# Add name of binary
binary=$1
GIT_LOCATION=$2

# Run container
docker run -u "root" --privileged \
    -v "$(pwd)/arena:/phuzzui" \
    -it pascal0x90/basic_phuzzer \
    /bin/bash -c "./startup.sh $binary $GIT_LOCATION"
    #-v "$(pwd)/workdir:/phuzzui/workdir" \
