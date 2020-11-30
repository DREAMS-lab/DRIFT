#!/bin/bash

# This file should be in the root of the 
# source of the project.  

AFL_LOCATION=$1
binary=$2

# Start compilation
$AFL_LOCATION/afl-clang-fast chall.bin.c -o /phuzzui/build/$binary

