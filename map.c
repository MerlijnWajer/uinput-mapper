/*
 * Status:
 *
 * - Can map keys from some keyboard to keys on a joystick.
 *
 * Does not:
 * - Show up as a joystick device?
 * - Emulate multiple joysticks
 * - Have a nice mapping file format / datastructures YET.
 *
 */


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

/* Reverse mapping, for later use */
static const struct _key_to_str {
    char *name;
    int num;
} key_map[] = {
#define DEF_KEY(NAME) \
    {#NAME,NAME},
    #include "def_keys.h"
    {NULL, -1}
};

static int get_key_num(char* name)
{
    int i = 0;

    while (key_map[i].name) {
        if (!strcmp(key_map[i].name, name))
            return key_map[i].num;

        i++;
    }

    return -1;
}


/* TODO:
 * - Use atexit() to free joysticks
 * - Add file parsing / reading
 * - Add proper datastructures to keep track
 */

int main(int argc, char** argv) {
    int i, nowrite;
    int in, uin; /* fds */
    struct input_event e, je;
    struct uinput_user_dev uidev;

    /*
     * KEY_LEFT -> ABS_HAT0X
     * KEY_RIGHT -> ABS_HAT0X
     * KEY_UP -> ABS_HAT0Y
     * KEY_DOWN -> ABS_HAT0Y
     *
     * KEY_LEFTCTRL -> BTN_0
     * KEY_LEFTALT -> BTN_1
     * KEY_SPACE -> BTN_2
     *
     * KEY_1 -> BTN_3
     */

    int abskeyevs[] = {
        ABS_HAT0X,
        ABS_HAT0Y,
        0
    };

    int evkeys[] = {
        BTN_JOYSTICK,
        BTN_0,
        BTN_1,
        BTN_2,
        BTN_3,
        0
    };

    /* Open input and uinput */
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

    /* Register device opts */
    if (ioctl(uin, UI_SET_EVBIT, EV_ABS) < 0) {
        perror("ioctl EV_ABS");
        return 1;
    }

    if (ioctl(uin, UI_SET_EVBIT, EV_KEY) < 0) {
        perror("ioctl EV_KEY");
        return 1;
    }

    /* Every ``button'' needs to be registered */
    i = 0;
    while(abskeyevs[i] != 0) {
        if (ioctl(uin, UI_SET_ABSBIT, abskeyevs[i]) < 0) {
            perror("ioctl dynamic");
            return 1;
        }
        i++;
    }

    i = 0;
    while(evkeys[i] != 0) {
        if (ioctl(uin, UI_SET_KEYBIT, evkeys[i]) < 0) {
            perror("ioctl dynamic 2");
            return 1;
        }
        i++;
    }


    /* Allocate device info */
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

    /* Do it! */
    while (1) {
        if (read(in, &e, sizeof(struct input_event))) {
            printf("Event: (Type: %d, Code: %d, Value %d)\n", e.type, e.code, e.value);
        }


        memset(&je, '\0', sizeof(struct input_event));
        nowrite = 0;

        if (e.type == EV_KEY) {
            switch(e.code) {
            case KEY_UP:
                je.type = EV_ABS; je.code = ABS_HAT0Y; je.value = -e.value; break;
            case KEY_DOWN:
                je.type = EV_ABS; je.code = ABS_HAT0Y; je.value = e.value; break;
            case KEY_LEFT:
                je.type = EV_ABS; je.code = ABS_HAT0X; je.value = -e.value; break;
            case KEY_RIGHT:
                je.type = EV_ABS; je.code = ABS_HAT0X; je.value = e.value; break;
            case KEY_LEFTCTRL:
                je.type = EV_KEY; je.code = BTN_0; je.value = e.value; break;
            case KEY_LEFTALT:
                je.type = EV_KEY; je.code = BTN_1; je.value = e.value; break;
            case KEY_SPACE:
                je.type = EV_KEY; je.code = BTN_2; je.value = e.value; break;
            case KEY_1:
                je.type = EV_KEY; je.code = BTN_3; je.value = e.value; break;
            default:
                nowrite = 1;
            }
            if (nowrite == 0) {
                if(write(uin, &je, sizeof(struct input_event)) < 0) {
                    perror("EV_ABS Write event");
                    return -1;
                }
            }
        }

        /* Synchronisation events */
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
    }


}
