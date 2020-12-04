#!/bin/sh

/usr/bin/afl-unix/afl-fuzz -i /DRIFT/workdir/phuzwork/initial_seeds -o /DRIFT/workdir/phuzwork/ -m 8G -M fuzzer-master -x /DRIFT/workdir/phuzwork/dict.txt -- /phuzzui/examples/mavlink > /DRIFT/workdir/phuzwork/fuzzer-master.log
