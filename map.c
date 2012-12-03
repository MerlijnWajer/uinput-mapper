#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <unistd.h>
#include <fcntl.h>

#include <time.h>

#include <linux/input.h>
#include <linux/uinput.h>

#define INPUT_PATH "/dev/input/by-path/platform-i8042-serio-0-event-kbd"
/*#define INPUT_PATH "/dev/input/by-path/platform-i8042-serio-0-event-kbd"*/
#define UINPUT_PATH "/dev/uinput"

/* TODO:
 * - Use atexit() to free joysticks
 * - Make joysticks static
 *
 *
 */

int main(int argc, char** argv) {
    int in, uin;
    struct input_event e, je;
    struct uinput_user_dev uidev;

    in = open(INPUT_PATH, O_RDONLY);
    if(in < 0) {
        perror("open in");
        return 1;
    }

    uin = open(UINPUT_PATH, O_WRONLY | O_NONBLOCK);
    if (uin < 0) {
        perror("open uin");
        return 2;
    }

    /* Create devices */
    if (ioctl(uin, UI_SET_EVBIT, EV_ABS) < 0) {
        perror("ioctl EV_ABS");
        return 1;
    }

    if (ioctl(uin, UI_SET_EVBIT, EV_KEY) < 0) {
        perror("ioctl EV_KEY");
        return 1;
    }

    /* Every ``button'' needs to be registered */
    if (ioctl(uin, UI_SET_ABSBIT, ABS_HAT0Y) < 0) {
        perror("ioctl ABS_");
        return 1;
    }

    memset(&uidev, '\0', sizeof(struct uinput_user_dev));
    snprintf(uidev.name, UINPUT_MAX_NAME_SIZE, "key2joy:1");

    uidev.id.bustype = BUS_USB;
    uidev.id.vendor  = 0x42;
    uidev.id.product = 0xbebe;
    uidev.id.version = 1;

    if (write(uin, &uidev, sizeof(uidev)) < 0) {
        perror("write");
        return -1;
    }

    if (ioctl(uin, UI_DEV_CREATE)) {
        perror("ioctl create");
        return 1;
    }

    while (1) {
        printf("in: %d, uin: %d\n", in, uin);
        if (read(in, &e, sizeof(struct input_event))) {
            printf("Event: (Type: %d, Code: %d, Value %d)\n", e.type, e.code, e.value);
        }


        if (e.type == EV_KEY && e.code == KEY_UP) {
            memset(&je, '\0', sizeof(struct input_event));
            je.type = EV_ABS;
            je.code = ABS_HAT0Y;
            je.value = -e.value;
            if(write(uin, &je, sizeof(struct input_event)) < 0) {
                perror("EV_ABS Write event");
                return -1;
            }
        }
        if (e.type == EV_SYN) {
            memset(&je, '\0', sizeof(struct input_event));
            printf("SYN event\n");

            je.type = EV_SYN;
            je.code = 0;
            je.value = 0;

            if (write(uin, &je, sizeof(struct input_event)) < 0) {
                perror("SYN write event");
                return -1;
            }
        }
        printf("---\n");
    }


}
