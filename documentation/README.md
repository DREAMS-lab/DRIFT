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
failing built-in code assertions, or potential memory leaks. Fuzzers are used to test programs that take structured inputs.

The exact implementation of the fuzzing mechanism in this library varies, and will continue to change with time since this is a prominent research area. Fundamentally, a fuzzer recieves a harnessing program, which harnesses the library/target being fuzzed. The fuzzer passes the harness program, and observes how far the passed inputs get. The fuzzing engine compiles the harness program, allowing the program control flow graph to be monitored. 

For exact information on how different types of fuzzers are used see [LLVM](https://llvm.org/docs/FuzzingLLVM.html#fuzzing-llvm-generic).

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

A fuzzing harness is a program which allows input from the fuzzing engine to be passed too the libarary which is the subject of the fuzzing procedure being mentioned. An simple example of a fuzzing harness is the [Mavlink single_byte_harness](https://github.com/DREAMS-lab/DRIFT/blob/main/harnesses/mavlink/src/single_byte_harness.cpp). The program has a main, and a stdin which is passed to a function in Mavlink, the library being fuzzed. This program will be comipled with afl-g++, which allows the engine to mount the harnessing program. 

This example has important components: a main, an input vector (in this case it is stdin which takes command line arguments), and a way to call Mavlink. The harnessing program is compiled with the fuzzing engine; the fuzzing engine will be able to trace how far the input, which was passed to the library via the stdin in the harness gets. Exact guides to writing harnesses for afl can be found on the site [afl quick start](https://lcamtuf.coredump.cx/afl/QuickStartGuide.txt).

We have provided some harnesses for Mavlink. It is more than likely there are different harnesses which can be made for the same library. Designing different harnesses for the same library will allow one to fuzz different parts of the libary, which relates to increased code coverage. 

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
WebUI runs at port 8888 by default. The container can also be run in debug mode and with different options as follows
```
Usage: ./run [OPTIONS] <port> (Defaults to port 8888)

OPTIONS:
-h    Print this Help.
-d    Debug mode, runs container with interactive shell instead of WebUI.
```
#### CI Integration
The CI integration version of the DRIFT WebUI is for use as an extension of the CI pipeline. It runs automatically as an instance to reflect the current
status of the CI while it is running and fuzzing a component.
For use, after building the container. Navigate to the CI integration version of the WebUI
```
cd DRIFT/src/drift-ui-ci
```
1. Include the WebUI code inside the docker container used for fuzzing which is run by the CI, and run the WebUI `start.sh`
2. Another option is to keep the WebUI docker container seprate and just mount the fuzz-master log path to the WebUI.

DRIFT WebUI will default to monitroing `/dev/shm/work/` and will look for `fuzzer-master.log` as an indicator of the CI starting the fuzzer, it will also pull info from the same path.
once the log is removed the UI will stop monitoring.

To change the log path to monitor simply modify last line in `DRIFT/src/drift-ui-ci/src/app.py`

### Options
DRIFT WebUI provides a set of custom options for cases where a custom binary is to be fuzzed. 
#### Custom harnesses
The WebUI interface provides an option to choose a custom binary. Custom binaries are listed in the WebUI dropdown menu with the other components.
In order for the binary to show it must be placed in `DRIFT/src/drift-ui/src/examples/`. The binary must have an stdin input vector or otherwise be a harness
that is provided with the correct arguments option see [Custom arguments](#custom-arguments).

#### Custom dictonaries
The WebUI provides the option of choosing a custom dictonary to pass to AFL++, the textbox in the WebUI takes the path to the dictonary. 
The path and the dictonary must be present inside the WebUI container which can be achived through either placing it inside `DRIFT/src/drift-ui/src/examples/` or by mounting a volume.

#### Custom arguments
The WebUI provides the option of choosing a custom argument to be passed to the binary. The textbox takes arguments in the form AFL takes them. 
By default AFL++ will pass input through stdin. To pass input through a file for example use `@@` as a custom argument.
See docs for AFL for more information.

### Logs
Detailed Logs of each fuzzing instance are stored in `/dev/shm/work/` in the WebUI container which can be attached to, or run in debug mode to view.
Another option is to keep the WebUI docker container seprate and just mount the `fuzz-master.log` log path to the WebUI as in the CI integration option.

