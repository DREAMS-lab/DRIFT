# check parameter count 
if [ "$#" -ne 2 ]; then
    echo "Error: Not enough parameters, got $1 and $2"
    echo "Usage: ./setup {afl_directory} {name_of_binary}"
    exit 1
fi

# make build loc
 mkdir build

# download requirements
apt install cmake -y

# set the afl directory location
AFL_DIR=$1

# init MavLink
git submodule update --init --recursive
sleep 2

# compile MavLink
(cd mavlink/pymavlink/ && tools/mavgen.py --lang=C --wire-protocol=2.0 --output=../../generated/include/mavlink/v2.0 ../message_definitions/v1.0/common.xml)

# compile the harness
$AFL_DIR/afl-g++ -I generated/include/mavlink/v2.0 -static src/$2 -o /phuzzui/build/$2
