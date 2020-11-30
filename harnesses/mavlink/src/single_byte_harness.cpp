#include <unistd.h>
#include <string.h>
#include <stdio.h>

#include <common/mavlink.h>

#define SIZE 10000

int main() {
	// make sure buffer is initialized to eliminate variable behaviour that isn't dependent on the input.
	char input[SIZE] = {0};
	ssize_t length;
	length = read(STDIN_FILENO, input, SIZE); 

    for (size_t i = 0; i < length; ++i) {
        mavlink_message_t message;
        mavlink_status_t status;
        mavlink_parse_char(MAVLINK_COMM_0, input[i], &message, &status);
    }
    
    return 0;
}
