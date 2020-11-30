```Run in Pascal0x90's phuzzer_docker with: sudo ./run.sh single_byte_harness.cpp https://github.com/BPDanek/mavlink-afl-harness.git ```

For other normal usage: 
# MavLink AFL Harness
This a just the harnessing source code, and accompanying compile scripts, for
fuzzing the MavLink communication library. It is based on the repo for fuzzing
using LibFuzzer [here](https://github.com/Auterion/mavlink-fuzz-testing). 

## Instructions

1. Have [AFL](https://github.com/google/AFL) downloaded and compiled. Also make
   sure to have `cmake`

2. Run Setup Script
To run the setup script all you must do is give it the location of the AFL
folder where AFL's binaries are located
```bash
./setup /absolute/path/to/AFL/
```

3. Run AFL on Harness:
```
/path/to/afl-fuzz -i in_dir -o out_dir build/single_byte_harness
```

## TODO
To make this fuzzer better a few things can be done:
1. Add support for other harnesses (see src folder)
2. Get example MavLink packets for seeds
3. Find some crashing examples from other repos for regression testing

