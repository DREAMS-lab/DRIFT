# phuzzer_docker
Based on https://github.com/wes4m/phuzzerUI

## Background
This is a fuzzer built for CIs. 

## Usage
1. Pull the Fuzzer Image
```
docker pull pascal0x90/basic_phuzzer
```
2. Run the Start script with params
```
./run.sh target_binary_name https://github.com/repo/to/clone
```

## Dockerhub Image
https://hub.docker.com/repository/docker/pascal0x90/basic_phuzzer?ref=login

## Modifications
To use this repo, follow the following process:
* Modify the setup.sh script to compile your program to the build folder one level above the folder you clone into. 
* Assure the target binary is called in the startup.sh file. 

### Note
The output of the fuzzer will be thrown into the `arena` folder. This will contain the fuzzer log as well as any crashes found. 
