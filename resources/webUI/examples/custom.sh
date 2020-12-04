#!/bin/sh

/usr/bin/afl-unix/afl-fuzz -i /DRIFT/workdir/work/initial_seeds -o /DRIFT/workdir/work/ -m 8G -M fuzzer-master -x DICT ARGS BIN > /DRIFT/workdir/work/fuzzer-master.log
