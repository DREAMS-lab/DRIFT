# DRIFT Documentation

## Table of contents 
1. [Overview](#overview)
    1. [Description](#description)
    2. [Fuzzing](#fuzzing)
    3. [Research](#research)
        1. [PX4](#px4)
        2. [Gazebo](#gazebo)
        3. [Mavlink](#mavlink)
        4. [Harnessing](#harnessing)
2. [Components](#components)
    1. [Fuzzing engine](#fuzzing-engine)
    2. [CI](#ci)
        1. [Installation](#ci-installation)
        2. [Usage](#ci-usage)
            1. [??](#example)
    3. [WebUI](#webui)
        1. [Installation](#webui-installation)
        2. [Usage](#webui-usage)
            1. [Standalone](#standalone)
            2. [CI Integration](#ci-integration)
        3. [Options](#webui-options)
            1. [Custom harnesses](#custom-harnesses)
            2. [Custom dictonaries](#custom-dictonaries)
            3. [Custom Arguments](#custom-arguments)
        4. [Logs](#webui-logs)


# Overview
## Description
D.R.I.F.T short for Drone Research Integrated [Fuzzing](#fuzzing) Tool aims to solve the above problems through the use of a security testing mechanism called fuzzing,
which is an automated method that can provide insight into what bugs,
issues, and vulnerabilities that drone system could have with extreme speeds and advantage over manual labor.
## Fuzzing
Fuzzing or fuzz testing is an automated software testing technique that involves providing invalid,
unexpected, or random data as inputs to a computer program. The program is then monitored for exceptions such as crashes,
failing built-in code assertions, or potential memory leaks. Typically, fuzzers are typically used to test programs that take structured inputs.
## Research
DRIFT main focus is DREAMS lab development pipeline and the components involved in developing drone's software.
Such as PX4, Gazebo, Mavlink. This also includes the various internal sub-components used by said components.
Researching was required in order to fuzz the different components. The below results are a quick overview of each component.
### PX4
PX4 is an open source flight control software for drones and other unmanned vehicles. It is the firmware DRIFT focuses on. 
DRIFT research showed that PX4 firmware can be harnessed for use in DRIFT. A few expirmental harnsses were made. However, due to time constaints 
a fully functional harness has not been made.
[Link](https://px4.io)
### Gazebo
Gazebo is a well-known and respected robotics simulator, and is also the official DARPA Virtual Robotics Simulator. It is used by Gazebo SITL. Through DRIFT research we concluded that
the best candidate in the given time to fuzz was one of Gazeb's internal components that is gz-server. gz-server had its own challenges with
performance issues. Another internal component of Gazebo is the sdformat lib which DRIFT harnessed an input vector for. [Link](http://gazebosim.org)
### Mavlink
MAVLink or Micro Air Vehicle Link is a protocol for communicating with small unmanned vehicle. It is designed as a header-only message marshaling library.
It is used by PX4 with ROS, named MavROS which is MAVLink extendable communication node for ROS with proxy for Ground Control Station. Through DRIFT research
we have harnessed multiple input vecotors to Mavlink allowing DRIFT to integrate Mavlink developemnt pipeline and efficiently fuzz it. [Link](https://mavlink.io/en/)
### Harnessing
Harnessing is the process involing any step necessary to get a useable input vector to allow fuzzer to feed an input to the program, and have the ability to
correctly follow the state of its execution. Harnessing is the backbone of fuzzing and thus the manjority of DRIFT efforts were spent researching the different components 
and harnessing them. Harnesses can be found in [Harnesses](https://github.com/DREAMS-lab/DRIFT/tree/main/harnesses).

# Components
## Fuzzing engine
The main component of DRIFT is its fuzzing engine. DRIFT can be easily modified to use different fuzzing engines such as AFL, AFL++, and libFuzzer.
DRIFT makes uses of different wrappers around the main fuzzing engine to provide the best fuzzing results. DRIFT uses [AFL++](https://github.com/AFLplusplus/AFLplusplus) and the following frameworks, [phuzzer](https://github.com/angr/phuzzer), 
[driller](https://github.com/shellphish/driller) and [shellphuzz](https://github.com/shellphish/fuzzer/blob/master/shellphuzz) as well as DRIFT custom functionalities.

## CI
### Installation <a name="ci-installation"></a>
### Usage <a name="ci-usage"></a>

## WebUI
The WebUI provides an easy to use cross-platform graphical interface that can be used as a standalone DRIFT instance to fuzz any of the given components using
the provides harnesses or input a custom component provided a harness and other options such as a dictonary, and arguments.
### Installation <a name="webui-installation"></a>
DRIFT WebUI is shipped as a docker container for ease of use.
To install standalone version clone DRIFT repository
```
git clone https://github.com/DREAMS-lab/DRIFT.git
```
Navigate to the standalone version of the WebUI
```
cd DRIFT/src/drift-ui
```
Execute the builder script
```
./build
```

To install the CI integration version clone DRIFT repository
```
git clone https://github.com/DREAMS-lab/DRIFT.git
```
Navigate to the CI integration version of the WebUI
```
cd DRIFT/src/drift-ui-ci
```
Execute the builder script
```
./build
```
### Usage <a name="webui-usage"></a>
#### Standalone
The standalone version of the DRIFT WebUI is for use as a direct DRIFT instance to fuzz the provided components or a custom binary.
For use, after building the container. Navigate to the Standalone version of the WebUI
```
cd DRIFT/src/drift-ui
```
Execute the runner script
```
./run
```
WebUI runs at port 8080 by default. The container can also be run in debug mode and with different options as follows
```
Usage: ./run [OPTIONS] <port> (Defaults to port 8888)

OPTIONS:
-h    Print this Help.
-d    Debug mode, runs container with interactive shell instead of WebUI.
```
#### CI Integration
### Options
#### Custom harnesses
#### Custom dictonaries
#### Custom arguments
### Logs
