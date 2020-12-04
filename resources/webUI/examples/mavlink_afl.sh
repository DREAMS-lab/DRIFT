#!/bin/sh

/usr/bin/afl-unix/afl-fuzz -i /DRIFT/workdir/work/initial_seeds -o /DRIFT/workdir/work/ -m 8G -M fuzzer-master -x /DRIFT/workdir/work/dict.txt -- /DRIFT/webUI/examples/mavlink > /DRIFT/workdir/work/fuzzer-master.log
