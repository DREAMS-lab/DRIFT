cmake_minimum_required(VERSION 3.5)

set(CMAKE_C_COMPILER "$ENV{AFL_DIR}/afl-gcc")
set(CMAKE_CXX_COMPILER "$ENV{AFL_DIR}/afl-g++")
set(CMAKE_CXX_STANDARD 14)

set(CMAKE_CXX_FLAGS -static)

project(mavlink_fuzz_testing)

include_directories(../generated/include/mavlink/v2.0)

add_executable(single_byte_harness
    single_byte_harness.cpp
)

#add_executable(parser_with_random_message
#    parser_with_random_message.cpp
#)

#add_executable(parser_with_assembled_message
#    parser_with_assembled_message.cpp
#)
