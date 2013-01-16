#include <stdio.h>
#include <stdlib.h>
#include <linux/input.h>

#include <unistd.h>
#include <fcntl.h>

#define INPUT_PATH "/dev/input/by-id/usb-Logitech_USB-PS_2_Optical_Mouse-event-mouse"

int main (int argc, char** argv) {
    int f;

    (void)argc;
    (void)argv;


    f = open(INPUT_PATH, O_RDONLY);

    if (f < 0) {
        perror("open");
        return 1;
    }


    return 0;
}
