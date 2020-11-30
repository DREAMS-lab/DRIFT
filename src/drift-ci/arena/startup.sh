#!/bin/bash

# fix python
rm /usr/bin/python
ln -s /usr/bin/python3 /usr/bin/python

# Take in name of binary
binary=$1

# Take in git repo
GIT_LOCATION=$2

# Get the harness
git clone $GIT_LOCATION harness 

# Compile binary
mkdir build
cp setup.sh harness/.
cd ./harness 
./setup.sh /phuzzers/AFLplusplus $binary
cd ../

cd /phuzzui

# Remove soruce
rm -rf ./harness

# Sets kernel options for AFL
echo core > /proc/sys/kernel/core_pattern
echo 1 > /proc/sys/kernel/sched_child_runs_first

# Make working dir and results dir
mkdir /phuzzer/workdir
mkdir run

# run
python3 -m phuzzer -p AFL++ -c 1 -w /phuzzui/workdir "/phuzzui/build/$binary"

# if we wanna be cool and provide a seed dir just need to do the following
#mkdir seed_dir
#python3 -m phuzzer -p AFL++ -c 1 -w /phuzzui/workdir -s /phuzzui/seed_dir "/phuzzui/build/$binary"
mv seed_dir run/.

# Consolidate everything
mv build run/.
mv run_* run/.
mv core run/.

# Make everything readable since root created it
chmod -R 777 /phuzzui/run
